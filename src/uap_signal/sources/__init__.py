"""Source orchestrator and registry."""

from __future__ import annotations

from collections.abc import Callable
from datetime import date

from uap_signal.models import Release

SourceFetcher = Callable[[date, bool], list[Release]]


def _war_gov_fetch(target_date: date, extract_content: bool = True) -> list[Release]:
    from uap_signal.sources import war_gov

    return war_gov.fetch(target_date, extract_content=extract_content)


def _news_rss_fetch(target_date: date, extract_content: bool = True) -> list[Release]:
    from uap_signal.sources import news_rss

    return news_rss.fetch(target_date, extract_content=extract_content)


def _black_vault_fetch(target_date: date, extract_content: bool = True) -> list[Release]:
    from uap_signal.sources import black_vault

    return black_vault.fetch(target_date, extract_content=extract_content)


def _aaro_fetch(target_date: date, extract_content: bool = True) -> list[Release]:
    from uap_signal.sources import aaro

    return aaro.fetch(target_date, extract_content=extract_content)


def _congress_fetch(target_date: date, extract_content: bool = True) -> list[Release]:
    from uap_signal.sources import congress

    return congress.fetch(target_date, extract_content=extract_content)


SOURCE_REGISTRY = {
    "war_gov": _war_gov_fetch,
    "news_rss": _news_rss_fetch,
    "black_vault": _black_vault_fetch,
    "aaro": _aaro_fetch,
    "congress": _congress_fetch,
}


def fetch_all(
    target_date: date,
    selected_sources: list[str] | None = None,
    errors: list[str] | None = None,
    extract_content: bool = True,
) -> list[Release]:
    names = selected_sources or ["war_gov", "news_rss"]
    unknown = sorted(set(names) - set(SOURCE_REGISTRY))
    if unknown:
        supported = ", ".join(sorted(SOURCE_REGISTRY))
        raise ValueError(f"Unknown source(s): {', '.join(unknown)}. Supported sources: {supported}.")

    releases: list[Release] = []
    for name in names:
        fetcher = SOURCE_REGISTRY[name]
        try:
            releases.extend(fetcher(target_date, extract_content))
        except Exception as exc:
            if errors is not None:
                errors.append(f"{name}: {type(exc).__name__}: {exc}")
            continue
    return releases
