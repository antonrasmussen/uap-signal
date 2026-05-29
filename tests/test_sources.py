from datetime import date

import pytest

from uap_signal.models import ContentType, Release, SourceTrust
from uap_signal.sources import SOURCE_REGISTRY, fetch_all


def test_sources_registered():
    assert "war_gov" in SOURCE_REGISTRY
    assert "news_rss" in SOURCE_REGISTRY


def test_fetchers_callable():
    for key in ("war_gov", "news_rss"):
        assert callable(SOURCE_REGISTRY[key])


def test_fetch_all_rejects_unknown_source():
    with pytest.raises(ValueError, match="Unknown source"):
        fetch_all(date.today(), selected_sources=["missing"])


def test_fetch_all_reports_source_errors(monkeypatch):
    def failing_fetcher(_target_date: date, _extract_content: bool = True) -> list[Release]:
        raise RuntimeError("network down")

    monkeypatch.setitem(SOURCE_REGISTRY, "broken", failing_fetcher)
    errors: list[str] = []

    assert fetch_all(date.today(), selected_sources=["broken"], errors=errors) == []
    assert errors == ["broken: RuntimeError: network down"]


def test_fetch_all_passes_extract_content_flag(monkeypatch):
    seen_extract_content: list[bool] = []

    def fetcher(target_date: date, extract_content: bool = True) -> list[Release]:
        seen_extract_content.append(extract_content)
        return [
            Release(
                url="https://example.gov/doc",
                title="Example",
                source_name="example",
                source_trust=SourceTrust.OFFICIAL,
                content_type=ContentType.HTML,
                first_seen_date=target_date.isoformat(),
            )
        ]

    monkeypatch.setitem(SOURCE_REGISTRY, "example", fetcher)

    releases = fetch_all(date.today(), selected_sources=["example"], extract_content=False)

    assert len(releases) == 1
    assert seen_extract_content == [False]
