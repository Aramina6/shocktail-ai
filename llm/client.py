"""Multi-provider LLM client — free hosted tiers only by default.

Default chain (all free signup, works on Streamlit Cloud):
  Groq → Google Gemini → Hugging Face → Together AI

Ollama is opt-in only (local). It is NOT tried unless ENABLE_OLLAMA=true.
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
    api_key_env: str
    signup_url: str
    api_base: str | None = None
    opt_in_env: str | None = None  # if set, only used when env is "true"


# Hosted free providers — no Ollama in default chain
HOSTED_PROVIDER_CHAIN: list[ProviderConfig] = [
    ProviderConfig(
        "groq",
        "groq/llama-3.3-70b-versatile",
        "GROQ_API_KEY",
        "https://console.groq.com/keys",
    ),
    ProviderConfig(
        "gemini",
        "gemini/gemini-2.0-flash",
        "GEMINI_API_KEY",
        "https://aistudio.google.com/apikey",
    ),
    ProviderConfig(
        "huggingface",
        "huggingface/meta-llama/Meta-Llama-3.1-8B-Instruct",
        "HF_TOKEN",
        "https://huggingface.co/settings/tokens",
    ),
    ProviderConfig(
        "together",
        "together_ai/meta-llama/Llama-3-8b-chat-hf",
        "TOGETHER_API_KEY",
        "https://api.together.xyz/settings/api-keys",
    ),
]

OLLAMA_PROVIDER = ProviderConfig(
    "ollama",
    "ollama/llama3.1",
    "OLLAMA_API_KEY",  # unused; kept for struct consistency
    "https://ollama.com",
    api_base="http://localhost:11434",
    opt_in_env="ENABLE_OLLAMA",
)


def _resolve_secret(env_name: str) -> str | None:
    if st is not None:
        try:
            if env_name in st.secrets:
                val = str(st.secrets[env_name]).strip()
                if val and "your_" not in val and "..." not in val:
                    return val
        except Exception:
            pass
    val = os.environ.get(env_name, "").strip()
    if val and "your_" not in val:
        return val
    return None


def _ollama_enabled() -> bool:
    flag = _resolve_secret("ENABLE_OLLAMA") or os.environ.get("ENABLE_OLLAMA", "")
    return str(flag).lower() in ("1", "true", "yes")


def get_provider_chain() -> list[ProviderConfig]:
    chain = list(HOSTED_PROVIDER_CHAIN)
    if _ollama_enabled():
        chain.append(OLLAMA_PROVIDER)
    return chain


# Back-compat alias for tests
PROVIDER_CHAIN = get_provider_chain


def get_configured_providers() -> list[ProviderConfig]:
    """Return hosted providers with valid API keys (+ Ollama if explicitly enabled)."""
    available: list[ProviderConfig] = []
    for provider in get_provider_chain():
        if provider.name == "ollama":
            if _ollama_enabled():
                available.append(provider)
            continue
        if _resolve_secret(provider.api_key_env):
            available.append(provider)
    return available


def get_provider_status() -> list[dict[str, str]]:
    statuses = []
    for provider in HOSTED_PROVIDER_CHAIN:
        if _resolve_secret(provider.api_key_env):
            statuses.append({
                "name": provider.name,
                "model": provider.model,
                "status": "configured ✅",
                "signup": provider.signup_url,
            })
        else:
            statuses.append({
                "name": provider.name,
                "model": provider.model,
                "status": f"needs {provider.api_key_env}",
                "signup": provider.signup_url,
            })
    ollama_status = "enabled (local)" if _ollama_enabled() else "disabled (set ENABLE_OLLAMA=true)"
    statuses.append({
        "name": "ollama",
        "model": OLLAMA_PROVIDER.model,
        "status": ollama_status,
        "signup": OLLAMA_PROVIDER.signup_url,
    })
    return statuses


def _setup_help_message() -> str:
    return (
        "**No free LLM key found.** Add at least ONE of these to "
        "`.streamlit/secrets.toml` (or Streamlit Cloud → Secrets):\n\n"
        "```toml\n"
        "GROQ_API_KEY = \"gsk_...\"       # https://console.groq.com/keys (recommended)\n"
        "GEMINI_API_KEY = \"...\"         # https://aistudio.google.com/apikey (free)\n"
        "HF_TOKEN = \"hf_...\"            # https://huggingface.co/settings/tokens\n"
        "TOGETHER_API_KEY = \"...\"       # https://api.together.xyz (signup credits)\n"
        "```\n\n"
        "Ollama is **not** used on Streamlit Cloud. Do not rely on it unless running locally "
        "with `ENABLE_OLLAMA = \"true\"`."
    )


def _apply_provider_env(provider: ProviderConfig) -> None:
    if provider.name != "ollama":
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
    from litellm import completion

    providers = get_configured_providers()
    if preferred_provider and preferred_provider != "auto":
        providers = sorted(
            providers,
            key=lambda p: 0 if p.name == preferred_provider else 1,
        )

    if not providers:
        return {
            "content": None,
            "provider": None,
            "model": None,
            "error": _setup_help_message(),
        }

    errors: list[str] = []

    for provider in providers:
        _apply_provider_env(provider)
        for attempt in range(max_retries):
            try:
                kwargs: dict[str, Any] = {
                    "model": provider.model,
                    "messages": messages,
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                    "timeout": 60,
                }
                if provider.name == "ollama":
                    kwargs["api_base"] = provider.api_base

                response = completion(**kwargs)
                content = response.choices[0].message.content
                return {
                    "content": content,
                    "provider": provider.name,
                    "model": provider.model,
                    "error": None,
                }
            except Exception as exc:
                err_msg = f"{provider.name}: {type(exc).__name__}"
                errors.append(err_msg)
                if attempt < max_retries - 1:
                    time.sleep(1.0 * (attempt + 1))

    return {
        "content": None,
        "provider": None,
        "model": None,
        "error": (
            "All configured providers failed. Try a different key or provider.\n"
            + " | ".join(errors)
            + "\n\n" + _setup_help_message()
        ),
    }