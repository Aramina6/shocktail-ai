"""Tests for the Intelligence Engine (internal LLM layer)."""

from unittest.mock import MagicMock, patch

import pytest

from llm.client import (
    USER_UNAVAILABLE_MSG,
    chat_completion,
    get_copilot_status,
    is_copilot_available,
)
from llm.context import build_messages, build_risk_context


class FakeSessionState:
    stress_context = {
        "scenario_name": "2008 Global Financial Crisis",
        "factor_shocks_pct": {"Mkt-RF": -45},
        "portfolio_betas": {"Mkt-RF": 1.0},
        "expected_return_impact_pct": -45.0,
        "factor_volatility_annualized_pct": 22.5,
    }
    power_context = {"power_scenario": "Texas Summer Heat Wave", "grid_stress_score": 75}


def test_copilot_status_online_with_key(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "test-key")
    assert is_copilot_available()
    assert get_copilot_status() == "Online"


def test_copilot_status_offline_without_key(monkeypatch):
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("HF_TOKEN", raising=False)
    monkeypatch.delenv("TOGETHER_API_KEY", raising=False)
    assert not is_copilot_available()
    assert get_copilot_status() == "Offline"


@patch("litellm.completion")
def test_chat_completion_product_response(mock_completion, monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "test-key")
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "Research narrative"
    mock_completion.return_value = mock_response

    result = chat_completion([{"role": "user", "content": "hi"}])
    assert result["content"] == "Research narrative"
    assert result["provider"] == "Shocktail Intelligence Engine"
    assert "groq" not in (result.get("error") or "").lower()


def test_unavailable_message_is_product_friendly(monkeypatch):
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("HF_TOKEN", raising=False)
    monkeypatch.delenv("TOGETHER_API_KEY", raising=False)

    result = chat_completion([{"role": "user", "content": "hi"}])
    assert result["content"] is None
    assert result["error"] == USER_UNAVAILABLE_MSG
    assert "GEMINI" not in result["error"]
    assert "HF_TOKEN" not in result["error"]


def test_build_risk_context_includes_power():
    text = build_risk_context(FakeSessionState())
    assert "Power" in text