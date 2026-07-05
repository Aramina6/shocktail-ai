# Shocktail.ai 🍸

**Market shocks, shaken — not stirred.**

Interactive scenario intelligence for advisors, portfolio managers, and risk teams. Mix factor shocks, stress portfolios, get AI narratives grounded in real math.

[![GitHub](https://img.shields.io/badge/GitHub-shocktail--ai-181717?logo=github)](https://github.com/Aramina6/shocktail-ai)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://realtime-disasters-monitoring-cxephdtyww4jf2dwjunnhq.streamlit.app/)

**Topics:** `fintech` · `quantitative-finance` · `risk-management` · `stress-testing` · `streamlit` · `llm` · `ai-copilot` · `startup`

---

## What It Does

| Pillar | Description |
|--------|-------------|
| **Scenario Bar** | Historical crisis presets + custom factor shock mixer (Fama-French + vol) |
| **Risk Copilot** | Free LLM (Groq/HF/Ollama) narratives grounded in your live scenario |
| **Context Modules** | Optional layers — physical hazards today; transition, power, GPU on roadmap |

**Not** a disaster-only dashboard. **Not** generic AI portfolio advice. A **scenario bar** for market risk.

---

## Scenario Cocktails (Presets)

| Cocktail | Crisis |
|----------|--------|
| The Lehman Last Call | 2008 GFC |
| The Lockdown Lime | COVID crash |
| The Stagflation Sour | 2022 inflation + war |
| The OPEC Old Fashioned | Oil supply shock |
| Build Your Own | Custom sliders |

---

## Quick Start

```bash
git clone https://github.com/Aramina6/shocktail-ai.git
cd shocktail-ai
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -r requirements.txt

# Free LLM: copy and add Groq key
copy .streamlit\secrets.toml.example .streamlit\secrets.toml

streamlit run app.py
```

1. Open **Scenario Bar** → pick a cocktail
2. Adjust factor betas
3. Open **Risk Copilot** → "Explain Scenario" or ask anything

---

## Startup Docs

- [Product Offering](docs/PRODUCT.md) — ICP, tiers, GTM, YC pitch
- [Roadmap](docs/ROADMAP.md) — transition risk, power modeling, GPU forecasting
- [Brand Guide](brand/BRAND.md) — voice, cocktail naming, visual direction

---

## Architecture

```
app.py                 # Shocktail UI orchestrator
factor_model/          # Scenario Bar engine (FF5, scenarios, stress)
llm/                   # Grounded copilot (Groq → HF → Ollama)
physical_hazard/       # Context module (legacy, de-emphasized)
docs/                  # Product + methodology
```

---

## Roadmap Highlights

- **Now:** Scenario Bar + Copilot + market factors
- **Q4 2026:** Portfolio upload, Monte Carlo, white-label PDF
- **2027:** Transition risk (NGFS-style pathways)
- **2027–28:** Power/grid stress, GPU token economics forecasting

---

## Tests

```bash
pytest tests/ -v
```

---

*Educational use only — not investment advice.*

**Shocktail.ai** — shake the factors, serve the insight.