# Shocktail.ai

**AI Market Intelligence Platform** — scenario research, alternative data, and grounded Research Copilot.

[![GitHub](https://img.shields.io/badge/GitHub-shocktail--ai-181717?logo=github)](https://github.com/Aramina6/shocktail-ai)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://realtime-disasters-monitoring-cxephdtyww4jf2dwjunnhq.streamlit.app/)

---

## Positioning

**Shocktail** is an AI market intelligence platform for scenario research — interactive
what-if analysis with quant-grounded narratives and alternative data signals.

| Capability | Status |
|------------|--------|
| Factor stress scenarios | ✅ Live |
| Grounded Research Copilot | ✅ Live |
| Alternative data (power, geo, insurance) | ✅ Live |
| Document search (SEC filings) | 🔜 Roadmap |

---

## Platform modules

| Module | Description |
|--------|-------------|
| **Scenario Intelligence** | Fama-French factor stress + historical crisis library |
| **Research Copilot** | Analyst-grade AI narratives grounded in live context |
| **Alternative Data** | Power grid, geophysical, insurance loss signals |

---

## Quick start

```bash
git clone https://github.com/Aramina6/shocktail-ai.git
cd shocktail-ai
pip install -r requirements.txt
copy .streamlit\secrets.toml.example .streamlit\secrets.toml
# Add GROQ_API_KEY
streamlit run app.py
```

**Deploy (operator):** add `GROQ_API_KEY` in Streamlit Cloud → Settings → Secrets. End users never see this.

---

## Docs

- [Product Offering](docs/PRODUCT.md)
- [Roadmap](docs/ROADMAP.md)
- [Brand](brand/BRAND.md)

---

*Educational use only — not investment advice.*