"""LLM summarization and scoring."""

from __future__ import annotations

import json

from uap_signal.config import DEFAULT_MODELS, Settings
from uap_signal.models import AnalysisResult, Classification, Release
from uap_signal.store import Store


class AnalysisConfigurationError(RuntimeError):
    """Raised when LLM provider configuration is invalid."""


PROMPT_TEMPLATE = """You are analyzing a UAP/UFO release item.
Return JSON with keys:
- summary (2-3 sentences)
- why_it_matters (string; keep short)
- novelty_score (integer 1-10)
- reasoning (short rationale)

Title: {title}
Source: {source_name}
Pre-classification: {classification}
Content:
{content}
"""


def _parse_json_response(text: str) -> dict:
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {
            "summary": text[:300],
            "why_it_matters": "",
            "novelty_score": 5,
            "reasoning": "Fallback parse path used.",
        }


def _resolve_provider_settings(
    settings: Settings,
    provider_override: str | None = None,
    model_override: str | None = None,
) -> tuple[str, str]:
    provider = (provider_override or settings.provider).lower()
    if provider not in DEFAULT_MODELS:
        supported = ", ".join(sorted(DEFAULT_MODELS))
        raise AnalysisConfigurationError(f"Unsupported provider '{provider}'. Supported providers: {supported}.")

    if provider == "anthropic" and not settings.anthropic_api_key:
        raise AnalysisConfigurationError("ANTHROPIC_API_KEY is required when provider is anthropic.")
    if provider == "openai" and not settings.openai_api_key:
        raise AnalysisConfigurationError("OPENAI_API_KEY is required when provider is openai.")

    return provider, model_override or settings.model or DEFAULT_MODELS[provider]


def _anthropic_summarize(settings: Settings, model: str, prompt: str) -> dict:
    from anthropic import Anthropic

    client = Anthropic(api_key=settings.anthropic_api_key)
    resp = client.messages.create(
        model=model,
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}],
    )
    text = "".join(block.text for block in resp.content if getattr(block, "type", "") == "text")
    return _parse_json_response(text)


def _openai_summarize(settings: Settings, model: str, prompt: str) -> dict:
    from openai import OpenAI

    client = OpenAI(api_key=settings.openai_api_key)
    resp = client.responses.create(
        model=model,
        input=prompt,
        text={"format": {"type": "json_object"}},
    )
    text = resp.output_text
    return _parse_json_response(text)


def summarize_release(
    release: Release,
    classification: Classification,
    settings: Settings,
    store: Store,
    provider_override: str | None = None,
    model_override: str | None = None,
) -> AnalysisResult:
    cached = store.get_analysis_by_hash(release.content_hash)
    if cached:
        return AnalysisResult(
            release_url=release.url,
            classification=Classification(cached["classification"]),
            summary=cached["summary"],
            why_it_matters=cached["why_it_matters"],
            novelty_score=int(cached["novelty_score"]),
            model_used=cached["model_used"],
            content_hash=cached["content_hash"],
            reasoning=cached["reasoning"],
        )

    prompt = PROMPT_TEMPLATE.format(
        title=release.title,
        source_name=release.source_name,
        classification=classification.value,
        content=(release.raw_text or "No extracted text available.")[:12000],
    )

    provider, model = _resolve_provider_settings(settings, provider_override, model_override)
    if provider == "openai":
        data = _openai_summarize(settings, model, prompt)
    else:
        data = _anthropic_summarize(settings, model, prompt)

    result = AnalysisResult(
        release_url=release.url,
        classification=classification,
        summary=data.get("summary", "No summary."),
        why_it_matters=data.get("why_it_matters"),
        novelty_score=max(1, min(10, int(data.get("novelty_score", 5)))),
        source_credibility=release.source_trust,
        model_used=model,
        content_hash=release.content_hash,
        reasoning=data.get("reasoning"),
    )
    store.save_analysis(result)
    return result
