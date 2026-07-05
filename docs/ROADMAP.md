# Shocktail.ai — Product Roadmap

Shocktail is a **broad scenario intelligence platform**. Physical hazard context is one module — not the product identity. This roadmap sequences market → narrative → portfolio → transition → compute.

---

## Vision Arc

```
2026 H1   Scenario Bar + Copilot (market shocks)
2026 H2   Portfolio upload + Monte Carlo + PDF export
2027 H1   Transition risk module (NGFS-style pathways)
2027 H2   Power & grid stress modeling
2028      GPU / token economics forecasting
```

---

## Phase 0 — Foundation (Done / In Progress)

**Theme:** *Prove the shaker works.*

| Item | Status |
|------|--------|
| Fama-French factor stress + scenario library | ✅ Live |
| Free LLM copilot (Groq → HF → Ollama) | ✅ Live |
| Grounded context from session state | ✅ Live |
| Physical hazard context module | ✅ Live (de-emphasized in UI) |
| Unit tests + CI | ✅ Live |
| Shocktail.ai branding | ✅ This sprint |

**Exit criteria:** 10 advisor interviews, 100 scenario runs from strangers.

---

## Phase 1 — Scenario Bar MVP (Q3 2026)

**Theme:** *The bar is open.*

| Feature | Description |
|---------|-------------|
| Named scenario cocktails | Preset combos: "Stagflation Sour", "AI Hangover", "Soft Landing Spritz" |
| Multi-shock mixer | Stack macro shocks (rates, oil, vol) on factor base |
| Shareable shock links | URL encodes scenario params |
| Copilot scenario builder | "Add 100bps hike to current mix" → updates sliders |
| Email capture | 3 free shocks/mo → list building |

**Not in scope:** Full portfolio optimization, options greeks, prime brokerage integration.

**Exit criteria:** 500 MAU, 15 Pro waitlist signups.

---

## Phase 2 — Portfolio Shaker (Q4 2026 – Q1 2027)

**Theme:** *Holdings in, shaken report out.*

| Feature | Description |
|---------|-------------|
| CSV / ticker upload | Up to 50 holdings, yfinance prices |
| Factor regression per holding | OLS vs FF5 → portfolio-level betas auto-fill |
| Monte Carlo stress paths | 1K–10K sims, correlated factor draws |
| Plotly visuals | Drawdown fan, distribution overlay, scenario comparison |
| White-label PDF export | Pro tier — client-ready Shocktail report |
| Sensitivity tornado | Which factors drive 80% of loss |

**Exit criteria:** 50 paying Stirred ($99/mo) users OR 1 fintech pilot.

---

## Phase 3 — Transition Risk Module (Q2–Q3 2027)

**Theme:** *Carbon in the mix.*

| Feature | Description |
|---------|-------------|
| NGFS-inspired pathways | Orderly / disorderly / hot house (open parameter sets) |
| Carbon price shock factor | Correlated with energy, utilities, materials |
| Sector transition betas | Map holdings to emission-intensive sectors |
| Policy scenario library | IRA rollback, EU CBAM tightening, etc. |
| Copilot transition narratives | "What does Net Zero 2050 do to this portfolio?" |

**Data (free / open):**
- NGFS scenario documentation (parameters)
- EPA / IEA open datasets where available
- FRED for energy price series

**Buyer unlock:** Corporate treasury, ESG teams, insurers.

---

## Phase 4 — Power & Grid Stress (Q4 2027)

**Theme:** *Data centers need a drink too.*

| Feature | Description |
|---------|-------------|
| Regional grid stress index | Heat + demand + outage proxies (EIA, open utility data) |
| Data-center exposure mapping | REITs, hyperscaler suppliers, utility holdings |
| Power price shock scenarios | Correlated with AI infra and industrial factors |
| Compound scenarios | "Texas heat wave + AI demand spike + rate shock" |

**Buyer unlock:** AI infra investors, real asset funds, corporate facilities.

---

## Phase 5 — GPU & Token Economics (2028)

**Theme:** *Forecast the hangover before the bill arrives.*

| Feature | Description |
|---------|-------------|
| GPU hour price curves | Public cloud pricing APIs + historical scrape |
| Token usage forecasting | User inputs workload → cost / capacity projection |
| AI capex shock scenarios | "What if inference costs 3x?" |
| Supply constraint factors | HBM shortage, fab delay → sector impacts |
| Copilot infra narratives | CFO-friendly summaries |

**Buyer unlock:** AI startups, infra funds, corporate AI budget owners.

**Differentiation:** Almost nobody connects **token economics → portfolio factor shocks** in one interactive tool.

---

## Module Priority Matrix

| Module | Revenue proximity | Build effort | Strategic moat |
|--------|-------------------|--------------|----------------|
| Scenario Bar | ★★★★★ | Low (done) | Medium |
| Risk Copilot | ★★★★★ | Low (done) | Medium |
| Portfolio Shaker | ★★★★☆ | Medium | High |
| Transition risk | ★★★☆☆ | Medium | High |
| Power / grid | ★★★☆☆ | High | Very high |
| GPU / tokens | ★★★★☆ | High | Very high |
| Physical hazards | ★★☆☆☆ | Done | Low (supporting) |

---

## What We Deprioritize

- **QuantScenario Studio as brand hero** — it's Phase 2 engineering, not company identity
- **Physical-only positioning** — supporting context, not TAM story
- **Retail trader features** — low willingness to pay
- **Full CAT modeling** — can't compete with Verisk on stochastic events

---

## Technical Architecture (Target)

```
┌─────────────────────────────────────────────────────────┐
│                    Shocktail.ai UI                       │
│  Scenario Bar │ Copilot │ Portfolio │ Context Modules   │
└────────────┬────────────────────────────────────────────┘
             │
┌────────────▼────────────────────────────────────────────┐
│                  Scenario Engine                         │
│  factor shocks │ cov matrix │ MC sim │ sensitivity      │
└────────────┬────────────────────────────────────────────┘
             │
┌────────────▼────────────────────────────────────────────┐
│              Context Adapters (plugins)                  │
│  market │ transition │ power │ gpu │ physical (legacy)  │
└────────────┬────────────────────────────────────────────┘
             │
┌────────────▼────────────────────────────────────────────┐
│           LLM Layer (grounded, free-tier)                │
│  Groq → HF → Ollama │ context builder │ PDF gen         │
└─────────────────────────────────────────────────────────┘
```

---

*Last updated: July 2026*