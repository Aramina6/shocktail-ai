"""Multi-provider LLM client with free-tier fallback chain.

Priority: Groq (free) → Hugging Face Inference → Ollama (local, zero cost).
"""

from __future__ import annotations

import os
import time
from dataclasses import dataclass
from typing import Any

try:
    import streamlit as st
except ImportError:
    st = None


@dataclass(frozen=True)
class ProviderConfig:
    name: str
    model: str
    api_key_env: str | None
    api_base: str | None = None


PROVIDER_CHAIN: list[ProviderConfig] = [
    ProviderConfig("groq", "groq/llama-3.3-70b-versatile", "GROQ_API_KEY"),
    ProviderConfig(
        "huggingface",
        "huggingface/meta-llama/Meta-Llama-3.1-8B-Instruct",
        "HF_TOKEN",
    ),
    ProviderConfig("ollama", "ollama/llama3.1", None, "http://localhost:11434"),
]


def _resolve_secret(env_name: str) -> str | None:
    """Read API key from Streamlit secrets or environment."""
    if st is not None:
        try:
            if env_name in st.secrets:
                return str(st.secrets[env_name])
        except Exception:
            pass
    return os.environ.get(env_name)


def get_configured_providers() -> list[ProviderConfig]:
    """Return providers that have credentials or need none (Ollama)."""
    available: list[ProviderConfig] = []
    for provider in PROVIDER_CHAIN:
        if provider.api_key_env is None:
            available.append(provider)
        elif _resolve_secret(provider.api_key_env):
            available.append(provider)
    return available


def get_provider_status() -> list[dict[str, str]]:
    """Human-readable status for each provider."""
    statuses = []
    for provider in PROVIDER_CHAIN:
        if provider.api_key_env is None:
            statuses.append({
                "name": provider.name,
                "model": provider.model,
                "status": "available (local — start Ollama if needed)",
            })
        elif _resolve_secret(provider.api_key_env):
            statuses.append({
                "name": provider.name,
                "model": provider.model,
                "status": "configured",
            })
        else:
            statuses.append({
                "name": provider.name,
                "model": provider.model,
                "status": f"missing {provider.api_key_env}",
            })
    return statuses


def _apply_provider_env(provider: ProviderConfig) -> None:
    if provider.api_key_env:
        key = _resolve_secret(provider.api_key_env)
        if key:
            os.environ[provider.api_key_env] = key
    if provider.api_base:
        os.environ["OLLAMA_API_BASE"] = provider.api_base


def chat_completion(
    messages: list[dict[str, str]],
    *,
    temperature: float = 0.4,
    max_tokens: int = 1200,
    preferred_provider: str | None = None,
    max_retries: int = 2,
) -> dict[str, Any]:
    """
    Call LLM with automatic fallback across free providers.

    Returns dict with keys: content, provider, model, error (if all failed).
    """
    from litellm import completion

    providers = get_configured_providers()
    if preferred_provider:
        providers = sorted(
            providers,
            key=lambda p: 0 if p.name == preferred_provider else 1,
        )

    if not providers:
        return {
            "content": None,
            "provider": None,
            "model": None,
            "error": (
                "No LLM provider configured. Add GROQ_API_KEY (free at console.groq.com) "
                "or HF_TOKEN to .streamlit/secrets.toml, or run Ollama locally."
            ),
        }

    errors: list[str] = []

    for provider in providers:
        _apply_provider_env(provider)
        for attempt in range(max_retries):
            try:
                response = completion(
                    model=provider.model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    timeout=60,
                )
                content = response.choices[0].message.content
                return {
                    "content": content,
                    "provider": provider.name,
                    "model": provider.model,
                    "error": None,
                }
            except Exception as exc:
                err_msg = f"{provider.name} attempt {attempt + 1}: {exc}"
                errors.append(err_msg)
                if attempt < max_retries - 1:
                    time.sleep(1.5 * (attempt + 1))

    return {
        "content": None,
        "provider": None,
        "model": None,
        "error": "All providers failed. " + " | ".join(errors),
    }