"""CLI entry point for UAP Signal."""

from __future__ import annotations

from datetime import date
from pathlib import Path

import typer

from uap_signal.analyzer import AnalysisConfigurationError, summarize_release
from uap_signal.classifier import classify_release
from uap_signal.config import get_settings
from uap_signal.display import (
    print_cost_estimate,
    print_fetched_table,
    print_report,
    print_source_errors,
    print_sources,
)
from uap_signal.mailer import send_failure_alert, send_markdown_email
from uap_signal.models import AnalysisResult, Classification, ContentType, Release, SourceTrust
from uap_signal.pipeline import (
    backfill_existing_reports,
    generate_release_report,
    run_digest,
    run_watch,
    send_existing_report,
)
from uap_signal.release_watch import ReleaseBatch, detect_new_releases, format_release_label
from uap_signal.sources import SOURCE_REGISTRY, fetch_all, warufo
from uap_signal.state import load_release_state
from uap_signal.store import Store

app = typer.Typer(help="UAP Signal: cut through UAP/UFO release noise.")


def _parse_date(value: str | None) -> date:
    return date.fromisoformat(value) if value else date.today()


@app.command("check")
def check(
    date_str: str | None = typer.Option(None, "--date", help="Date in YYYY-MM-DD format."),
    source: str | None = typer.Option(None, "--source", help="Single source name."),
    max_items: int | None = typer.Option(None, "--max-items", help="Max items sent to LLM."),
    dry_run: bool = typer.Option(False, "--dry-run", help="Fetch and show items without LLM analysis or DB writes."),
    new_only: bool = typer.Option(False, "--new-only", help="Skip items already analyzed."),
    model_provider: str | None = typer.Option(None, "--provider", help="anthropic or openai."),
    model: str | None = typer.Option(None, "--model", help="Override LLM model."),
) -> None:
    """Fetch, classify, summarize and show what's new."""
    settings = get_settings()
    target_date = _parse_date(date_str)
    selected = [source] if source else None
    source_errors: list[str] = []
    try:
        releases = fetch_all(
            target_date,
            selected_sources=selected,
            errors=source_errors,
            extract_content=not dry_run,
        )
    except ValueError as exc:
        raise typer.BadParameter(str(exc)) from exc

    releases = releases[: max(1, max_items or settings.max_items)]
    print_source_errors(source_errors)

    if new_only:
        with Store(settings.database_path) as store:
            seen = store.get_analyzed_urls()
        releases = [r for r in releases if r.url not in seen]
        if not releases:
            typer.echo("All items already analyzed.")
            return

    if dry_run:
        print_fetched_table(releases)
        print_cost_estimate(len(releases))
        return

    rows = []
    with Store(settings.database_path) as store:
        store.save_releases(releases)
        seen_urls = store.get_analyzed_urls()
        new_count = 0
        cached_count = 0
        for release in releases:
            if release.url in seen_urls:
                cached = store.get_analysis_by_url(release.url)
                if cached:
                    analysis = AnalysisResult(
                        release_url=release.url,
                        classification=Classification(cached["classification"]),
                        summary=cached["summary"],
                        why_it_matters=cached["why_it_matters"],
                        novelty_score=int(cached["novelty_score"]),
                        model_used=cached["model_used"],
                        content_hash=cached["content_hash"],
                        reasoning=cached["reasoning"],
                    )
                    rows.append((release, analysis))
                    cached_count += 1
                    continue
            classification = classify_release(release, store=store)
            try:
                analysis = summarize_release(
                    release=release,
                    classification=classification,
                    settings=settings,
                    store=store,
                    provider_override=model_provider,
                    model_override=model,
                )
            except AnalysisConfigurationError as exc:
                raise typer.BadParameter(str(exc)) from exc
            rows.append((release, analysis))
            new_count += 1

    print_report(target_date.isoformat(), rows)
    if new_count or cached_count:
        from rich.console import Console

        Console().print(f"{new_count} new, {cached_count} cached", style="dim")


@app.command("analyze")
def analyze(
    url: str,
    provider: str | None = typer.Option(None, "--provider", help="anthropic or openai"),
    model: str | None = typer.Option(None, "--model", help="Override LLM model."),
) -> None:
    """Analyze a single URL."""
    settings = get_settings()
    with Store(settings.database_path) as store:
        release = Release(
            url=url,
            title=f"Ad-hoc analysis: {url}",
            source_name="ad_hoc",
            source_trust=SourceTrust.UNKNOWN,
            content_type=ContentType.HTML,
            raw_text=url,
        )
        store.save_releases([release])
        classification = classify_release(release, store=store)
        try:
            result = summarize_release(
                release, classification, settings, store, provider_override=provider, model_override=model
            )
        except AnalysisConfigurationError as exc:
            raise typer.BadParameter(str(exc)) from exc
    print_report(date.today().isoformat(), [(release, result)])


@app.command("sources")
def sources() -> None:
    """Show configured source stats."""
    settings = get_settings()
    with Store(settings.database_path) as store:
        stats = list(store.get_source_stats())
    if not stats:
        stats = [{"source_name": name, "item_count": 0, "last_seen": "-"} for name in SOURCE_REGISTRY]
    print_sources(stats)


@app.command("history")
def history(days: int = typer.Option(7, "--days")) -> None:
    """Show previously seen items from local DB."""
    settings = get_settings()
    with Store(settings.database_path) as store:
        rows = store.get_recent_releases(days=days)
    payload = []
    for row in rows:
        release = Release(
            url=row["url"],
            title=row["title"],
            source_name=row["source_name"],
            source_trust=SourceTrust(row["source_trust"]),
            content_type=ContentType(row["content_type"]),
            first_seen_date=row["first_seen_date"],
            raw_text=row["raw_text"],
        )
        analysis = AnalysisResult(
            release_url=row["url"],
            classification=Classification(row["classification"] or "CONTEXT"),
            summary=row["summary"] or "(not analyzed)",
            novelty_score=int(row["novelty_score"] or 0),
        )
        payload.append((release, analysis))
    print_report(f"last {days} days", payload)


@app.command("config")
def config() -> None:
    """Print active runtime config."""
    settings = get_settings()
    masked_anthropic = "set" if settings.anthropic_api_key else "missing"
    masked_openai = "set" if settings.openai_api_key else "missing"
    typer.echo(f"db={settings.database_path}")
    typer.echo(f"provider={settings.provider}")
    typer.echo(f"model={settings.model}")
    typer.echo(f"anthropic_api_key={masked_anthropic}")
    typer.echo(f"openai_api_key={masked_openai}")
    typer.echo(f"email_provider={settings.email_provider}")
    typer.echo(f"email_to={'set' if settings.email_to else 'missing'}")
    typer.echo(f"reports_dir={settings.reports_dir}")
    typer.echo(f"state_dir={settings.state_dir}")


@app.command("watch")
def watch(
    dry_run: bool = typer.Option(False, "--dry-run", help="Skip email and state/report writes."),
    force_release: str | None = typer.Option(None, "--force-release", help="Process a specific release ID."),
    no_heartbeat: bool = typer.Option(False, "--no-heartbeat", help="Skip heartbeat email when nothing is new."),
    provider: str | None = typer.Option(None, "--provider", help="anthropic or openai."),
    model: str | None = typer.Option(None, "--model", help="Override LLM model."),
) -> None:
    """Daily watcher: detect new PURSUE releases, report + email, or heartbeat."""
    settings = get_settings()
    try:
        result = run_watch(
            settings,
            dry_run=dry_run,
            force_release=force_release,
            no_heartbeat=no_heartbeat,
            provider=provider,
            model=model,
        )
    except AnalysisConfigurationError as exc:
        raise typer.BadParameter(str(exc)) from exc
    except Exception as exc:
        if not dry_run:
            send_failure_alert(settings, str(exc))
        raise

    typer.echo(f"status={result['status']}")
    typer.echo(f"new_releases={','.join(result['new_releases']) or '-'}")
    typer.echo(f"emailed={result['emailed']}")
    if result["report_paths"]:
        typer.echo("reports=" + ", ".join(result["report_paths"]))


@app.command("report")
def report_cmd(
    release_id: str = typer.Argument(..., help="Release ID such as 05 or 5."),
    dry_run: bool = typer.Option(False, "--dry-run", help="Analyze/render without writing state."),
    provider: str | None = typer.Option(None, "--provider", help="anthropic or openai."),
    model: str | None = typer.Option(None, "--model", help="Override LLM model."),
) -> None:
    """Generate a markdown report for a specific PURSUE release (no email)."""
    settings = get_settings()
    rid = format_release_label(release_id)
    batches = detect_new_releases(load_release_state(settings.state_dir), force_release=rid)
    if not batches:
        items = warufo.fetch(date.today(), extract_content=False, release_filter=rid)
        if not items:
            raise typer.BadParameter(f"Release {rid} not found in warufo archive.")
        batches = [ReleaseBatch(release_id=rid, items=items)]
    try:
        markdown, path = generate_release_report(
            batches[0],
            settings,
            dry_run=dry_run,
            provider=provider,
            model=model,
        )
    except AnalysisConfigurationError as exc:
        raise typer.BadParameter(str(exc)) from exc
    typer.echo(f"wrote={path}")
    typer.echo(f"chars={len(markdown)}")


@app.command("send-report")
def send_report(
    path: Path,
) -> None:
    """Email an existing markdown report file."""
    if not path.exists() or not path.is_file():
        raise typer.BadParameter(f"Report not found: {path}")
    settings = get_settings()
    ok = send_existing_report(settings, path)
    if not ok:
        raise typer.Exit(code=1)
    typer.echo(f"sent={path}")


@app.command("digest")
def digest(
    dry_run: bool = typer.Option(False, "--dry-run", help="Skip email and news-state writes."),
    provider: str | None = typer.Option(None, "--provider", help="anthropic or openai."),
    model: str | None = typer.Option(None, "--model", help="Override LLM model."),
) -> None:
    """Weekly news digest: analyze new RSS items and email a digest."""
    settings = get_settings()
    try:
        result = run_digest(settings, dry_run=dry_run, provider=provider, model=model)
    except AnalysisConfigurationError as exc:
        raise typer.BadParameter(str(exc)) from exc
    except Exception as exc:
        if not dry_run:
            send_failure_alert(settings, str(exc))
        raise
    typer.echo(f"status={result['status']}")
    typer.echo(f"item_count={result['item_count']}")
    typer.echo(f"emailed={result['emailed']}")


@app.command("send-test")
def send_test() -> None:
    """Send a short SMTP/Resend connectivity test email."""
    settings = get_settings()
    body = (
        f"# UAP Signal test email\n\n"
        f"Provider: `{settings.email_provider}`\n\n"
        f"If you received this, email delivery is working."
    )
    ok = send_markdown_email(settings, subject="UAP Signal test email", markdown_body=body)
    if not ok:
        raise typer.Exit(code=1)
    typer.echo("sent=test")


@app.command("backfill-email")
def backfill_email() -> None:
    """Email all existing reports in reports/ as separate messages (oldest first)."""
    settings = get_settings()
    sent = backfill_existing_reports(settings)
    if not sent:
        typer.echo("sent=0")
        raise typer.Exit(code=1)
    for path in sent:
        typer.echo(f"sent={path}")


if __name__ == "__main__":
    app()
