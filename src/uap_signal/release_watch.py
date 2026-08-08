"""Detect new PURSUE release batches from the warufo archive."""

from __future__ import annotations

import re
from collections import defaultdict
from dataclasses import dataclass
from datetime import date, datetime
from typing import Iterable

from uap_signal.models import Release
from uap_signal.sources import warufo
from uap_signal.state import ReleaseState

_MONTHS = {
    "jan": 1,
    "january": 1,
    "feb": 2,
    "february": 2,
    "mar": 3,
    "march": 3,
    "apr": 4,
    "april": 4,
    "may": 5,
    "jun": 6,
    "june": 6,
    "jul": 7,
    "july": 7,
    "aug": 8,
    "august": 8,
    "sep": 9,
    "sept": 9,
    "september": 9,
    "oct": 10,
    "october": 10,
    "nov": 11,
    "november": 11,
    "dec": 12,
    "december": 12,
}

_RELEASE_PATH_RE = re.compile(
    r"release[_-]?(?P<rid>\d{1,2})/(?P<mon>[A-Za-z]+)[_-]?(?P<day>\d{1,2})",
    re.IGNORECASE,
)


@dataclass
class ReleaseBatch:
    release_id: str
    items: list[Release]
    release_date: date | None = None

    @property
    def file_count(self) -> int:
        return len(self.items)


def infer_release_date(items: Iterable[Release], fallback_year: int | None = None) -> date | None:
    year = fallback_year or date.today().year
    for item in items:
        candidates = [item.url, str((item.metadata or {}).get("detail_page") or "")]
        for candidate in candidates:
            match = _RELEASE_PATH_RE.search(candidate or "")
            if not match:
                continue
            month = _MONTHS.get(match.group("mon").lower())
            day = int(match.group("day"))
            if not month:
                continue
            try:
                return date(year, month, day)
            except ValueError:
                continue
    return None


def group_by_release(items: Iterable[Release]) -> dict[str, list[Release]]:
    grouped: dict[str, list[Release]] = defaultdict(list)
    for item in items:
        release_id = (item.metadata or {}).get("data_release")
        if not release_id:
            continue
        grouped[str(release_id)].append(item)
    return dict(sorted(grouped.items()))


def fetch_archive_batches(target_date: date | None = None) -> dict[str, ReleaseBatch]:
    target = target_date or date.today()
    items = warufo.fetch(target, extract_content=False)
    batches: dict[str, ReleaseBatch] = {}
    for release_id, group in group_by_release(items).items():
        batches[release_id] = ReleaseBatch(
            release_id=release_id,
            items=group,
            release_date=infer_release_date(group, fallback_year=target.year),
        )
    return batches


def detect_new_releases(
    state: ReleaseState,
    *,
    target_date: date | None = None,
    force_release: str | None = None,
) -> list[ReleaseBatch]:
    batches = fetch_archive_batches(target_date)
    if force_release:
        rid = force_release.zfill(2) if force_release.isdigit() else force_release
        batch = batches.get(rid)
        return [batch] if batch else []

    new_batches: list[ReleaseBatch] = []
    for release_id, batch in batches.items():
        if not state.has(release_id):
            new_batches.append(batch)
    return new_batches


def format_release_label(release_id: str) -> str:
    return release_id.zfill(2) if release_id.isdigit() else release_id


def iso_now() -> str:
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
