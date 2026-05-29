"""war.gov/ufo source fetcher."""

from __future__ import annotations

import tempfile
from datetime import UTC, date, datetime
from urllib.parse import urljoin

import pdfplumber
from bs4 import BeautifulSoup

from uap_signal.http import get_bytes, get_text
from uap_signal.models import ContentType, Release, SourceTrust
from uap_signal.security import analyze_pdf_security, is_allowed_source_url

BASE_URL = "https://www.war.gov/ufo"


def _extract_pdf_text(pdf_bytes: bytes) -> str:
    with tempfile.NamedTemporaryFile(suffix=".pdf") as temp:
        temp.write(pdf_bytes)
        temp.flush()
        security_report = analyze_pdf_security(temp.name)
        if not security_report.passed:
            return ""
        chunks: list[str] = []
        with pdfplumber.open(temp.name) as doc:
            for page in doc.pages[:25]:
                chunks.append(page.extract_text() or "")
        return "\n".join(chunks).strip()


def fetch(target_date: date, extract_content: bool = True) -> list[Release]:
    html = get_text(BASE_URL)
    soup = BeautifulSoup(html, "html.parser")
    releases: list[Release] = []
    for anchor in soup.select("a[href]"):
        href = anchor.get("href", "")
        title = anchor.get_text(strip=True) or "Untitled war.gov item"
        if not href:
            continue
        full_url = urljoin(BASE_URL, href)
        if not full_url.lower().endswith(".pdf"):
            continue
        if not is_allowed_source_url(full_url):
            continue

        raw_text = None
        if extract_content:
            try:
                raw_text = _extract_pdf_text(get_bytes(full_url))
            except Exception:
                raw_text = None

        releases.append(
            Release(
                url=full_url,
                title=title,
                source_name="war_gov",
                source_trust=SourceTrust.OFFICIAL,
                content_type=ContentType.PDF,
                first_seen_date=target_date.isoformat(),
                published_date=datetime.now(UTC).date().isoformat(),
                raw_text=raw_text,
                metadata={"parent_url": BASE_URL},
            )
        )
    return releases
