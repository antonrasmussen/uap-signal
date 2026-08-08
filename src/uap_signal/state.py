"""Persistent JSON state for release watching and news digests."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class SeenRelease:
    release_id: str
    file_count: int
    release_date: str | None = None
    report_path: str | None = None
    first_seen_at: str | None = None


@dataclass
class ReleaseState:
    releases: dict[str, SeenRelease] = field(default_factory=dict)

    def has(self, release_id: str) -> bool:
        return release_id in self.releases

    def mark(
        self,
        release_id: str,
        *,
        file_count: int,
        release_date: str | None = None,
        report_path: str | None = None,
        first_seen_at: str | None = None,
    ) -> None:
        existing = self.releases.get(release_id)
        self.releases[release_id] = SeenRelease(
            release_id=release_id,
            file_count=file_count,
            release_date=release_date or (existing.release_date if existing else None),
            report_path=report_path or (existing.report_path if existing else None),
            first_seen_at=first_seen_at or (existing.first_seen_at if existing else None),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "releases": {
                release_id: asdict(seen)
                for release_id, seen in sorted(self.releases.items())
            }
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any] | None) -> ReleaseState:
        state = cls()
        if not payload:
            return state
        for release_id, raw in (payload.get("releases") or {}).items():
            state.releases[release_id] = SeenRelease(
                release_id=raw.get("release_id", release_id),
                file_count=int(raw.get("file_count", 0)),
                release_date=raw.get("release_date"),
                report_path=raw.get("report_path"),
                first_seen_at=raw.get("first_seen_at"),
            )
        return state


@dataclass
class NewsState:
    urls: set[str] = field(default_factory=set)

    def has(self, url: str) -> bool:
        return url in self.urls

    def mark_many(self, urls: list[str]) -> None:
        self.urls.update(urls)

    def to_dict(self) -> dict[str, Any]:
        return {"urls": sorted(self.urls)}

    @classmethod
    def from_dict(cls, payload: dict[str, Any] | None) -> NewsState:
        if not payload:
            return cls()
        return cls(urls=set(payload.get("urls") or []))


def _read_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def releases_path(state_dir: str | Path) -> Path:
    return Path(state_dir) / "releases.json"


def news_path(state_dir: str | Path) -> Path:
    return Path(state_dir) / "seen_news.json"


def load_release_state(state_dir: str | Path) -> ReleaseState:
    return ReleaseState.from_dict(_read_json(releases_path(state_dir)))


def save_release_state(state_dir: str | Path, state: ReleaseState) -> None:
    _write_json(releases_path(state_dir), state.to_dict())


def load_news_state(state_dir: str | Path) -> NewsState:
    return NewsState.from_dict(_read_json(news_path(state_dir)))


def save_news_state(state_dir: str | Path, state: NewsState) -> None:
    _write_json(news_path(state_dir), state.to_dict())
