"""Orchestration for daily watch, report generation, and weekly digests."""

from __future__ import annotations

import logging
from datetime import date
from pathlib import Path

from uap_signal.analyzer import summarize_release, synthesize_report
from uap_signal.classifier import classify_release
from uap_signal.config import Settings
from uap_signal.mailer import send_markdown_email
from uap_signal.models import AnalysisResult, Classification, Release
from uap_signal.release_watch import ReleaseBatch, detect_new_releases, format_release_label, iso_now
from uap_signal.report import (
    ReportItem,
    Synthesis,
    render_digest,
    render_heartbeat,
    render_release_report,
    report_filename,
    subject_for_release,
    subject_from_markdown_path,
    write_report,
)
from uap_signal.sources import fetch_all, warufo
from uap_signal.state import (
    load_news_state,
    load_release_state,
    save_news_state,
    save_release_state,
)
from uap_signal.store import Store

logger = logging.getLogger(__name__)


def _analyze_items(
    releases: list[Release],
    settings: Settings,
    *,
    provider: str | None = None,
    model: str | None = None,
) -> list[ReportItem]:
    rows: list[ReportItem] = []
    with Store(settings.database_path) as store:
        store.save_releases(releases)
        seen_urls = store.get_analyzed_urls()
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
                    rows.append(ReportItem(release=release, analysis=analysis))
                    continue
            classification = classify_release(release, store=store)
            analysis = summarize_release(
                release=release,
                classification=classification,
                settings=settings,
                store=store,
                provider_override=provider,
                model_override=model,
            )
            rows.append(ReportItem(release=release, analysis=analysis))
    return rows


def generate_release_report(
    batch: ReleaseBatch,
    settings: Settings,
    *,
    report_date: date | None = None,
    include_news: bool = True,
    dry_run: bool = False,
    provider: str | None = None,
    model: str | None = None,
) -> tuple[str, Path]:
    report_day = report_date or date.today()
    rid = format_release_label(batch.release_id)
    release_day = batch.release_date or report_day

    primary_releases = warufo.fetch(report_day, extract_content=not dry_run, release_filter=rid)
    if not primary_releases:
        primary_releases = batch.items

    primary_items = _analyze_items(primary_releases, settings, provider=provider, model=model)

    news_items: list[ReportItem] = []
    if include_news:
        errors: list[str] = []
        news_releases = fetch_all(
            report_day,
            selected_sources=["news_rss"],
            errors=errors,
            extract_content=not dry_run,
        )
        for err in errors:
            logger.warning("news source warning: %s", err)
        news_releases = news_releases[: settings.max_items]
        news_items = _analyze_items(news_releases, settings, provider=provider, model=model)

    if dry_run:
        synthesis = Synthesis(
            executive_summary=(
                f"Dry-run synthesis for PURSUE Release {rid} "
                f"({len(primary_items)} primary items, {len(news_items)} news items)."
            ),
            key_findings=[
                "Dry-run mode: LLM synthesis skipped.",
                f"Primary item count: {len(primary_items)}.",
                f"News item count: {len(news_items)}.",
            ],
            character=f"PURSUE Release {rid}",
            next_steps=["Re-run without --dry-run to generate the full report."],
        )
    else:
        synthesis = synthesize_report(
            release_id=rid,
            release_date=release_day.isoformat(),
            items=[(item.release, item.analysis) for item in primary_items],
            settings=settings,
            provider_override=provider,
            model_override=model,
        )

    state = load_release_state(settings.state_dir)
    markdown = render_release_report(
        release_id=rid,
        report_date=report_day,
        release_date=release_day,
        primary=primary_items,
        news=news_items,
        synthesis=synthesis,
        state=state,
    )
    path = Path(settings.reports_dir) / report_filename(rid, report_day)
    if not dry_run:
        write_report(path, markdown)
        state.mark(
            rid,
            file_count=len(primary_items),
            release_date=release_day.isoformat(),
            report_path=str(path),
            first_seen_at=iso_now(),
        )
        save_release_state(settings.state_dir, state)
    return markdown, path


def run_watch(
    settings: Settings,
    *,
    dry_run: bool = False,
    force_release: str | None = None,
    no_heartbeat: bool = False,
    provider: str | None = None,
    model: str | None = None,
) -> dict:
    """Daily entry point: detect new releases, report + email, or heartbeat."""
    report_day = date.today()
    state = load_release_state(settings.state_dir)
    batches = detect_new_releases(state, target_date=report_day, force_release=force_release)

    if not batches:
        heartbeat = render_heartbeat(
            report_date=report_day,
            seen_releases=sorted(state.releases),
            latest_release=max(state.releases) if state.releases else None,
        )
        emailed = False
        if not dry_run and not no_heartbeat:
            emailed = send_markdown_email(
                settings,
                subject=f"UAP Signal Heartbeat — {report_day.isoformat()}",
                markdown_body=heartbeat,
            )
        return {
            "status": "heartbeat",
            "new_releases": [],
            "emailed": emailed,
            "report_paths": [],
        }

    report_paths: list[str] = []
    emailed_any = False
    for batch in batches:
        markdown, path = generate_release_report(
            batch,
            settings,
            report_date=report_day,
            dry_run=dry_run,
            provider=provider,
            model=model,
        )
        report_paths.append(str(path))
        if dry_run:
            continue
        subject = subject_for_release(batch.release_id, report_day)
        if send_markdown_email(settings, subject=subject, markdown_body=markdown):
            emailed_any = True

    return {
        "status": "reported",
        "new_releases": [format_release_label(b.release_id) for b in batches],
        "emailed": emailed_any,
        "report_paths": report_paths,
    }


def run_digest(
    settings: Settings,
    *,
    dry_run: bool = False,
    provider: str | None = None,
    model: str | None = None,
) -> dict:
    report_day = date.today()
    news_state = load_news_state(settings.state_dir)
    errors: list[str] = []
    releases = fetch_all(
        report_day,
        selected_sources=["news_rss"],
        errors=errors,
        extract_content=not dry_run,
    )
    for err in errors:
        logger.warning("news source warning: %s", err)

    fresh = [r for r in releases if not news_state.has(r.url)][: settings.max_items]
    items = _analyze_items(fresh, settings, provider=provider, model=model) if fresh else []
    markdown = render_digest(report_date=report_day, items=items)
    emailed = False
    if not dry_run:
        news_state.mark_many([item.release.url for item in items])
        save_news_state(settings.state_dir, news_state)
        emailed = send_markdown_email(
            settings,
            subject=f"UAP Signal Weekly News Digest — {report_day.isoformat()}",
            markdown_body=markdown,
        )
    return {
        "status": "digest",
        "item_count": len(items),
        "emailed": emailed,
        "markdown": markdown,
    }


def send_existing_report(settings: Settings, path: Path) -> bool:
    markdown = path.read_text(encoding="utf-8")
    subject = subject_from_markdown_path(path)
    return send_markdown_email(settings, subject=subject, markdown_body=markdown)


def backfill_existing_reports(settings: Settings, reports_dir: str | Path | None = None) -> list[str]:
    directory = Path(reports_dir or settings.reports_dir)
    paths = sorted(directory.glob("*-pursue-release-*-report.md"))
    sent: list[str] = []
    for path in paths:
        if send_existing_report(settings, path):
            sent.append(str(path))
    return sent
