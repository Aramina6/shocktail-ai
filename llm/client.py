"""Shocktail Intelligence Engine — internal LLM layer.

Product rule: users never see provider names, API keys, or infra details.
Operators configure GROQ_API_KEY in Streamlit Secrets (deploy-time only).
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

PRODUCT_NAME = "Shocktail Intelligence Engine"
PRIMARY_KEY = "GROQ_API_KEY"
PRIMARY_MODEL = "groq/llama-3.3-70b-versatile"

USER_UNAVAILABLE_MSG = (
    "Research Copilot is temporarily unavailable. "
    "Please try again in a few moments."
)

OPERATOR_SETUP_MSG = (
    "Operator: set GROQ_API_KEY in Streamlit Cloud → Settings → Secrets, then reboot."
)


@dataclass(frozen=True)
class _Provider:
    model: str
    api_key_env: str


# Silent fallbacks — never surfaced in product UI
_FALLBACK_CHAIN: list[_Provider] = [
    _Provider(PRIMARY_MODEL, PRIMARY_KEY),
    _Provider("gemini/gemini-2.0-flash", "GEMINI_API_KEY"),
    _Provider("huggingface/meta-llama/Meta-Llama-3.1-8B-Instruct", "HF_TOKEN"),
    _Provider("together_ai/meta-llama/Llama-3-8b-chat-hf", "TOGETHER_API_KEY"),
]


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
    return val if val and "your_" not in val else None


def is_copilot_available() -> bool:
    return len(_active_providers()) > 0


def get_copilot_status() -> str:
    return "Online" if is_copilot_available() else "Offline"


def _active_providers() -> list[_Provider]:
    return [p for p in _FALLBACK_CHAIN if _resolve_secret(p.api_key_env)]


# Back-compat for tests
def get_configured_providers():
    return _active_providers()


PROVIDER_CHAIN = _FALLBACK_CHAIN


def get_provider_status():
    """Internal/debug only — not used in product UI."""
    return [{"status": get_copilot_status()}]


def chat_completion(
    messages: list[dict[str, str]],
    *,
    temperature: float = 0.4,
    max_tokens: int = 1200,
    preferred_provider: str | None = None,
    max_retries: int = 2,
) -> dict[str, Any]:
    from litellm import completion

    providers = _active_providers()
    if not providers:
        return {
            "content": None,
            "provider": None,
            "model": None,
            "error": USER_UNAVAILABLE_MSG,
            "operator_hint": OPERATOR_SETUP_MSG,
        }

    errors: list[str] = []

    for provider in providers:
        key = _resolve_secret(provider.api_key_env)
        if key:
            os.environ[provider.api_key_env] = key

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
                    "provider": PRODUCT_NAME,
                    "model": None,
                    "error": None,
                }
            except Exception as exc:
                errors.append(type(exc).__name__)
                if attempt < max_retries - 1:
                    time.sleep(1.0 * (attempt + 1))

    return {
        "content": None,
        "provider": None,
        "model": None,
        "error": USER_UNAVAILABLE_MSG,
        "operator_hint": OPERATOR_SETUP_MSG,
    }