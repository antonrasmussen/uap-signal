"""Congress.gov source via official API (v1)."""

from __future__ import annotations

import os
from datetime import date

import httpx

from uap_signal.models import ContentType, Release, SourceTrust

API_URL = "https://api.congress.gov/v3/bill"


def fetch(target_date: date, extract_content: bool = True) -> list[Release]:
    del extract_content
    api_key = os.getenv("CONGRESS_API_KEY")
    if not api_key:
        return []

    params = {"api_key": api_key, "format": "json", "limit": 50}
    response = httpx.get(API_URL, params=params, timeout=30)
    response.raise_for_status()
    payload = response.json()
    releases: list[Release] = []
    for item in payload.get("bills", []):
        title = item.get("title", "")
        if "uap" not in title.lower() and "ufo" not in title.lower():
            continue
        url = item.get("url") or f"https://www.congress.gov/bill/{item.get('congress')}-congress/{item.get('type')}-bill/{item.get('number')}"
        releases.append(
            Release(
                url=url,
                title=title,
                source_name="congress",
                source_trust=SourceTrust.OFFICIAL,
                content_type=ContentType.API_ENTRY,
                first_seen_date=target_date.isoformat(),
                published_date=item.get("latestAction", {}).get("actionDate"),
                raw_text=item.get("latestAction", {}).get("text"),
            )
        )
    return releases
