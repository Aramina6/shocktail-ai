"""Tests for the free LLM client layer."""

import os
from unittest.mock import MagicMock, patch

import pytest

from llm.client import (
    PROVIDER_CHAIN,
    chat_completion,
    get_configured_providers,
    get_provider_status,
)
from llm.context import build_messages, build_risk_context


class FakeSessionState:
    stress_context = {
        "scenario_name": "2008 Global Financial Crisis",
        "scenario_description": "Banking crisis",
        "factor_shocks_pct": {"Mkt-RF": -45, "VIX": 120},
        "portfolio_betas": {"Mkt-RF": 1.0},
        "expected_return_impact_pct": -45.0,
        "factor_volatility_annualized_pct": 22.5,
        "industries_impacted": ["Financials"],
    }


def test_build_risk_context_includes_stress_data():
    text = build_risk_context(FakeSessionState())
    assert "2008 Global Financial Crisis" in text
    assert "Mkt-RF" in text
    assert "-45" in text


def test_build_messages_wraps_user_question():
    msgs = build_messages(FakeSessionState(), "Explain this", "You are helpful.")
    assert msgs[0]["role"] == "system"
    assert msgs[1]["role"] == "user"
    assert "Explain this" in msgs[1]["content"]
    assert "LIVE CONTEXT" in msgs[1]["content"]


def test_get_configured_providers_with_groq_key(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "test-key")
    providers = get_configured_providers()
    assert any(p.name == "groq" for p in providers)


def test_get_provider_status_reports_missing_keys(monkeypatch):
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    monkeypatch.delenv("HF_TOKEN", raising=False)
    statuses = {s["name"]: s["status"] for s in get_provider_status()}
    assert "missing" in statuses["groq"]
    assert "local" in statuses["ollama"]


@patch("litellm.completion")
def test_chat_completion_success(mock_completion, monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "test-key")

    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "Test narrative"
    mock_completion.return_value = mock_response

    result = chat_completion([{"role": "user", "content": "hi"}])

    assert result["content"] == "Test narrative"
    assert result["provider"] == "groq"
    assert result["error"] is None
    mock_completion.assert_called_once()


@patch("litellm.completion")
def test_chat_completion_fallback_on_failure(mock_completion, monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "test-key")
    monkeypatch.delenv("HF_TOKEN", raising=False)

    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "Ollama response"

    def side_effect(*args, **kwargs):
        model = kwargs.get("model", "")
        if model.startswith("groq/"):
            raise Exception("rate limit")
        return mock_response

    mock_completion.side_effect = side_effect

    result = chat_completion([{"role": "user", "content": "hi"}], max_retries=1)

    assert result["content"] == "Ollama response"
    assert result["provider"] == "ollama"


def test_no_providers_returns_helpful_error(monkeypatch):
    for provider in PROVIDER_CHAIN:
        if provider.api_key_env:
            monkeypatch.delenv(provider.api_key_env, raising=False)

    with patch("llm.client.get_configured_providers", return_value=[]):
        result = chat_completion([{"role": "user", "content": "hi"}])

    assert result["content"] is None
    assert "GROQ_API_KEY" in result["error"]