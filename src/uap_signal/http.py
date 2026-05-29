"""HTTP utilities with retries and sane defaults."""

from __future__ import annotations

import httpx

DEFAULT_HEADERS = {
    "User-Agent": "uap-signal/0.1 (+https://example.local)",
}


def get_text(url: str, timeout_seconds: int = 30) -> str:
    last_error: Exception | None = None
    for _attempt in range(3):
        try:
            with httpx.Client(timeout=timeout_seconds, headers=DEFAULT_HEADERS, follow_redirects=True) as client:
                response = client.get(url)
                response.raise_for_status()
                return response.text
        except httpx.HTTPError as exc:
            last_error = exc
    assert last_error is not None
    raise last_error


def get_bytes(url: str, timeout_seconds: int = 30) -> bytes:
    last_error: Exception | None = None
    for _attempt in range(3):
        try:
            with httpx.Client(timeout=timeout_seconds, headers=DEFAULT_HEADERS, follow_redirects=True) as client:
                response = client.get(url)
                response.raise_for_status()
                return response.content
        except httpx.HTTPError as exc:
            last_error = exc
    assert last_error is not None
    raise last_error
