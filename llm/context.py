"""Build grounded context from app session state for LLM prompts."""

from __future__ import annotations

from typing import Any


def _format_dict(d: dict[str, Any], suffix: str = "") -> str:
    if not d:
        return "  (none)"
    lines = []
    for key, value in d.items():
        if isinstance(value, float):
            lines.append(f"  - {key}: {value:.2f}{suffix}")
        else:
            lines.append(f"  - {key}: {value}{suffix}")
    return "\n".join(lines)


def build_risk_context(session_state: Any) -> str:
    """Serialize stress test + physical hazard snapshot for the copilot."""
    parts: list[str] = []

    stress = getattr(session_state, "stress_context", None) or {}
    if stress:
        parts.append("## Active Scenario Intelligence")
        codename = stress.get("cocktail_name", "")
        if codename:
            parts.append(f"Scenario codename: {codename}")
        parts.append(f"Scenario: {stress.get('scenario_name', 'Not set')}")
        parts.append(f"Description: {stress.get('scenario_description', '')}")
        parts.append(f"Expected return impact: {stress.get('expected_return_impact_pct', 'N/A')}%")
        parts.append(
            f"Factor volatility (annualized): "
            f"{stress.get('factor_volatility_annualized_pct', 'N/A')}%"
        )
        parts.append("Factor shocks (%):")
        parts.append(_format_dict(stress.get("factor_shocks_pct", {}), "%"))
        parts.append("Portfolio betas:")
        parts.append(_format_dict(stress.get("portfolio_betas", {})))
        industries = stress.get("industries_impacted", [])
        if industries:
            parts.append("Industries typically impacted:")
            for ind in industries:
                parts.append(f"  - {ind}")
    else:
        parts.append(
            "## Factor Stress Test\nNo stress context yet. "
            "User should configure scenario and betas in the Factor Stress Testing tab."
        )

    phys = getattr(session_state, "physical_hazard_context", None) or {}
    if phys:
        parts.append("\n## Physical Hazard Snapshot")
        for key, value in phys.items():
            if value:
                parts.append(f"- {key}: {value}")

    power = getattr(session_state, "power_context", None) or {}
    if power:
        parts.append("\n## Power & Grid Context")
        if power.get("cocktail_name"):
            parts.append(f"Power cocktail: {power['cocktail_name']}")
        parts.append(f"Power scenario: {power.get('power_scenario', 'N/A')}")
        parts.append(f"Description: {power.get('description', '')}")
        parts.append(f"Grid stress score: {power.get('grid_stress_score', 'N/A')}/100")
        if power.get("aggregate_heat_stress") is not None:
            parts.append(f"Live avg heat stress: {power['aggregate_heat_stress']}/100")
        if power.get("hottest_region"):
            parts.append(f"Hottest hub: {power['hottest_region']}")
        if power.get("electricity_cpi_yoy_pct") is not None:
            parts.append(f"Electricity CPI YoY: {power['electricity_cpi_yoy_pct']:.1f}%")
        hints = power.get("factor_shock_hints", {})
        if hints:
            parts.append("Suggested factor hints (%):")
            parts.append(_format_dict(hints, "%"))
        sectors = power.get("sectors_impacted", [])
        if sectors:
            parts.append("Power-impacted sectors:")
            for s in sectors:
                parts.append(f"  - {s}")

    return "\n".join(parts)


def build_messages(
    session_state: Any,
    user_message: str,
    system_prompt: str,
) -> list[dict[str, str]]:
    """Assemble chat messages with grounded context."""
    context_block = build_risk_context(session_state)
    return [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": (
                f"LIVE CONTEXT (ground your answer in this data only):\n\n"
                f"{context_block}\n\n---\n\nUSER QUESTION:\n{user_message}"
            ),
        },
    ]