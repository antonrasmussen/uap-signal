from datetime import date

from typer.testing import CliRunner

from uap_signal import cli
from uap_signal.models import ContentType, Release, SourceTrust


def test_check_dry_run_does_not_open_store(monkeypatch):
    runner = CliRunner()

    def fake_fetch_all(target_date: date, selected_sources=None, errors=None, extract_content=True):
        assert selected_sources is None
        assert extract_content is False
        if errors is not None:
            errors.append("news_rss: RuntimeError: unavailable")
        return [
            Release(
                url="https://example.gov/doc.pdf",
                title="Document",
                source_name="war_gov",
                source_trust=SourceTrust.OFFICIAL,
                content_type=ContentType.PDF,
                first_seen_date=target_date.isoformat(),
            )
        ]

    class FailingStore:
        def __init__(self, _db_path: str) -> None:
            raise AssertionError("dry-run should not open the database")

    monkeypatch.setattr(cli, "fetch_all", fake_fetch_all)
    monkeypatch.setattr(cli, "Store", FailingStore)

    result = runner.invoke(cli.app, ["check", "--dry-run"])

    assert result.exit_code == 0
    assert "Dry run" in result.stdout
    assert "Source warnings" in result.stdout
