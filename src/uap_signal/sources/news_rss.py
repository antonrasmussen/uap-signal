"""Google News RSS source fetcher."""

from __future__ import annotations

from datetime import date
from urllib.parse import quote_plus

import feedparser
import trafilatura

from uap_signal.http import get_text
from uap_signal.models import ContentType, Release, SourceTrust

QUERY = (
    "UAP OR UFO OR USO OR Pentagon UFO OR declassified UAP OR AARO OR "
    "all-domain anomaly resolution"
)


def _rss_url() -> str:
    return f"https://news.google.com/rss/search?q={quote_plus(QUERY)}&hl=en-US&gl=US&ceid=US:en"


def _extract_url(entry: dict) -> str:
    return entry.get("link", "")


def fetch(target_date: date, extract_content: bool = True) -> list[Release]:
    parsed = feedparser.parse(_rss_url())
    releases: list[Release] = []
    for entry in parsed.entries[:50]:
        url = _extract_url(entry)
        if not url:
            continue
        title = entry.get("title", "Untitled news item")
        raw_text = None
        if extract_content:
            try:
                html = get_text(url)
                raw_text = trafilatura.extract(html, include_comments=False, include_tables=False)
            except Exception:
                raw_text = entry.get("summary", "")
        else:
            raw_text = entry.get("summary", "")

        releases.append(
            Release(
                url=url,
                title=title,
                source_name="news_rss",
                source_trust=SourceTrust.MAJOR_NEWS,
                content_type=ContentType.RSS_ENTRY,
                first_seen_date=target_date.isoformat(),
                published_date=entry.get("published"),
                raw_text=raw_text,
                metadata={"publisher": entry.get("source", {}).get("title")},
            )
        )
    return releases
