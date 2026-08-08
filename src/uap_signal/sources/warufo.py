"""WARUFO.com archive source fetcher.

Indexes the PURSUE declassified UAP document archive hosted at warufo.com,
which mirrors the official war.gov/ufo release catalog. The underlying
documents are official U.S. government records (DoD, CIA, NASA, etc.).
"""

from __future__ import annotations

from datetime import date

from bs4 import BeautifulSoup

from uap_signal.http import get_text
from uap_signal.models import ContentType, Release, SourceTrust

BASE_URL = "https://warufo.com"
ARCHIVE_URL = f"{BASE_URL}/archive"

_OFFICIAL_AGENCIES = {"DoD", "DoW", "CIA", "NASA", "FBI", "ODNI", "DOE", "State", "DoS", "EOP"}


def _normalize_release_id(value: str | None) -> str | None:
    if value is None:
        return None
    cleaned = value.strip()
    if not cleaned:
        return None
    if cleaned.isdigit():
        return cleaned.zfill(2)
    return cleaned


def _row_data_release(row) -> str | None:
    raw = row.get("data-release")
    if raw:
        return _normalize_release_id(str(raw))
    for child in row.find_all(True):
        child_raw = child.get("data-release")
        if child_raw:
            return _normalize_release_id(str(child_raw))
    return None


def _content_type_for_link(link: str | None) -> ContentType:
    if link and "dvidshub.net" in link:
        return ContentType.VIDEO
    if link and link.lower().endswith(".pdf"):
        return ContentType.PDF
    if link and link.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".webp")):
        return ContentType.IMAGE
    return ContentType.HTML


def fetch(
    target_date: date,
    extract_content: bool = True,
    release_filter: str | None = None,
) -> list[Release]:
    del extract_content
    wanted = _normalize_release_id(release_filter)
    html = get_text(ARCHIVE_URL)
    soup = BeautifulSoup(html, "html.parser")
    releases: list[Release] = []

    table = soup.find("table")
    if not table:
        return releases

    for row in table.find_all("tr")[1:]:
        cols = row.find_all("td")
        if len(cols) < 7:
            continue

        data_release = _row_data_release(row)
        if wanted and data_release != wanted:
            continue

        title_cell = cols[2]
        title_a = title_cell.find("a")
        title = title_a.get_text(strip=True) if title_a else title_cell.get_text(strip=True)
        if not title:
            continue

        detail_page = f'{BASE_URL}{title_a["href"]}' if title_a and title_a.get("href", "").startswith("/") else None

        link_cell = cols[6]
        link_a = link_cell.find("a")
        link = link_a.get("href", "").strip() if link_a else None
        url = link or detail_page or ""

        agency = cols[1].get_text(strip=True) if len(cols) > 1 else ""
        description = cols[3].get_text(strip=True) if len(cols) > 3 else ""
        incident_date = cols[4].get_text(strip=True) if len(cols) > 4 else ""
        location = cols[5].get_text(strip=True) if len(cols) > 5 else ""

        content_type = _content_type_for_link(link)
        is_official = any(agency.upper().startswith(a.upper()) for a in _OFFICIAL_AGENCIES) or agency.startswith(
            "Executive"
        )

        releases.append(
            Release(
                url=url,
                title=title,
                source_name="warufo",
                source_trust=SourceTrust.OFFICIAL if is_official else SourceTrust.INDEPENDENT,
                content_type=content_type,
                first_seen_date=target_date.isoformat(),
                published_date=incident_date if incident_date else None,
                raw_text=description,
                metadata={
                    "agency": agency,
                    "incident_date": incident_date,
                    "location": location,
                    "detail_page": detail_page,
                    "archive_url": ARCHIVE_URL,
                    "data_release": data_release,
                },
            )
        )

    return releases
