"""Google News RSS source fetcher with article URL resolution.

Uses Google News RSS for discovery, then resolves the real article URL
via Google search and extracts full text with trafilatura.
"""

from __future__ import annotations

import re
import time
from datetime import date
from urllib.parse import parse_qs, quote_plus, urlparse

import feedparser
import trafilatura

from uap_signal.http import get_text
from uap_signal.models import ContentType, Release, SourceTrust

QUERY = (
    "UAP OR UFO OR USO OR Pentagon UFO OR declassified UAP OR AARO OR "
    "all-domain anomaly resolution"
)

BROWSER_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)


def _rss_url() -> str:
    return f"https://news.google.com/rss/search?q={quote_plus(QUERY)}&hl=en-US&gl=US&ceid=US:en"


def _resolve_real_url(title: str, source_domain: str) -> str | None:
    """Resolve the real article URL via Google 'I'm Feeling Lucky' search."""
    import httpx

    search_url = f"https://www.google.com/search?q=site:{source_domain}+{quote_plus(title)}&btnI"
    try:
        with httpx.Client(
            follow_redirects=True,
            headers={"User-Agent": BROWSER_UA},
            timeout=15,
        ) as client:
            resp = client.get(search_url)
        if resp.status_code != 200:
            return None

        final = str(resp.url)
        # Google wraps the real URL in /url?q=...
        parsed = urlparse(final)
        if parsed.path == "/url":
            qs = parse_qs(parsed.query)
            return qs.get("q", [None])[0]
        return final if final.startswith("http") else None
    except Exception:
        return None


def _extract_article_text(url: str) -> str | None:
    try:
        html = get_text(url)
        text = trafilatura.extract(html, include_comments=False, include_tables=False)
        return text.strip() if text else None
    except Exception:
        return None


def _extract_domain(source_url: str | None) -> str | None:
    if not source_url:
        return None
    parsed = urlparse(source_url)
    return parsed.netloc or None


def fetch(target_date: date, extract_content: bool = True) -> list[Release]:
    parsed = feedparser.parse(_rss_url())
    releases: list[Release] = []
    seen_real_urls: set[str] = set()

    for entry in parsed.entries:
        title = entry.get("title", "Untitled news item")
        summary_raw = entry.get("summary", "")
        summary_clean = re.sub(r"<[^>]+>", "", summary_raw).strip()
        source_domain = _extract_domain(entry.get("source", {}).get("href"))

        real_url = None
        full_text = summary_clean

        if source_domain:
            real_url = _resolve_real_url(title, source_domain)
            if real_url:
                if real_url in seen_real_urls:
                    continue
                seen_real_urls.add(real_url)
                if extract_content:
                    extracted = _extract_article_text(real_url)
                    if extracted and len(extracted) > len(full_text):
                        full_text = extracted
                    time.sleep(1.5)

        url = real_url or entry.get("link", "")
        if not url:
            continue

        releases.append(
            Release(
                url=url,
                title=title,
                source_name="news_rss",
                source_trust=SourceTrust.MAJOR_NEWS,
                content_type=ContentType.RSS_ENTRY,
                first_seen_date=target_date.isoformat(),
                published_date=entry.get("published"),
                raw_text=full_text,
                metadata={
                    "publisher": entry.get("source", {}).get("title"),
                    "google_rss_url": entry.get("link"),
                },
            )
        )

    return releases
