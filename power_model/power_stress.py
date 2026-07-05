"""Power & grid stress UI module."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from .grid_data import (
    compute_aggregate_grid_stress,
    fetch_electricity_cpi_trend,
    fetch_regional_heat_stress,
)
from .scenarios import get_power_scenario, get_power_scenario_names


def _save_power_context(
    *,
    selected_scenario: str,
    scenario: dict,
    grid_summary: dict,
    elec_df: pd.DataFrame,
):
    yoy = None
    if not elec_df.empty and "yoy_pct" in elec_df.columns:
        val = elec_df["yoy_pct"].iloc[-1]
        if pd.notna(val):
            yoy = float(val)

    st.session_state.power_context = {
        "power_scenario": selected_scenario,
        "cocktail_name": scenario.get("cocktail_name", ""),
        "grid_stress_score": scenario.get("grid_stress_score"),
        "description": scenario.get("description", ""),
        "sectors_impacted": scenario.get("sectors_impacted", []),
        "factor_shock_hints": scenario.get("factor_shock_hints", {}),
        "live_grid_summary": grid_summary.get("summary"),
        "hottest_region": grid_summary.get("hottest_region"),
        "aggregate_heat_stress": grid_summary.get("aggregate_stress_score"),
        "electricity_cpi_latest": (
            float(elec_df["electricity_cpi"].iloc[-1]) if not elec_df.empty else None
        ),
        "electricity_cpi_yoy_pct": yoy,
    }


def render():
    st.subheader("⚡ Power & Grid Stress")
    st.caption(
        "Live heat stress at major grid hubs + electricity CPI trend + stylized power scenarios. "
        "Free data: Open-Meteo, FRED."
    )

    heat_df = fetch_regional_heat_stress()
    elec_df = fetch_electricity_cpi_trend()
    grid_summary = compute_aggregate_grid_stress(heat_df)

    c1, c2, c3 = st.columns(3)
    with c1:
        score = grid_summary.get("aggregate_stress_score")
        st.metric("Live Heat Stress (avg)", f"{score}/100" if score is not None else "N/A")
    with c2:
        st.metric("Hottest Hub", grid_summary.get("hottest_region") or "N/A")
    with c3:
        if not elec_df.empty and "yoy_pct" in elec_df.columns:
            yoy = elec_df["yoy_pct"].iloc[-1]
            st.metric("Electricity CPI YoY", f"{yoy:.1f}%" if pd.notna(yoy) else "N/A")
        else:
            st.metric("Electricity CPI YoY", "N/A")

    if not heat_df.empty:
        fig = px.bar(
            heat_df.sort_values("heat_stress_score", ascending=True),
            x="heat_stress_score",
            y="region",
            orientation="h",
            color="heat_stress_score",
            color_continuous_scale="Oranges",
            title="Regional Heat Stress (0–100)",
            labels={"heat_stress_score": "Stress score", "region": ""},
        )
        fig.update_layout(height=320, coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(heat_df, use_container_width=True, hide_index=True)

    if not elec_df.empty:
        fig2 = px.line(
            elec_df, x="date", y="electricity_cpi",
            title="US Electricity CPI (FRED — CUUR0000SEHE)",
        )
        fig2.update_layout(height=260)
        st.plotly_chart(fig2, use_container_width=True)

    st.divider()
    st.markdown("**Power Stress Scenario**")
    names = get_power_scenario_names()
    selected = st.selectbox("Choose power scenario", names, key="power_scenario_select")
    scenario = get_power_scenario(selected)

    cocktail = scenario.get("cocktail_name", "")
    if cocktail:
        st.info(f"**{cocktail}** — {scenario['description']}")
    st.markdown(f"**Grid stress score:** {scenario['grid_stress_score']}/100")
    st.markdown("**Sectors impacted:**")
    for s in scenario.get("sectors_impacted", []):
        st.markdown(f"- {s}")

    hints = scenario.get("factor_shock_hints", {})
    if hints:
        st.markdown("**Suggested market factor hints (%):**")
        st.write(", ".join(f"{k}: {v:+d}" for k, v in hints.items()))

    _save_power_context(
        selected_scenario=selected,
        scenario=scenario,
        grid_summary=grid_summary,
        elec_df=elec_df,
    )

    st.caption(
        "Power context feeds the Risk Copilot. Pair with Scenario Bar for compound shocks."
    )