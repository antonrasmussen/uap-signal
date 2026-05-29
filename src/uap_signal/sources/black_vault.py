"""The Black Vault source fetcher (v1)."""

from __future__ import annotations

from datetime import date

from bs4 import BeautifulSoup

from uap_signal.http import get_text
from uap_signal.models import ContentType, Release, SourceTrust

BASE_URL = "https://www.theblackvault.com/documentarchive/"


def fetch(target_date: date, extract_content: bool = True) -> list[Release]:
    del extract_content
    html = get_text(BASE_URL)
    soup = BeautifulSoup(html, "html.parser")
    releases: list[Release] = []

    for anchor in soup.select("article a[href], h2 a[href]")[:25]:
        url = anchor.get("href", "")
        title = anchor.get_text(strip=True)
        if not url or not title:
            continue
        releases.append(
            Release(
                url=url,
                title=title,
                source_name="black_vault",
                source_trust=SourceTrust.INDEPENDENT,
                content_type=ContentType.HTML,
                first_seen_date=target_date.isoformat(),
                metadata={"parent_url": BASE_URL},
            )
        )
    return releases
