"""Unit tests for core.providers — pure logic, no network calls."""

import pytest

from core.config import Settings
from core.providers import PROVIDERS, get_api_key, get_model, get_provider


def test_known_provider_resolves():
    provider = get_provider(Settings(provider="nvidia", model=None))
    assert provider.name == "nvidia"
    assert provider.base_url.endswith("/v1")


def test_unknown_provider_raises_with_helpful_message():
    with pytest.raises(RuntimeError) as exc:
        get_provider(Settings(provider="does-not-exist", model=None))
    assert "Unknown AI_PROVIDER" in str(exc.value)
    assert "nvidia" in str(exc.value)  # lists valid options


def test_model_override_wins_over_default():
    assert get_model(Settings(provider="nvidia", model="custom/model")) == "custom/model"


def test_default_model_used_when_no_override():
    settings = Settings(provider="nvidia", model=None)
    assert get_model(settings) == PROVIDERS["nvidia"].default_model


def test_missing_key_raises(monkeypatch):
    monkeypatch.delenv("NVIDIA_API_KEY", raising=False)
    with pytest.raises(RuntimeError) as exc:
        get_api_key(PROVIDERS["nvidia"])
    assert "NVIDIA_API_KEY" in str(exc.value)


def test_key_present_is_returned(monkeypatch):
    monkeypatch.setenv("NVIDIA_API_KEY", "test-key-123")
    assert get_api_key(PROVIDERS["nvidia"]) == "test-key-123"


def test_keyless_provider_returns_placeholder():
    # Ollama needs no key; the OpenAI SDK still requires a non-empty string.
    assert get_api_key(PROVIDERS["ollama"]) == "not-needed"
