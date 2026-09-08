"""Provider registry + client factory.

NVIDIA, OpenAI, Gemini, and Ollama all speak the OpenAI-compatible protocol, so a
"provider" is just a base URL, the env var holding its API key, and a default
model. Switching providers = change AI_PROVIDER in .env. Adding a new provider
= add one entry to PROVIDERS below.
"""

import os
from dataclasses import dataclass

from openai import OpenAI

from core.config import Settings, get_settings


@dataclass(frozen=True)
class Provider:
    name: str
    base_url: str | None   # None => use the OpenAI SDK's default (api.openai.com)
    key_env: str | None    # None => provider needs no key (e.g. local Ollama)
    default_model: str


PROVIDERS: dict[str, Provider] = {
    "nvidia": Provider(
        name="nvidia",
        base_url="https://integrate.api.nvidia.com/v1",
        key_env="NVIDIA_API_KEY",
        default_model="openai/gpt-oss-20b",
    ),
    # Ready-to-use slots — wired but not yet exercised. Add a key to .env and
    # set AI_PROVIDER to switch.
    "openai": Provider(
        name="openai",
        base_url=None,
        key_env="OPENAI_API_KEY",
        default_model="gpt-4o-mini",
    ),
    "gemini": Provider(
        name="gemini",
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        key_env="GEMINI_API_KEY",
        default_model="gemini-2.5-flash",
    ),
    "ollama": Provider(
        name="ollama",
        base_url="http://localhost:11434/v1",
        key_env=None,
        default_model="llama3.1",
    ),
}


def get_provider(settings: Settings | None = None) -> Provider:
    settings = settings or get_settings()
    try:
        return PROVIDERS[settings.provider]
    except KeyError:
        valid = ", ".join(sorted(PROVIDERS))
        raise RuntimeError(
            f"Unknown AI_PROVIDER '{settings.provider}'. Valid options: {valid}."
        ) from None


def get_api_key(provider: Provider) -> str:
    if provider.key_env is None:
        return "not-needed"  # OpenAI SDK requires a non-empty string even when unused
    key = os.environ.get(provider.key_env)
    if not key:
        raise RuntimeError(
            f"{provider.key_env} is not set. Copy .env.example to .env and add your key."
        )
    return key


def get_model(settings: Settings | None = None, provider: Provider | None = None) -> str:
    settings = settings or get_settings()
    provider = provider or get_provider(settings)
    return settings.model or provider.default_model


def get_client(settings: Settings | None = None) -> OpenAI:
    """Build an OpenAI-compatible client for the configured provider."""
    settings = settings or get_settings()
    provider = get_provider(settings)
    kwargs: dict = {"api_key": get_api_key(provider)}
    if provider.base_url:
        kwargs["base_url"] = provider.base_url
    return OpenAI(**kwargs)
