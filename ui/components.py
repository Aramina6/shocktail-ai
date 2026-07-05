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
        The accessible intelligence layer for teams who need AlphaSense-class insight
        without enterprise contracts.
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
        st.metric("AI Engine", "Groq", help="Free-tier LLM with grounded context")


def render_vs_alphasense():
    st.markdown('<div class="st-section-label">Competitive Position</div>', unsafe_allow_html=True)
    st.markdown(
        """
<div class="st-compare-grid">
    <div class="st-compare-card">
        <h4>Traditional platforms (AlphaSense, Bloomberg)</h4>
        <ul>
            <li>$10K–$30K+ per seat annually</li>
            <li>Document search across filings & transcripts</li>
            <li>Enterprise sales cycles & opaque pricing</li>
            <li>Limited interactive scenario stress testing</li>
            <li>Generic AI summaries without factor grounding</li>
        </ul>
    </div>
    <div class="st-compare-card shocktail">
        <h4>Shocktail.ai — scenario intelligence wedge</h4>
        <ul>
            <li>Free tier → $99/mo pro (planned) — 100× more accessible</li>
            <li>Interactive factor stress + crisis scenario library</li>
            <li>Research Copilot grounded in live quantitative context</li>
            <li>Alternative data: power grid, geophysical, insurance losses</li>
            <li>Transparent methodology — every number traceable to source</li>
        </ul>
    </div>
</div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
**Our wedge:** AlphaSense wins on document corpus search at enterprise scale.
**Shocktail wins** on interactive *what-if* scenario research, quant-grounded AI narratives,
and alternative risk signals — the workflow analysts use *after* they find the document.
        """
    )


def render_alt_data_selector() -> str:
    """Sidebar-style alt data picker; returns selection key."""
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