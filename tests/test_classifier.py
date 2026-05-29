from uap_signal.classifier import classify_release
from uap_signal.models import Classification, ContentType, Release, SourceTrust


def test_official_source_is_genuinely_new():
    release = Release(
        url="https://www.war.gov/ufo/doc1.pdf",
        title="DoD tranche 1",
        source_name="war_gov",
        source_trust=SourceTrust.OFFICIAL,
        content_type=ContentType.PDF,
        raw_text="Declassified UAP files.",
    )
    assert classify_release(release) == Classification.GENUINELY_NEW


def test_major_news_meta_is_meta():
    release = Release(
        url="https://example.com/reaction",
        title="Reaction: what this means for UAP disclosure",
        source_name="news_rss",
        source_trust=SourceTrust.MAJOR_NEWS,
        content_type=ContentType.RSS_ENTRY,
        raw_text="Political reaction and implications.",
    )
    assert classify_release(release) == Classification.META


def test_major_news_non_meta_is_context():
    release = Release(
        url="https://example.com/report",
        title="Pentagon UFO report released",
        source_name="news_rss",
        source_trust=SourceTrust.MAJOR_NEWS,
        content_type=ContentType.RSS_ENTRY,
        raw_text="A report about a new UAP document.",
    )
    assert classify_release(release) == Classification.CONTEXT


def test_independent_without_core_terms_is_speculation():
    release = Release(
        url="https://example.com/blog",
        title="Strange lights over town",
        source_name="blog",
        source_trust=SourceTrust.INDEPENDENT,
        content_type=ContentType.HTML,
        raw_text="No official terminology here.",
    )
    assert classify_release(release) == Classification.SPECULATION


def test_independent_repeated_text_is_rehash():
    class FakeStore:
        def get_text_corpus_by_source(self, source_name: str) -> list[str]:
            assert source_name == "blog"
            return ["UAP disclosure " * 500]

    release = Release(
        url="https://example.com/rehash",
        title="UAP disclosure update",
        source_name="blog",
        source_trust=SourceTrust.INDEPENDENT,
        content_type=ContentType.HTML,
        raw_text="UAP disclosure " * 500,
    )
    assert classify_release(release, store=FakeStore()) == Classification.REHASH
