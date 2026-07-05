# app.py
"""
Shocktail.ai — AI Market Intelligence Platform

Positioning: AlphaSense-class scenario & alternative-data intelligence
for portfolio managers, analysts, and risk teams.
"""

import streamlit as st

from factor_model import market_factor_stress
from llm import copilot
from physical_hazard import earthquakes, tropical_cyclones, space_hazards, nfip_insurance
from power_model import power_stress
from ui import inject_theme, render_hero, render_platform_stats, render_vs_alphasense
from ui.components import render_alt_data_selector


st.set_page_config(
    page_title="Shocktail.ai | AI Market Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_theme()

# ── Sidebar: Intelligence Console ──────────────────────────────────────────
with st.sidebar:
    st.markdown("### Shocktail")
    st.caption("AI Market Intelligence")

    st.markdown('<div class="st-section-label">Alternative Data</div>', unsafe_allow_html=True)
    alt_data = render_alt_data_selector()

    st.divider()
    st.markdown('<div class="st-section-label">AI Engine</div>', unsafe_allow_html=True)
    copilot.render_sidebar_settings()

    st.divider()
    with st.expander("Roadmap vs AlphaSense"):
        st.markdown(
            """
**Live now**
- Scenario Intelligence (factor stress)
- Research Copilot (grounded LLM)
- Infrastructure & geophysical signals

**Building next**
- Document search (SEC filings, transcripts)
- Portfolio upload + Monte Carlo
- Transition risk & GPU/token economics
- Team workspaces + API
            """
        )

# ── Main workspace ─────────────────────────────────────────────────────────
render_hero()

overview_tab, scenario_tab, copilot_tab, platform_tab = st.tabs([
    "Overview",
    "Scenario Intelligence",
    "Research Copilot",
    "Platform",
])

with overview_tab:
    render_platform_stats()
    st.divider()
    render_vs_alphasense()
    st.divider()
    st.markdown('<div class="st-section-label">Quick start</div>', unsafe_allow_html=True)
    st.markdown(
        """
1. **Scenario Intelligence** — load a historical crisis preset or build a custom shock
2. **Attach alt data** — power grid, geophysical, or insurance signals (sidebar)
3. **Research Copilot** — generate analyst-grade narratives grounded in live numbers
        """
    )

with scenario_tab:
    market_factor_stress.render()

with copilot_tab:
    copilot.render()

with platform_tab:
    st.markdown('<div class="st-section-label">Product vision</div>', unsafe_allow_html=True)
    st.markdown(
        """
### Shocktail.ai — the scenario intelligence layer

**Shocktail** is building the **accessible alternative to enterprise market intelligence platforms**.
Where AlphaSense dominates document search for large institutions, Shocktail owns the
**interactive scenario research workflow**: stress portfolios, attach alternative data,
and produce AI narratives that cite real factor math.

### Who it's for

| Segment | Use case |
|---------|----------|
| **Buy-side analysts** | Crisis scenario research, sector impact memos |
| **Wealth advisors / RIAs** | Client-ready stress narratives |
| **Risk managers** | Factor exposure stress testing |
| **Fintech builders** | Embeddable scenario API (roadmap) |

### Pricing (planned)

| Tier | Price | Includes |
|------|-------|----------|
| **Intelligence** (Free) | $0 | Scenarios, copilot, alt data |
| **Professional** | $99/mo | White-label reports, CSV upload |
| **Team** | $499/mo | Seats, shared research, API |
| **Enterprise** | Custom | SSO, custom data feeds, SLA |

*Educational use only — not investment advice.*
        """
    )
    render_vs_alphasense()

# ── Alternative data panel ─────────────────────────────────────────────────
if alt_data == "power_grid":
    st.markdown("---")
    st.markdown('<div class="st-section-label">Alternative Data · Infrastructure</div>', unsafe_allow_html=True)
    power_stress.render()
elif alt_data == "earthquakes":
    st.markdown("---")
    st.markdown('<div class="st-section-label">Alternative Data · Geophysical</div>', unsafe_allow_html=True)
    earthquakes.render()
elif alt_data == "cyclones":
    st.markdown("---")
    st.markdown('<div class="st-section-label">Alternative Data · Geophysical</div>', unsafe_allow_html=True)
    tropical_cyclones.render()
elif alt_data == "space_weather":
    st.markdown("---")
    st.markdown('<div class="st-section-label">Alternative Data · Geophysical</div>', unsafe_allow_html=True)
    space_hazards.render()
elif alt_data == "flood_insurance":
    st.markdown("---")
    st.markdown('<div class="st-section-label">Alternative Data · Insurance</div>', unsafe_allow_html=True)
    nfip_insurance.render()

st.markdown(
    """
<div class="st-footer">
    Shocktail.ai · AI Market Intelligence · Scenario Research · Alternative Data ·
    <a href="https://github.com/Aramina6/shocktail-ai" style="color:#D4A853">GitHub</a>
</div>
    """,
    unsafe_allow_html=True,
)