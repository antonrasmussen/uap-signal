# Deploying uap-signal daily email

Production runs on GitHub Actions against `antonrasmussen/uap-signal`.

## 1. Configure repository secrets

```bash
gh secret set OPENAI_API_KEY -R antonrasmussen/uap-signal
gh secret set SMTP_USER -R antonrasmussen/uap-signal
gh secret set SMTP_PASSWORD -R antonrasmussen/uap-signal
gh secret set EMAIL_TO -R antonrasmussen/uap-signal
gh secret set ALERT_EMAIL_TO -R antonrasmussen/uap-signal
```

Optional:

```bash
gh secret set ANTHROPIC_API_KEY -R antonrasmussen/uap-signal
gh secret set RESEND_API_KEY -R antonrasmussen/uap-signal
```

## 2. Configure repository variables

```bash
gh variable set EMAIL_PROVIDER -R antonrasmussen/uap-signal --body smtp
gh variable set EMAIL_FROM -R antonrasmussen/uap-signal --body 'you@gmail.com'
gh variable set SMTP_HOST -R antonrasmussen/uap-signal --body smtp.gmail.com
gh variable set SMTP_PORT -R antonrasmussen/uap-signal --body 587
gh variable set UAP_SIGNAL_PROVIDER -R antonrasmussen/uap-signal --body openai
gh variable set UAP_SIGNAL_MODEL -R antonrasmussen/uap-signal --body gpt-4.1-mini
```

## 3. Gmail SMTP (solo use)

1. Use a Gmail account with 2FA enabled.
2. Create an [App Password](https://myaccount.google.com/apppasswords).
3. Set:
   - `SMTP_USER` / `EMAIL_FROM` = that Gmail address
   - `SMTP_PASSWORD` = the app password (not your login password)
   - `EMAIL_PROVIDER=smtp`

The same credentials already used by `medical-equipment-corp/sam-opportunity-pipeline` can be reused.

## 4. Verify email locally (optional)

```bash
pip install -e .
uap-signal send-test
```

## 5. Manual backfill of existing reports

Once secrets are set:

```bash
gh workflow run "Daily UAP Signal Watch" -R antonrasmussen/uap-signal -f backfill=true
```

Or use the Actions UI: **Daily UAP Signal Watch** → **Run workflow** → enable `backfill`.

This emails each file in `reports/` as a separate message, oldest first.

## 6. Schedules

| Workflow | Cron (UTC) | Behavior |
|----------|------------|----------|
| Daily watch | `0 12 * * *` | Detect new PURSUE release → report+email, else heartbeat |
| Friday catch-up | `0 23 * * 5` | Same watch job (releases often drop Friday) |
| Weekly digest | `0 12 * * 1` | News RSS digest email |

GitHub may delay scheduled workflows on inactive repos by up to about an hour.

## 7. State committed by CI

- `state/releases.json` — seen PURSUE release IDs and report paths
- `state/seen_news.json` — news URLs already included in digests
- `reports/*.md` — generated intelligence reports

SQLite (`.uap_signal.db`) remains a local/CI ephemeral analysis cache and is gitignored.
