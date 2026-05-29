"""Rule-based source-trust classifier for novelty detection."""

from __future__ import annotations

import re
from difflib import SequenceMatcher

from uap_signal.models import Classification, Release, SourceTrust
from uap_signal.store import Store

META_PATTERNS = [
    r"\bwhat this means\b",
    r"\breaction\b",
    r"\bpolitics\b",
    r"\bpromise\b",
    r"\bimplications\b",
]

CORE_TERMS = [
    "uap",
    "ufo",
    "uso",
    "unidentified aerial",
    "unidentified anomalous",
    "aaro",
    "all-domain anomaly resolution",
    "declassified uap",
    "declassified ufo",
    "war.gov/ufo",
    "pentagon ufo",
    "dod uap",
    "non-human intelligence",
    "nhi",
    "uap disclosure",
    "ufo disclosure",
    "grusch",
    "kirkpatrick",
    "aoimsg",
    "uaptf",
]


def _looks_like_meta(text: str) -> bool:
    return any(re.search(pattern, text, flags=re.IGNORECASE) for pattern in META_PATTERNS)


def _is_rehash_against_corpus(text: str, corpus: list[str], threshold: float = 0.88) -> bool:
    sample = text[:4000]
    for old in corpus[-20:]:
        if SequenceMatcher(None, sample, old[:4000]).ratio() >= threshold:
            return True
    return False


def _contains_core_terms(text: str) -> bool:
    lowered = text.lower()
    return any(term in lowered for term in CORE_TERMS)


def classify_release(release: Release, store: Store | None = None) -> Classification:
    body = " ".join(filter(None, [release.title, release.raw_text or ""]))

    if release.source_trust == SourceTrust.OFFICIAL:
        return Classification.GENUINELY_NEW

    if release.source_trust == SourceTrust.MAJOR_NEWS:
        if _looks_like_meta(body):
            return Classification.META
        return Classification.CONTEXT

    if not _contains_core_terms(body):
        return Classification.SPECULATION

    if store:
        corpus = store.get_text_corpus_by_source(release.source_name)
        if release.raw_text and _is_rehash_against_corpus(release.raw_text, corpus):
            return Classification.REHASH

    if _looks_like_meta(body):
        return Classification.META

    return Classification.SPECULATION
