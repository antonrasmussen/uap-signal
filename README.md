# UAP Signal

`uap-signal` is a Python CLI for finding what is actually new in UAP/UFO releases.

## What it does

- Pulls from Google News RSS and the WARUFO.com PURSUE archive index by default
- Classifies items with rule-based source trust logic
- Uses one LLM provider at a time for summaries and novelty scoring
- Caches results in SQLite to avoid repeat API spend
- Supports dry-run cost estimates and max-item caps

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

For development:

```bash
pip install -e ".[dev]"
ruff check .
pytest
```

## Env config

Create `.env`:

```env
UAP_SIGNAL_DB=.uap_signal.db
UAP_SIGNAL_PROVIDER=anthropic
UAP_SIGNAL_MODEL=claude-3-5-sonnet-latest
ANTHROPIC_API_KEY=...
# or OPENAI_API_KEY=...
```

Optional for v1 source:

```env
CONGRESS_API_KEY=...
```

## Commands

```bash
uap-signal check --date 2026-05-08 --max-items 25
uap-signal check --dry-run
uap-signal check --provider openai
uap-signal check --provider openai --model gpt-4.1-mini
uap-signal analyze https://example.com/article
uap-signal sources
uap-signal history --days 14
uap-signal config
```

## Notes

- Date semantics are **first seen by us**, not necessarily publisher timestamp.
- `--dry-run` fetches and prints item titles/URLs, estimates LLM spend, and skips DB writes and full article/PDF extraction.
- Classification is split from summarization:
  - Classification: rule-based (`classifier.py`)
  - Summarization/scoring: LLM (`analyzer.py`)
- `v1` sources (`black_vault`, `aaro`, `congress`) are implemented and available in the source registry.
- `war_gov` source (`https://www.war.gov/ufo`) is registered but currently blocked by Akamai CDN. The `warufo` source indexes the same PURSUE records via the accessible `warufo.com` third-party archive.
- `news_rss` uses Google News RSS. Article links are Google redirect URLs that resolve in a browser.
- Source failures are reported as CLI warnings so a partial report is not mistaken for a complete fetch.
