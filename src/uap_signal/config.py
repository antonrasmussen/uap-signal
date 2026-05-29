"""Runtime configuration for UAP Signal."""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()

DEFAULT_MODELS = {
    "anthropic": "claude-3-5-sonnet-latest",
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
    )
