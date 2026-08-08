from uap_signal.state import (
    NewsState,
    ReleaseState,
    load_news_state,
    load_release_state,
    save_news_state,
    save_release_state,
)


def test_release_state_round_trip(tmp_path):
    state = ReleaseState()
    assert not state.has("05")
    state.mark(
        "05",
        file_count=41,
        release_date="2026-08-07",
        report_path="reports/2026-08-07-pursue-release-05-report.md",
        first_seen_at="2026-08-07T00:00:00Z",
    )
    save_release_state(tmp_path, state)

    loaded = load_release_state(tmp_path)
    assert loaded.has("05")
    assert loaded.releases["05"].file_count == 41
    assert loaded.releases["05"].report_path.endswith("05-report.md")


def test_release_state_empty_when_missing(tmp_path):
    loaded = load_release_state(tmp_path)
    assert loaded.releases == {}


def test_news_state_mark_and_persist(tmp_path):
    state = NewsState()
    state.mark_many(["https://a.example/1", "https://b.example/2"])
    save_news_state(tmp_path, state)

    loaded = load_news_state(tmp_path)
    assert loaded.has("https://a.example/1")
    assert loaded.has("https://b.example/2")
    assert not loaded.has("https://c.example/3")

    # Idempotent re-mark
    loaded.mark_many(["https://a.example/1"])
    save_news_state(tmp_path, loaded)
    again = load_news_state(tmp_path)
    assert again.urls == {"https://a.example/1", "https://b.example/2"}
