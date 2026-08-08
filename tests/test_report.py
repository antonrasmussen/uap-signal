from datetime import date
from pathlib import Path

from uap_signal.models import AnalysisResult, Classification, ContentType, Release, SourceTrust
from uap_signal.report import (
    ReportItem,
    Synthesis,
    composition_stats,
    group_by_novelty,
    render_digest,
    render_heartbeat,
    render_release_report,
    subject_from_markdown_path,
)
from uap_signal.state import ReleaseState


def _item(title: str, novelty: int, agency: str = "DoW") -> ReportItem:
    release = Release(
        url=f"https://example.gov/{title}",
        title=title,
        source_name="warufo",
        source_trust=SourceTrust.OFFICIAL,
        content_type=ContentType.PDF,
        metadata={"agency": agency, "data_release": "05"},
    )
    analysis = AnalysisResult(
        release_url=release.url,
        classification=Classification.GENUINELY_NEW,
        summary=f"Summary for {title}",
        why_it_matters="Why it matters",
        novelty_score=novelty,
    )
    return ReportItem(release=release, analysis=analysis)


def test_composition_and_novelty_grouping():
    items = [
        _item("Top A", 8, "FBI"),
        _item("High B", 7, "DoW"),
        _item("Mid C", 4, "CIA"),
    ]
    stats = composition_stats(items)
    assert stats["count"] == 3
    assert stats["agencies"]["FBI"] == 1
    groups = group_by_novelty(items)
    assert [i.release.title for i in groups["top"]] == ["Top A"]
    assert [i.release.title for i in groups["high"]] == ["High B"]
    assert [i.release.title for i in groups["mid"]] == ["Mid C"]


def test_render_release_report_contains_sections():
    state = ReleaseState()
    state.mark("04", file_count=40, release_date="2026-07-10")
    markdown = render_release_report(
        release_id="05",
        report_date=date(2026, 8, 7),
        release_date=date(2026, 8, 7),
        primary=[_item("FBI-UAP-D032", 8, "FBI"), _item("DOW-UAP-PR117", 7)],
        news=[_item("CBS covers release", 6, "news_rss")],
        synthesis=Synthesis(
            executive_summary="Release 05 dropped today with FBI and DoW items.",
            key_findings=["Finding one", "Finding two", "Finding three"],
            character="Unresolved sensor + FBI triangles",
            next_steps=["Watch Gulf of Oman videos"],
        ),
        state=state,
    )
    assert "# PURSUE Release 05 — UAP Signal Intelligence Report" in markdown
    assert "## Executive Summary" in markdown
    assert "## Methodology" in markdown
    assert "## Release 05: Primary Document Analysis" in markdown
    assert "## News Cycle" in markdown
    assert "## Cross-Release Comparison" in markdown
    assert "FBI-UAP-D032" in markdown
    assert "Finding one" in markdown


def test_render_heartbeat_and_digest():
    heartbeat = render_heartbeat(
        report_date=date(2026, 8, 8),
        seen_releases=["01", "02", "05"],
        latest_release="05",
    )
    assert "No new PURSUE release detected today" in heartbeat
    digest = render_digest(report_date=date(2026, 8, 11), items=[_item("News item", 7)])
    assert "Weekly News Digest" in digest
    assert "News item" in digest


def test_subject_from_markdown_path():
    path = Path("reports/2026-08-07-pursue-release-05-report.md")
    assert subject_from_markdown_path(path) == "PURSUE Release 05 — UAP Signal Report (2026-08-07)"
