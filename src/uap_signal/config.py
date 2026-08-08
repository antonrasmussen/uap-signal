"""Runtime configuration for UAP Signal."""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()

DEFAULT_MODELS = {
    "anthropic": "claude-sonnet-4-5",
    "openai": "gpt-4.1-mini",
}


@dataclass
class Settings:
    database_path: str
    provider: str
    anthropic_api_key: str | None
    openai_api_key: str | None
    model: str
    max_items: int
    request_timeout_seconds: int
    email_provider: str
    email_from: str
    email_to: str
    alert_email_to: str
    smtp_host: str
    smtp_port: int
    smtp_user: str
    smtp_password: str
    resend_api_key: str
    reports_dir: str
    state_dir: str


def _env_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None:
        return default
    try:
        return int(value)
    except ValueError as exc:
        raise ValueError(f"{name} must be an integer") from exc


def get_settings() -> Settings:
    provider = os.getenv("UAP_SIGNAL_PROVIDER", "anthropic").lower()
    model = os.getenv("UAP_SIGNAL_MODEL") or DEFAULT_MODELS.get(provider, DEFAULT_MODELS["anthropic"])
    return Settings(
        database_path=os.getenv("UAP_SIGNAL_DB", ".uap_signal.db"),
        provider=provider,
        anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        model=model,
        max_items=_env_int("UAP_SIGNAL_MAX_ITEMS", 25),
        request_timeout_seconds=_env_int("UAP_SIGNAL_HTTP_TIMEOUT", 30),
        email_provider=os.getenv("EMAIL_PROVIDER", "smtp").lower(),
        email_from=os.getenv("EMAIL_FROM", "reports@example.com"),
        email_to=os.getenv("EMAIL_TO", ""),
        alert_email_to=os.getenv("ALERT_EMAIL_TO", ""),
        smtp_host=os.getenv("SMTP_HOST", "smtp.gmail.com"),
        smtp_port=_env_int("SMTP_PORT", 587),
        smtp_user=os.getenv("SMTP_USER", ""),
        smtp_password=os.getenv("SMTP_PASSWORD", ""),
        resend_api_key=os.getenv("RESEND_API_KEY", ""),
        reports_dir=os.getenv("UAP_SIGNAL_REPORTS_DIR", "reports"),
        state_dir=os.getenv("UAP_SIGNAL_STATE_DIR", "state"),
    )
