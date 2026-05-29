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


def fetch(target_date: date, extract_content: bool = True) -> list[Release]:
    del extract_content
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

        title_cell = cols[2]
        title_a = title_cell.find("a")
        title = (title_a.get_text(strip=True) if title_a else title_cell.get_text(strip=True))
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

        if link and "dvidshub.net" in link:
            content_type = ContentType.VIDEO
        elif link and link.endswith(".pdf"):
            content_type = ContentType.PDF
        else:
            content_type = ContentType.HTML

        agencies_offical = {"DoD", "DoW", "CIA", "NASA", "FBI", "ODNI", "DOE", "State"}
        is_official = any(agency.upper().startswith(a) for a in {a.upper() for a in agencies_offical})

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
                },
            )
        )

    return releases
