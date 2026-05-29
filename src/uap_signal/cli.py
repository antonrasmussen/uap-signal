"""CLI entry point for UAP Signal."""

from __future__ import annotations

from datetime import date

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
from uap_signal.models import ContentType, Release, SourceTrust
from uap_signal.sources import SOURCE_REGISTRY, fetch_all
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

    if dry_run:
        print_fetched_table(releases)
        print_cost_estimate(len(releases))
        return

    rows = []
    with Store(settings.database_path) as store:
        store.save_releases(releases)
        for release in releases:
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

    print_report(target_date.isoformat(), rows)


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
            result = summarize_release(release, classification, settings, store, provider_override=provider, model_override=model)
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
        from uap_signal.models import AnalysisResult, Classification

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


if __name__ == "__main__":
    app()
