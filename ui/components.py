"""Reusable UI components for Shocktail intelligence platform."""

from __future__ import annotations

import streamlit as st


def render_hero():
    st.markdown(
        """
<div class="st-hero">
    <div class="st-section-label">Market Intelligence Platform</div>
    <h1>Shocktail.ai</h1>
    <p class="tagline">
        AI-powered scenario research, factor stress intelligence, and alternative data —
        grounded in quantitative models, not hallucinated summaries.
    </p>
    <p class="positioning">
        Professional-grade market intelligence for analysts, portfolio managers, and risk teams.
    </p>
    <div class="st-stat-row">
        <span class="st-stat-pill"><strong>Live</strong> Factor stress engine</span>
        <span class="st-stat-pill"><strong>Live</strong> Research Copilot</span>
        <span class="st-stat-pill"><strong>Live</strong> Infrastructure signals</span>
        <span class="st-stat-pill"><strong>Open</strong> Fama-French · FRED · USGS</span>
    </div>
</div>
        """,
        unsafe_allow_html=True,
    )


def render_platform_stats():
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Data Sources", "12+", help="Open government & academic feeds")
    with c2:
        st.metric("Scenario Library", "6+", help="Historical crisis presets")
    with c3:
        st.metric("Alt Data Modules", "5", help="Power, geophysical, insurance")
    with c4:
        st.metric("AI Engine", "Groq", help="Grounded LLM with live context")


def render_value_props():
    st.markdown('<div class="st-section-label">Platform capabilities</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            """
**Scenario Intelligence**
- Historical crisis presets + custom factor shocks
- Fama-French covariance propagation
- Sector exposure mapping

**Research Copilot**
- Analyst-grade narratives from live context
- Executive summaries & sector memos
- Every claim tied to quantitative inputs
            """
        )
    with c2:
        st.markdown(
            """
**Alternative Data**
- Power grid & infrastructure stress
- Geophysical event signals
- Insurance loss aggregates (US)

**Transparent by design**
- Open data sources with methodology docs
- No black-box model outputs
- Educational / research use
            """
        )


def render_alt_data_selector() -> str:
    return st.selectbox(
        "Signal feed",
        options=[
            "none",
            "power_grid",
            "earthquakes",
            "cyclones",
            "space_weather",
            "flood_insurance",
        ],
        format_func=lambda x: {
            "none": "— No alt data attached —",
            "power_grid": "⚡ Infrastructure · Power & Grid",
            "earthquakes": "🌍 Geophysical · Seismic Activity",
            "cyclones": "🌀 Geophysical · Tropical Systems",
            "space_weather": "☄️ Geophysical · Space Weather",
            "flood_insurance": "🏛️ Insurance · Flood Losses (US)",
        }[x],
        help="Attach alternative data signals to enrich Research Copilot context.",
    )