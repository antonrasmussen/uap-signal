import pytest

from uap_signal.analyzer import AnalysisConfigurationError, _parse_json_response, summarize_release
from uap_signal.config import Settings
from uap_signal.models import AnalysisResult, Classification, ContentType, Release, SourceTrust
from uap_signal.store import Store


def _settings(provider: str = "anthropic", model: str = "test-model") -> Settings:
    return Settings(
        database_path=":memory:",
        provider=provider,
        anthropic_api_key=None,
        openai_api_key=None,
        model=model,
        max_items=25,
        request_timeout_seconds=30,
        email_provider="smtp",
        email_from="from@example.com",
        email_to="to@example.com",
        alert_email_to="",
        smtp_host="smtp.gmail.com",
        smtp_port=587,
        smtp_user="",
        smtp_password="",
        resend_api_key="",
        reports_dir="reports",
        state_dir="state",
    )


def _release() -> Release:
    return Release(
        url="https://example.gov/doc.pdf",
        title="Document",
        source_name="war_gov",
        source_trust=SourceTrust.OFFICIAL,
        content_type=ContentType.PDF,
        raw_text="Declassified UAP files.",
    )


def test_parse_json_response_falls_back_for_non_json():
    parsed = _parse_json_response("plain text response")
    assert parsed["summary"] == "plain text response"
    assert parsed["novelty_score"] == 5


def test_summarize_release_requires_provider_api_key(tmp_path):
    release = _release()
    with Store(str(tmp_path / "uap.db")) as store:
        store.save_releases([release])
        with pytest.raises(AnalysisConfigurationError, match="ANTHROPIC_API_KEY"):
            summarize_release(release, Classification.GENUINELY_NEW, _settings(), store)


def test_summarize_release_uses_cache_before_provider_validation(tmp_path):
    release = _release()
    with Store(str(tmp_path / "uap.db")) as store:
        store.save_releases([release])
        store.save_analysis(
            AnalysisResult(
                release_url=release.url,
                classification=Classification.GENUINELY_NEW,
                summary="Cached summary",
                novelty_score=7,
                source_credibility=SourceTrust.OFFICIAL,
                model_used="cached-model",
                content_hash=release.content_hash,
            )
        )

        result = summarize_release(release, Classification.CONTEXT, _settings(provider="openai"), store)

    assert result.summary == "Cached summary"
    assert result.classification == Classification.GENUINELY_NEW
    assert result.model_used == "cached-model"
