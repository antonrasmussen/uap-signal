# UAP Signal

`uap-signal` is a Python CLI for finding what is actually new in UAP/UFO releases.

## What it does

- Pulls from Google News RSS and the WARUFO.com PURSUE archive index by default
- Detects new PURSUE batches via warufo `data-release` tags
- Classifies items with rule-based source trust logic
- Uses one LLM provider at a time for summaries, novelty scoring, and report synthesis
- Caches results in SQLite (local) and tracks seen releases in committed `state/`
- Generates markdown reports under `reports/` and emails them over SMTP/Resend
- Runs daily on GitHub Actions (heartbeat when quiet; full report when a release drops)
- Sends a weekly news digest

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Env config

Create `.env`:

```env
UAP_SIGNAL_DB=.uap_signal.db
UAP_SIGNAL_PROVIDER=openai
UAP_SIGNAL_MODEL=gpt-4.1-mini
OPENAI_API_KEY=...
# or ANTHROPIC_API_KEY=...

EMAIL_PROVIDER=smtp
EMAIL_FROM=you@gmail.com
EMAIL_TO=you@gmail.com
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=you@gmail.com
SMTP_PASSWORD=your-gmail-app-password
ALERT_EMAIL_TO=you@gmail.com
```

See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for GitHub Actions secrets/variables.

## Commands

```bash
uap-signal check --date 2026-05-08 --max-items 25
uap-signal check --dry-run
uap-signal watch
uap-signal watch --dry-run
uap-signal watch --force-release 05
uap-signal report 05
uap-signal send-report reports/2026-08-07-pursue-release-05-report.md
uap-signal digest
uap-signal send-test
uap-signal backfill-email
uap-signal sources
uap-signal history --days 14
uap-signal config
```

## Daily automation

GitHub Actions workflows:

- `.github/workflows/daily.yml` — `0 12 * * *` plus Friday evening catch-up; runs `uap-signal watch`, commits new reports/state, emails reports or heartbeat
- `.github/workflows/weekly-digest.yml` — Mondays; runs `uap-signal digest`

Manual backfill of existing reports (5 separate emails):

1. Configure secrets/variables (see DEPLOYMENT.md)
2. Actions → **Daily UAP Signal Watch** → Run workflow → set `backfill=true`

## Notes

- Date semantics are **first seen by us**, not necessarily publisher timestamp.
- `--dry-run` fetches and prints/skips writes depending on the command.
- Classification is split from summarization:
  - Classification: rule-based (`classifier.py`)
  - Summarization/scoring: LLM (`analyzer.py`)
  - Report synthesis: LLM (`synthesize_report`)
- `war_gov` source (`https://www.war.gov/ufo`) is registered but currently blocked by Akamai CDN. The `warufo` source indexes the same PURSUE records via the accessible `warufo.com` third-party archive.
- Source failures are reported as CLI warnings so a partial report is not mistaken for a complete fetch.
