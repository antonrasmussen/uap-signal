"""Data models for UAP Signal."""

from __future__ import annotations

import hashlib
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any, Optional


class Classification(str, Enum):
    GENUINELY_NEW = "GENUINELY_NEW"
    CONTEXT = "CONTEXT"
    REHASH = "REHASH"
    SPECULATION = "SPECULATION"
    META = "META"


class SourceTrust(str, Enum):
    OFFICIAL = "official"
    MAJOR_NEWS = "major_news"
    INDEPENDENT = "independent"
    UNKNOWN = "unknown"


class ContentType(str, Enum):
    PDF = "pdf"
    HTML = "html"
    VIDEO = "video"
    IMAGE = "image"
    RSS_ENTRY = "rss_entry"
    API_ENTRY = "api_entry"


@dataclass
class Release:
    """A single item fetched from a source."""

    url: str
    title: str
    source_name: str
    source_trust: SourceTrust
    content_type: ContentType
    fetched_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    first_seen_date: str = field(default_factory=lambda: datetime.now(UTC).date().isoformat())
    published_date: Optional[str] = None
    raw_text: Optional[str] = None
    content_hash: Optional[str] = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.raw_text and not self.content_hash:
            self.content_hash = hashlib.sha256(self.raw_text.encode("utf-8", errors="ignore")).hexdigest()

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["source_trust"] = self.source_trust.value
        payload["content_type"] = self.content_type.value
        payload["fetched_at"] = self.fetched_at.isoformat()
        return payload


@dataclass
class AnalysisResult:
    """Analysis output for a release."""

    release_url: str
    classification: Classification
    summary: str
    why_it_matters: Optional[str] = None
    novelty_score: int = 0
    source_credibility: SourceTrust = SourceTrust.UNKNOWN
    analyzed_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    model_used: Optional[str] = None
    content_hash: Optional[str] = None
    reasoning: Optional[str] = None

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["classification"] = self.classification.value
        payload["source_credibility"] = self.source_credibility.value
        payload["analyzed_at"] = self.analyzed_at.isoformat()
        return payload
