"""LLM summarization and scoring with prompt caching support."""

from __future__ import annotations

import json

from uap_signal.config import DEFAULT_MODELS, Settings
from uap_signal.models import AnalysisResult, Classification, Release
from uap_signal.store import Store


class AnalysisConfigurationError(RuntimeError):
    """Raised when LLM provider configuration is invalid."""


SYSTEM_PROMPT = """You are an expert analyst of UAP/UFO release items. Analyze government and news reports about Unidentified Anomalous Phenomena (UAP) and produce a structured JSON assessment.

<instructions>
1. Read the title, source name, pre-classification, and content text carefully.
2. Write a 2-3 sentence plain-language summary that captures what the report actually says.
3. Write one sentence explaining why this report matters in a broader context (national security, historical significance, pattern recognition, public understanding, etc.).
4. Assign a novelty score from 1 to 10 following the guidelines below.
5. Write a short rationale justifying the score.
6. Output ONLY valid JSON with the exact keys specified — no markdown code fences, no surrounding text, no additional commentary.
</instructions>

<output_format>
{
  "summary": "2-3 sentence plain-language summary of the report content",
  "why_it_matters": "single sentence explaining broader significance",
  "novelty_score": 5,
  "reasoning": "short rationale for the novelty score"
}
</output_format>

<novelty_guidelines>
Score 1-3 (Routine / Rehash):
The same event or document covered by multiple news outlets with no new information. Well-known historical documents that have been public for years. No new analytical value.

Score 4-6 (Moderately Interesting):
A new incident or document that adds incremental knowledge. Some new details beyond what was previously known. Contributes to the record but does not fundamentally change understanding.

Score 7-8 (Highly Notable):
First-hand military or intelligence testimony accompanied by sensor data. Formal congressional action requesting specific classified records. Incidents at or near nuclear weapons facilities (a well-documented historical pattern). Multi-object formation behavior in contested airspace. Video or photographic evidence of unexplained objects with supporting context.

Score 9-10 (Extraordinary):
Confirmed evidence of non-human technology or intelligence. Physical debris with verified non-terrestrial material properties. Official government acknowledgment of extraterrestrial or non-human intelligence. Direct sensor measurement of performance far beyond known human technology.
</novelty_guidelines>

<background_context>
The Department of War (DoW) PURSUE program (Presidential Unsealing and Reporting System for UAP Encounters) launched in May 2026 under Secretary Pete Hegseth pursuant to President Trump's directive for government transparency on UAP. Release 01 (May 8, 2026) contained 162 files from six agencies: FBI, DoD, NASA, State Department, USAF, and USN. Release 02 (May 22, 2026) added 64 records from DoW, NASA, CIA, ODNI, and DOE — including 51 military sensor videos (DOW-UAP-PR050 through PR099), 6 documents (most notably a 116-page Armed Forces Special Weapons Program file documenting 209 UAP reports at Sandia Base, New Mexico between 1948-1950), and 7 NASA Apollo and Mercury voice loop audio recordings. The All-domain Anomaly Resolution Office (AARO) coordinates identification and declassification of responsive materials. The combined PURSUE catalog now contains 226 records spanning 79 years (1947-2026) across nine agencies.
</background_context>

<example_1>
Title: DOW-UAP-PR050, "4 UAP Formation Iran 26 Aug 2022 over water"
Source: warufo
Pre-classification: GENUINELY_NEW
Content: On March 6, 2026, eight members of the U.S. House of Representatives requested access to 51 potentially UAP-related records. AARO identified responsive materials on a classified network. A 20-second infrared video shows four areas of contrast in formation over water near Iran.

{
  "summary": "Military infrared footage from August 2022 captures four UAPs in formation over water near Iran. The 20-second video was uploaded to a classified network in June 2024 and released under PURSUE Release 02 following a formal congressional records request by eight House members.",
  "why_it_matters": "Multi-object formation flight in a contested CENTCOM area of responsibility, released only after bipartisan congressional demand for these specific records, suggests coordinated behavior with national security implications.",
  "novelty_score": 7,
  "reasoning": "Direct IR sensor data showing four objects in deliberate formation over a strategic region, released only after congressional pressure — unusual combination of military evidence and political oversight."
}
</example_1>

<example_2>
Title: Pentagon releases more UFO files: "Speechless after these observations"
Source: news_rss
Pre-classification: CONTEXT
Content: CBS News reports on the Pentagon releasing additional UFO files that have left observers reportedly speechless. No specific content details are available in the extracted text.

{
  "summary": "CBS News covers the broader PURSUE UAP file release but provides no specific details on the content of the released files. The reporting is a news aggregation piece without independent investigation or access to the documents themselves.",
  "why_it_matters": "Mainstream news coverage of UAP disclosure indicates growing normalization of the topic in public discourse, but this particular piece adds no substantive information beyond the headline.",
  "novelty_score": 2,
  "reasoning": "News aggregation of an already-reported event with no new details, no original reporting, and no access to the underlying documents."
}
</example_2>

<anti_hallucination>
Do NOT fabricate or infer details that are not present in the provided content. If the content is thin (headline only, truncated, or a news aggregation), say so explicitly in the summary and adjust the novelty score downward. Do not treat news articles about a document release as if they are the documents themselves. Acknowledge limitations honestly.
</anti_hallucination>

Now analyze the following item. Output ONLY valid JSON — no markdown fences, no code blocks, no surrounding text."""

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
    import re
    match = re.search(r"```(?:json)?\s*\n?(.*?)\n?```", text, re.DOTALL)
    if match:
        text = match.group(1).strip()
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


def _anthropic_summarize(
    settings: Settings,
    model: str,
    title: str,
    source_name: str,
    classification: str,
    content: str,
) -> dict:
    from anthropic import Anthropic

    client = Anthropic(api_key=settings.anthropic_api_key)
    item_data = f"Title: {title}\nSource: {source_name}\nPre-classification: {classification}\nContent:\n{content}"
    resp = client.messages.create(
        model=model,
        max_tokens=500,
        system=[
            {
                "type": "text",
                "text": SYSTEM_PROMPT,
                "cache_control": {"type": "ephemeral"},
            }
        ],
        messages=[{"role": "user", "content": item_data}],
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

    provider, model = _resolve_provider_settings(settings, provider_override, model_override)
    content = (release.raw_text or "No extracted text available.")[:12000]
    if provider == "openai":
        prompt = PROMPT_TEMPLATE.format(
            title=release.title,
            source_name=release.source_name,
            classification=classification.value,
            content=content,
        )
        data = _openai_summarize(settings, model, prompt)
    else:
        data = _anthropic_summarize(
            settings,
            model,
            title=release.title,
            source_name=release.source_name,
            classification=classification.value,
            content=content,
        )

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


SYNTHESIS_PROMPT = """You are synthesizing a PURSUE UAP release intelligence report.
Return ONLY valid JSON with keys:
- executive_summary (2-4 paragraph plain-language overview of the release)
- key_findings (array of exactly 3 short finding strings)
- character (one short phrase describing the release character for a comparison table)
- next_steps (array of 2-4 concrete follow-up actions)

Do not invent documents that are not in the item list. Prefer concrete IDs, agencies, years, and novelty themes.

Release ID: {release_id}
Release date: {release_date}
Item count: {item_count}
Agency mix: {agency_mix}
Average novelty: {avg_novelty}

Top items (title | agency | novelty | summary):
{item_lines}
"""


def synthesize_report(
    *,
    release_id: str,
    release_date: str,
    items: list[tuple[Release, AnalysisResult]],
    settings: Settings,
    provider_override: str | None = None,
    model_override: str | None = None,
):
    """Produce executive summary / key findings for a release report."""
    from collections import Counter

    from uap_signal.report import Synthesis

    provider, model = _resolve_provider_settings(settings, provider_override, model_override)
    agencies = Counter((r.metadata or {}).get("agency") or r.source_name for r, _ in items)
    scores = [a.novelty_score for _, a in items]
    avg = round(sum(scores) / len(scores), 2) if scores else 0
    ranked = sorted(items, key=lambda pair: (-pair[1].novelty_score, pair[0].title.lower()))
    item_lines = []
    for release, analysis in ranked[:40]:
        agency = (release.metadata or {}).get("agency") or release.source_name
        item_lines.append(
            f"- {release.title} | {agency} | {analysis.novelty_score}/10 | {analysis.summary}"
        )
    prompt = SYNTHESIS_PROMPT.format(
        release_id=release_id,
        release_date=release_date,
        item_count=len(items),
        agency_mix=", ".join(f"{k} ({v})" for k, v in agencies.most_common()),
        avg_novelty=avg,
        item_lines="\n".join(item_lines) or "(none)",
    )

    if provider == "openai":
        data = _openai_summarize(settings, model, prompt)
    else:
        from anthropic import Anthropic

        client = Anthropic(api_key=settings.anthropic_api_key)
        resp = client.messages.create(
            model=model,
            max_tokens=1200,
            messages=[{"role": "user", "content": prompt}],
        )
        text = "".join(block.text for block in resp.content if getattr(block, "type", "") == "text")
        data = _parse_json_response(text)

    findings = data.get("key_findings") or []
    if isinstance(findings, str):
        findings = [findings]
    next_steps = data.get("next_steps") or []
    if isinstance(next_steps, str):
        next_steps = [next_steps]

    return Synthesis(
        executive_summary=str(data.get("executive_summary") or "No executive summary generated."),
        key_findings=[str(x) for x in findings][:3],
        character=str(data.get("character") or f"PURSUE Release {release_id}"),
        next_steps=[str(x) for x in next_steps][:4],
    )

