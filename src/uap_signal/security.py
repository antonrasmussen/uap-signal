"""Security controls for source trust and PDF safety checks."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import urlparse

from pypdf import PdfReader

MAX_PDF_SIZE_BYTES = 25 * 1024 * 1024  # 25MB
MAX_PDF_PAGES = 1500

# Conservative defaults: only government/official domains.
ALLOWED_DOMAINS = {
    "war.gov",
    "aaro.mil",
    "congress.gov",
    "api.congress.gov",
    "odni.gov",
    "defense.gov",
}

ALLOWED_SUFFIXES = (
    ".gov",
    ".mil",
)


@dataclass
class PdfSecurityReport:
    file_path: str
    file_size_bytes: int
    sha256: str
    passed: bool
    risk_level: str
    flags: list[str] = field(default_factory=list)
    page_count: int = 0


def is_allowed_source_url(url: str) -> bool:
    """Allowlist check for fetchable sources."""
    parsed = urlparse(url)
    if parsed.scheme not in {"https"}:
        return False
    host = (parsed.hostname or "").lower()
    if not host:
        return False
    if host in ALLOWED_DOMAINS:
        return True
    return any(host.endswith(suffix) for suffix in ALLOWED_SUFFIXES)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def analyze_pdf_security(path: str) -> PdfSecurityReport:
    """
    Run obvious-risk checks before PDF content extraction.

    This is not a full malware sandbox, but it catches common high-risk traits.
    """
    pdf_path = Path(path)
    flags: list[str] = []

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file does not exist: {path}")
    if not pdf_path.is_file():
        raise ValueError(f"Path is not a file: {path}")

    file_size = pdf_path.stat().st_size
    if file_size > MAX_PDF_SIZE_BYTES:
        flags.append(f"oversized_file>{MAX_PDF_SIZE_BYTES}B")

    # Lightweight magic header check.
    with pdf_path.open("rb") as f:
        header = f.read(5)
    if header != b"%PDF-":
        flags.append("invalid_pdf_header")

    page_count = 0
    try:
        reader = PdfReader(str(pdf_path), strict=False)
        page_count = len(reader.pages)
        if page_count > MAX_PDF_PAGES:
            flags.append(f"excessive_page_count>{MAX_PDF_PAGES}")

        if reader.is_encrypted:
            flags.append("encrypted_pdf")

        root = reader.trailer.get("/Root")
        if root:
            if root.get("/OpenAction") is not None:
                flags.append("has_open_action")
            names = root.get("/Names")
            if names and names.get("/JavaScript") is not None:
                flags.append("has_embedded_javascript")
            if names and names.get("/EmbeddedFiles") is not None:
                flags.append("has_embedded_files")
            if root.get("/AcroForm") is not None:
                flags.append("has_acroform")

    except Exception as exc:  # noqa: BLE001 - security check should fail closed
        flags.append(f"pdf_parse_error:{type(exc).__name__}")

    # Heuristic risk model
    high_risk_flags = (
        "has_embedded_javascript",
        "has_embedded_files",
        "has_open_action",
        "pdf_parse_error",
    )
    risk_level = "low"
    if any(flag.startswith(high_risk_flags) for flag in flags):
        risk_level = "high"
    elif flags:
        risk_level = "medium"

    passed = risk_level in {"low", "medium"} and "invalid_pdf_header" not in flags

    return PdfSecurityReport(
        file_path=str(pdf_path),
        file_size_bytes=file_size,
        sha256=_sha256(pdf_path),
        passed=passed,
        risk_level=risk_level,
        flags=flags,
        page_count=page_count,
    )
