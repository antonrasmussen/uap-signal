from uap_signal.models import AnalysisResult, Classification, ContentType, Release, SourceTrust
from uap_signal.store import Store


def test_store_saves_releases_and_analysis(tmp_path):
    db_path = tmp_path / "uap.db"
    release = Release(
        url="https://example.gov/doc.pdf",
        title="Document",
        source_name="war_gov",
        source_trust=SourceTrust.OFFICIAL,
        content_type=ContentType.PDF,
        raw_text="Declassified UAP files.",
    )

    with Store(str(db_path)) as store:
        store.save_releases([release])
        store.save_analysis(
            AnalysisResult(
                release_url=release.url,
                classification=Classification.GENUINELY_NEW,
                summary="A new official document was released.",
                novelty_score=8,
                source_credibility=SourceTrust.OFFICIAL,
                model_used="test-model",
                content_hash=release.content_hash,
            )
        )

        cached = store.get_analysis_by_hash(release.content_hash)
        assert cached is not None
        assert cached["summary"] == "A new official document was released."

        recent = store.get_recent_releases(days=1)
        assert len(recent) == 1
        assert recent[0]["classification"] == Classification.GENUINELY_NEW.value

        stats = store.get_source_stats()
        assert stats[0]["source_name"] == "war_gov"
        assert stats[0]["item_count"] == 1


def test_store_preserves_first_seen_on_release_update(tmp_path):
    db_path = tmp_path / "uap.db"
    first = Release(
        url="https://example.gov/doc.pdf",
        title="Original",
        source_name="war_gov",
        source_trust=SourceTrust.OFFICIAL,
        content_type=ContentType.PDF,
        first_seen_date="2026-01-01",
    )
    second = Release(
        url=first.url,
        title="Updated",
        source_name="war_gov",
        source_trust=SourceTrust.OFFICIAL,
        content_type=ContentType.PDF,
        first_seen_date="2026-02-01",
    )

    with Store(str(db_path)) as store:
        store.save_releases([first])
        store.save_releases([second])
        rows = store.get_recent_releases(days=1000)

    assert rows[0]["title"] == "Updated"
    assert rows[0]["first_seen_date"] == "2026-01-01"
