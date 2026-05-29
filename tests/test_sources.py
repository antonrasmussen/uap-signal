from datetime import date

import pytest

from uap_signal.models import ContentType, Release, SourceTrust
from uap_signal.sources import SOURCE_REGISTRY, fetch_all


def test_sources_registered():
    for name in ("war_gov", "warufo", "news_rss", "black_vault", "aaro", "congress"):
        assert name in SOURCE_REGISTRY


def test_fetchers_callable():
    for key in ("war_gov", "warufo", "news_rss"):
        assert callable(SOURCE_REGISTRY[key])


def test_warufo_parses_archive_table(monkeypatch):
    fake_html = """
    <html>
    <body>
    <table>
    <tr><th>#</th><th>Agency</th><th>Title</th><th>Description</th><th>Date</th><th>Location</th><th>Link</th></tr>
    <tr>
        <td>1</td>
        <td>DoW</td>
        <td><a href="/document/1">DOW-UAP-PR050, Four UAP Formation</a></td>
        <td>Eight members of Congress requested a briefing</td>
        <td>2022</td>
        <td>CENTCOM</td>
        <td><a href="https://www.dvidshub.net/video/1007706">▶</a></td>
    </tr>
    <tr>
        <td>2</td>
        <td>CIA</td>
        <td><a href="/document/2">CIA-UAP-D001, Intelligence Report</a></td>
        <td>Classified intelligence report from 1973</td>
        <td>12/20/73</td>
        <td>USSR</td>
        <td><a href="https://www.war.gov/medialink/ufo/doc.pdf">📄</a></td>
    </tr>
    </table>
    </body>
    </html>
    """

    from uap_signal.sources import warufo

    monkeypatch.setattr(warufo, "get_text", lambda url: fake_html)

    releases = warufo.fetch(date(2026, 5, 22), extract_content=False)
    assert len(releases) == 2

    r1 = releases[0]
    assert r1.title == "DOW-UAP-PR050, Four UAP Formation"
    assert r1.url == "https://www.dvidshub.net/video/1007706"
    assert r1.source_name == "warufo"
    assert r1.source_trust == SourceTrust.OFFICIAL
    assert r1.content_type == ContentType.VIDEO
    assert r1.metadata["agency"] == "DoW"
    assert r1.metadata["location"] == "CENTCOM"

    r2 = releases[1]
    assert r2.title == "CIA-UAP-D001, Intelligence Report"
    assert r2.url == "https://www.war.gov/medialink/ufo/doc.pdf"
    assert r2.content_type == ContentType.PDF


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
