"""AARO source fetcher (v1)."""

from __future__ import annotations

from datetime import date
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from uap_signal.http import get_text
from uap_signal.models import ContentType, Release, SourceTrust

BASE_URL = "https://www.aaro.mil/"


def fetch(target_date: date, extract_content: bool = True) -> list[Release]:
    del extract_content
    html = get_text(BASE_URL)
    soup = BeautifulSoup(html, "html.parser")
    releases: list[Release] = []
    for anchor in soup.select("a[href]")[:50]:
        href = anchor.get("href", "")
        title = anchor.get_text(strip=True)
        if not href or not title:
            continue
        full_url = urljoin(BASE_URL, href)
        if "uap" not in full_url.lower() and "anomaly" not in full_url.lower():
            continue
        releases.append(
            Release(
                url=full_url,
                title=title,
                source_name="aaro",
                source_trust=SourceTrust.OFFICIAL,
                content_type=ContentType.HTML,
                first_seen_date=target_date.isoformat(),
                metadata={"parent_url": BASE_URL},
            )
        )
    return releases
