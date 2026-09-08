"""Application settings, loaded from the environment / .env file.

The only two knobs are which provider to talk to and (optionally) which model
to use. Everything provider-specific (base URL, key, default model) lives in
`core.providers`.
"""

import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    provider: str          # e.g. "nvidia" — must match a key in core.providers.PROVIDERS
    model: str | None      # optional override; falls back to the provider's default


def get_settings() -> Settings:
    """Read settings from the environment (loading .env first if present)."""
    load_dotenv()  # idempotent: safe to call repeatedly
    provider = os.environ.get("AI_PROVIDER", "nvidia").strip().lower()
    model = os.environ.get("AI_MODEL") or None
    return Settings(provider=provider, model=model)
