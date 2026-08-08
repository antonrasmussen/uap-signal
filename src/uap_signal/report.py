"""Markdown report generation for PURSUE releases and news digests."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, select_autoescape

from uap_signal.models import AnalysisResult, Release
from uap_signal.state import ReleaseState

TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"

KNOWN_RELEASE_META = {
    "01": {"date": "2026-05-08", "files": 158, "character": "Broad multi-agency opener"},
    "02": {"date": "2026-05-22", "files": 64, "character": "Engagement / transmedium / intel testimony"},
    "03": {"date": "2026-06-12", "files": 72, "character": "FBI domestic + CIA Cold War"},
    "04": {"date": "2026-07-10", "files": 40, "character": "Unresolved IR mass + nuclear thread"},
    "05": {"date": "2026-08-07", "files": 41, "character": "Unresolved sensor + FBI triangles / 2026 cases"},
}


@dataclass
class Synthesis:
    executive_summary: str
    key_findings: list[str] = field(default_factory=list)
    character: str = ""
    next_steps: list[str] = field(default_factory=list)


@dataclass
class ReportItem:
    release: Release
    analysis: AnalysisResult

    @property
    def agency(self) -> str:
        return str((self.release.metadata or {}).get("agency") or self.release.source_name)

    @property
    def novelty(self) -> int:
        return int(self.analysis.novelty_score)


def _env() -> Environment:
    return Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=select_autoescape(enabled_extensions=()),
        trim_blocks=True,
        lstrip_blocks=True,
    )


def composition_stats(items: list[ReportItem]) -> dict[str, Any]:
    agencies = Counter(item.agency for item in items)
    types = Counter(item.release.content_type.value for item in items)
    scores = [item.novelty for item in items]
    avg = round(sum(scores) / len(scores), 2) if scores else 0.0
    return {
        "agencies": dict(agencies.most_common()),
        "types": dict(types.most_common()),
        "avg_novelty": avg,
        "count": len(items),
        "agency_summary": ", ".join(f"{name} ({count})" for name, count in agencies.most_common()),
        "type_summary": ", ".join(f"{name} ({count})" for name, count in types.most_common()),
    }


def group_by_novelty(items: list[ReportItem]) -> dict[str, list[ReportItem]]:
    top = [i for i in items if i.novelty >= 8]
    high = [i for i in items if 6 <= i.novelty <= 7]
    mid = [i for i in items if i.novelty <= 5]

    def sort_key(item: ReportItem) -> tuple[int, str]:
        return (-item.novelty, item.release.title.lower())

    return {
        "top": sorted(top, key=sort_key),
        "high": sorted(high, key=sort_key),
        "mid": sorted(mid, key=sort_key),
    }


def cross_release_rows(
    state: ReleaseState,
    current_id: str,
    current_date: str,
    current_count: int,
    character: str,
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    seen_ids = set(state.releases) | {current_id}
    for release_id in sorted(seen_ids):
        known = KNOWN_RELEASE_META.get(release_id, {})
        if release_id == current_id:
            rows.append(
                {
                    "id": release_id,
                    "date": current_date,
                    "files": str(current_count),
                    "character": character or known.get("character", "New PURSUE batch"),
                }
            )
            continue
        saved = state.releases.get(release_id)
        rows.append(
            {
                "id": release_id,
                "date": (saved.release_date if saved and saved.release_date else None)
                or known.get("date", "—"),
                "files": str(
                    (saved.file_count if saved else None) or known.get("files") or "—"
                ),
                "character": known.get("character", "Prior PURSUE batch"),
            }
        )
    return rows


def report_filename(release_id: str, report_date: date) -> str:
    rid = release_id.zfill(2) if release_id.isdigit() else release_id
    return f"{report_date.isoformat()}-pursue-release-{rid}-report.md"


def render_release_report(
    *,
    release_id: str,
    report_date: date,
    release_date: date | None,
    primary: list[ReportItem],
    news: list[ReportItem],
    synthesis: Synthesis,
    state: ReleaseState,
) -> str:
    rid = release_id.zfill(2) if release_id.isdigit() else release_id
    stats = composition_stats(primary)
    novelty_groups = group_by_novelty(primary)
    release_date_str = (release_date or report_date).isoformat()
    rows = cross_release_rows(
        state,
        current_id=rid,
        current_date=release_date_str,
        current_count=len(primary),
        character=synthesis.character,
    )
    cumulative = sum(int(r["files"]) for r in rows if str(r["files"]).isdigit())
    template = _env().get_template("report.md.j2")
    return template.render(
        release_id=rid,
        report_date=report_date.isoformat(),
        release_date=release_date_str,
        file_count=len(primary),
        cumulative=cumulative,
        synthesis=synthesis,
        stats=stats,
        novelty_groups=novelty_groups,
        news=news,
        cross_release_rows=rows,
    )


def render_heartbeat(*, report_date: date, seen_releases: list[str], latest_release: str | None) -> str:
    template = _env().get_template("heartbeat.md.j2")
    return template.render(
        report_date=report_date.isoformat(),
        seen_releases=seen_releases,
        latest_release=latest_release,
    )


def render_digest(*, report_date: date, items: list[ReportItem]) -> str:
    template = _env().get_template("digest.md.j2")
    return template.render(
        report_date=report_date.isoformat(),
        items=sorted(items, key=lambda i: (-i.novelty, i.release.title.lower())),
        count=len(items),
        avg_novelty=round(sum(i.novelty for i in items) / len(items), 2) if items else 0,
    )


def write_report(path: Path, content: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


def subject_for_release(release_id: str, report_date: date) -> str:
    rid = release_id.zfill(2) if release_id.isdigit() else release_id
    return f"PURSUE Release {rid} — UAP Signal Report ({report_date.isoformat()})"


def subject_from_markdown_path(path: Path) -> str:
    name = path.stem
    # e.g. 2026-08-07-pursue-release-05-report
    parts = name.split("-")
    date_str = "-".join(parts[:3]) if len(parts) >= 3 else date.today().isoformat()
    release_id = "??"
    if "release" in parts:
        idx = parts.index("release")
        if idx + 1 < len(parts):
            release_id = parts[idx + 1]
    return f"PURSUE Release {release_id} — UAP Signal Report ({date_str})"
