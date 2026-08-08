from datetime import date

from uap_signal.models import ContentType, Release, SourceTrust
from uap_signal.release_watch import detect_new_releases, group_by_release, infer_release_date
from uap_signal.state import ReleaseState

FAKE_HTML = """
<html><body><table>
<tr><th>#</th><th>Agency</th><th>Title</th><th>Description</th><th>Date</th><th>Location</th><th>Link</th></tr>
<tr data-release="04">
  <td>1</td><td>DoW</td>
  <td><a href="/d/1">DOW-UAP-D001</a></td>
  <td>Old item</td><td>2020</td><td>CONUS</td>
  <td><a href="https://www.war.gov/medialink/ufo/release_04/Jul_10/documents/a.pdf">pdf</a></td>
</tr>
<tr data-release="05">
  <td>2</td><td>FBI</td>
  <td><a href="/d/2">FBI-UAP-D032</a></td>
  <td>New item</td><td>2026</td><td>West</td>
  <td><a href="https://www.war.gov/medialink/ufo/release_05/Aug_07/documents/b.pdf">pdf</a></td>
</tr>
<tr data-release="05">
  <td>3</td><td>DoW</td>
  <td><a href="/d/3">DOW-UAP-PR117</a></td>
  <td>Video item</td><td>2021</td><td>Gulf</td>
  <td><a href="https://www.dvidshub.net/video/1">video</a></td>
</tr>
</table></body></html>
"""


def _release(url: str, rid: str, title: str = "Item") -> Release:
    return Release(
        url=url,
        title=title,
        source_name="warufo",
        source_trust=SourceTrust.OFFICIAL,
        content_type=ContentType.PDF,
        metadata={"data_release": rid, "agency": "DoW"},
    )


def test_group_by_release():
    items = [
        _release("https://a", "04"),
        _release("https://b", "05"),
        _release("https://c", "05"),
    ]
    grouped = group_by_release(items)
    assert set(grouped) == {"04", "05"}
    assert len(grouped["05"]) == 2


def test_infer_release_date_from_url():
    item = _release(
        "https://www.war.gov/medialink/ufo/release_05/Aug_07/documents/x.pdf",
        "05",
    )
    assert infer_release_date([item], fallback_year=2026) == date(2026, 8, 7)


def test_detect_new_releases(monkeypatch):
    from uap_signal.sources import warufo

    monkeypatch.setattr(warufo, "get_text", lambda url: FAKE_HTML)
    state = ReleaseState()
    state.mark("04", file_count=1, release_date="2026-07-10")

    new = detect_new_releases(state, target_date=date(2026, 8, 7))
    assert [b.release_id for b in new] == ["05"]
    assert new[0].file_count == 2
    assert new[0].release_date == date(2026, 8, 7)

    forced = detect_new_releases(state, force_release="4")
    assert len(forced) == 1
    assert forced[0].release_id == "04"
