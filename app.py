# app.py
"""
Shocktail.ai — Main entry point.

Scenario-first layout:
- Scenario Bar (factor stress testing)
- Risk Copilot (grounded LLM)
- Context Modules (physical hazards + future: transition, power, GPU)
"""

import streamlit as st

from factor_model import market_factor_stress
from llm import copilot
from physical_hazard import earthquakes, tropical_cyclones, space_hazards, nfip_insurance
from power_model import power_stress


st.set_page_config(
    page_title="Shocktail.ai | Market shocks, shaken — not stirred",
    page_icon="🍸",
    layout="wide",
)

st.markdown(
    """
    <style>
    .shocktail-tagline { color: #888; font-size: 1.05rem; margin-top: -0.5rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("🍸 Shocktail.ai")
    st.caption("Market shocks, shaken — not stirred.")

    st.divider()
    st.markdown("**Context Modules**")
    st.caption("Optional data layers — not the core product")

    context_choice = st.radio(
        "Attach context",
        options=[
            "None",
            "Power & Grid Stress",
            "Physical — Earthquakes",
            "Physical — Cyclones",
            "Physical — Space Weather",
            "Physical — Flood Insurance (US)",
        ],
        index=0,
        help="Context informs the copilot. Market scenarios work without it.",
    )

    st.divider()
    copilot.render_sidebar_settings()

    st.divider()
    with st.expander("Product roadmap"):
        st.markdown(
            """
**Live:** Scenario Bar · Risk Copilot · Power & Grid · Market factors

**Coming:**
- Portfolio upload + Monte Carlo
- Transition risk pathways
- GPU / token forecasting
            """
        )


st.title("Shocktail.ai")
st.markdown(
    '<p class="shocktail-tagline">Mix market shocks. Stress your factors. '
    "Get AI narratives grounded in the math.</p>",
    unsafe_allow_html=True,
)

scenario_tab, copilot_tab, about_tab = st.tabs([
    "🍸 Scenario Bar",
    "🤖 Risk Copilot",
    "ℹ️ Product",
])

with scenario_tab:
    market_factor_stress.render()

with copilot_tab:
    copilot.render()

with about_tab:
    st.markdown(
        """
### What is Shocktail?

**Shocktail.ai** is a scenario intelligence platform for advisors, portfolio managers,
and risk teams. Shake factor shocks like a cocktail — historical crises, custom mixes,
or AI-assisted blends — and see portfolio impact with explainable narratives.

### Product tiers (planned)

| Tier | For |
|------|-----|
| **Shaker** (Free) | Try scenarios + copilot |
| **Stirred** ($99/mo) | White-label client reports |
| **Shaken** ($499/mo) | Teams + API |
| **Distillery** | Fintech embed |

### Roadmap modules

1. **Scenario Bar** — market factor stress *(live)*
2. **Portfolio Shaker** — CSV upload, Monte Carlo, PDF export
3. **Transition Risk** — carbon pathways, policy shocks
4. **Power & Grid** — data-center / utility stress *(live)*
5. **GPU & Tokens** — AI infra cost forecasting

Physical hazard data is one **context module** — not our identity.

*Educational use only — not investment advice.*

[Product doc](docs/PRODUCT.md) · [Roadmap](docs/ROADMAP.md) · [Brand](brand/BRAND.md)
        """
    )


if context_choice == "Power & Grid Stress":
    with st.expander("⚡ Power & Grid Stress — context", expanded=True):
        power_stress.render()
elif context_choice == "Physical — Earthquakes":
    with st.expander("🌍 Earthquakes (USGS) — context", expanded=False):
        earthquakes.render()
elif context_choice == "Physical — Cyclones":
    with st.expander("🌀 Cyclones (NOAA) — context", expanded=False):
        tropical_cyclones.render()
elif context_choice == "Physical — Space Weather":
    with st.expander("☄️ Space Weather — context", expanded=False):
        space_hazards.render()
elif context_choice == "Physical — Flood Insurance (US)":
    with st.expander("🇺🇸 NFIP / FEMA — context", expanded=False):
        nfip_insurance.render()

st.caption("Shocktail.ai · Scenario intelligence · Open data · Shaken, not stirred")