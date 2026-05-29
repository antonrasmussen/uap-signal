"""SQLite persistence for releases and analyses."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Iterable

from uap_signal.models import AnalysisResult, Release


class Store:
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(db_path)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA foreign_keys = ON")
        self._init_schema()

    def __enter__(self) -> Store:
        return self

    def __exit__(self, *_exc_info: object) -> None:
        self.close()

    def close(self) -> None:
        self._conn.close()

    def _init_schema(self) -> None:
        self._conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS releases (
                url TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                source_name TEXT NOT NULL,
                source_trust TEXT NOT NULL,
                content_type TEXT NOT NULL,
                fetched_at TEXT NOT NULL,
                first_seen_date TEXT NOT NULL,
                published_date TEXT,
                raw_text TEXT,
                content_hash TEXT,
                metadata_json TEXT
            );

            CREATE INDEX IF NOT EXISTS idx_releases_first_seen ON releases(first_seen_date);
            CREATE INDEX IF NOT EXISTS idx_releases_content_hash ON releases(content_hash);

            CREATE TABLE IF NOT EXISTS analyses (
                release_url TEXT PRIMARY KEY,
                classification TEXT NOT NULL,
                summary TEXT NOT NULL,
                why_it_matters TEXT,
                novelty_score INTEGER NOT NULL,
                source_credibility TEXT NOT NULL,
                analyzed_at TEXT NOT NULL,
                model_used TEXT,
                content_hash TEXT,
                reasoning TEXT,
                FOREIGN KEY(release_url) REFERENCES releases(url)
            );
            """
        )
        self._conn.commit()

    def save_releases(self, releases: Iterable[Release]) -> None:
        rows = [
            (
                r.url,
                r.title,
                r.source_name,
                r.source_trust.value,
                r.content_type.value,
                r.fetched_at.isoformat(),
                r.first_seen_date,
                r.published_date,
                r.raw_text,
                r.content_hash,
                json.dumps(r.metadata),
            )
            for r in releases
        ]
        self._conn.executemany(
            """
            INSERT INTO releases
            (url, title, source_name, source_trust, content_type, fetched_at, first_seen_date, published_date, raw_text, content_hash, metadata_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(url) DO UPDATE SET
                title=excluded.title,
                source_name=excluded.source_name,
                source_trust=excluded.source_trust,
                content_type=excluded.content_type,
                fetched_at=excluded.fetched_at,
                published_date=COALESCE(excluded.published_date, releases.published_date),
                raw_text=COALESCE(excluded.raw_text, releases.raw_text),
                content_hash=COALESCE(excluded.content_hash, releases.content_hash),
                metadata_json=excluded.metadata_json
            """,
            rows,
        )
        self._conn.commit()

    def save_analysis(self, result: AnalysisResult) -> None:
        self._conn.execute(
            """
            INSERT INTO analyses
            (release_url, classification, summary, why_it_matters, novelty_score, source_credibility, analyzed_at, model_used, content_hash, reasoning)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(release_url) DO UPDATE SET
                classification=excluded.classification,
                summary=excluded.summary,
                why_it_matters=excluded.why_it_matters,
                novelty_score=excluded.novelty_score,
                source_credibility=excluded.source_credibility,
                analyzed_at=excluded.analyzed_at,
                model_used=excluded.model_used,
                content_hash=excluded.content_hash,
                reasoning=excluded.reasoning
            """,
            (
                result.release_url,
                result.classification.value,
                result.summary,
                result.why_it_matters,
                result.novelty_score,
                result.source_credibility.value,
                result.analyzed_at.isoformat(),
                result.model_used,
                result.content_hash,
                result.reasoning,
            ),
        )
        self._conn.commit()

    def get_analysis_by_hash(self, content_hash: str | None) -> sqlite3.Row | None:
        if not content_hash:
            return None
        return self._conn.execute(
            "SELECT * FROM analyses WHERE content_hash = ? ORDER BY analyzed_at DESC LIMIT 1",
            (content_hash,),
        ).fetchone()

    def get_recent_releases(self, days: int = 7) -> list[sqlite3.Row]:
        return self._conn.execute(
            """
            SELECT r.*, a.classification, a.summary, a.novelty_score
            FROM releases r
            LEFT JOIN analyses a ON a.release_url = r.url
            WHERE date(r.first_seen_date) >= date('now', ?)
            ORDER BY r.first_seen_date DESC, r.fetched_at DESC
            """,
            (f"-{days} day",),
        ).fetchall()

    def get_source_stats(self) -> list[sqlite3.Row]:
        return self._conn.execute(
            """
            SELECT source_name, COUNT(*) AS item_count, MAX(fetched_at) AS last_seen
            FROM releases
            GROUP BY source_name
            ORDER BY item_count DESC
            """
        ).fetchall()

    def get_text_corpus_by_source(self, source_name: str) -> list[str]:
        rows = self._conn.execute(
            "SELECT raw_text FROM releases WHERE source_name = ? AND raw_text IS NOT NULL",
            (source_name,),
        ).fetchall()
        return [row["raw_text"] for row in rows if row["raw_text"]]
