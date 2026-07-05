# Shocktail.ai — Product Offering

**Tagline:** *Market shocks, shaken — not stirred.*

**One-liner:** Interactive scenario lab for portfolio managers, advisors, and risk teams who need explainable stress tests — market, transition, and compute — with AI narratives grounded in real math.

---

## The Problem

Risk teams and advisors face the same cocktail of pain:

| Pain | Who feels it |
|------|----------------|
| Clients ask "what if recession / war / AI bubble pops?" and answers take days | RIAs, wealth advisors |
| Bloomberg + internal models cost six figures; ChatGPT hallucinates | Mid-market funds, family offices |
| Climate + transition + AI infra risk are siloed in different tools | Insurers, corporates, fintech |
| Scenario libraries are static PDFs, not live or composable | Everyone doing stress testing |

**Shocktail** serves the gap: **quant-grounded scenario intelligence** that's fast, funny enough to remember, and cheap enough to start free.

---

## What Shocktail Is (and Isn't)

| Shocktail **is** | Shocktail **is not** |
|------------------|----------------------|
| A scenario bar for mixing market shocks | A catastrophe modeling replacement (Verisk/RMS) |
| Factor + macro + narrative stress testing | Generic portfolio optimization (robo-advisor) |
| AI copilot grounded in your numbers | ChatGPT with a finance skin |
| Modular risk context (physical, transition, compute) | A disaster-only dashboard |
| PLG → API → enterprise wedge | Consulting dressed as software |

**Positioning:** The **scenario layer** between spreadsheets and Bloomberg — shaken with real factors, garnished with LLM explanations.

---

## Product Pillars

### 1. Scenario Bar (Core — live today)
Mix market shocks like a cocktail:
- Historical presets (GFC, COVID, inflation shock, oil crisis)
- Custom factor sliders (Fama-French + vol proxy)
- Portfolio factor betas → instant impact + vol estimate
- **Next:** Holdings upload (CSV/tickers), Monte Carlo paths, drawdown charts

### 2. Risk Copilot (Core — live today)
Free-tier LLM (Groq / HF / Ollama) that only speaks from **live scenario context**:
- Client-ready summaries
- Sector rotation narratives
- Hedging ideas (educational)
- **Next:** Multi-turn scenario building ("add 100bps Fed hike to current mix")

### 3. Context Modules (Supporting — expandable)
Optional data layers that **inform** scenarios, not define the product:

| Module | Status | Role in Shocktail |
|--------|--------|-------------------|
| Market factors (FF5) | Live | Core shaker |
| Physical hazards | Live | One garnish — acute event context |
| Transition risk | Planned | NGFS-style pathways, carbon price shocks |
| Power & grid stress | Planned | Data-center / utility exposure modeling |
| GPU & token economics | Planned | AI infra cost & capacity forecasting |

Physical risk stays in the menu — it's not the main course.

### 4. Scenario Studio (Roadmap — not MVP hero)
Portfolio upload, parameterized scenarios ("Fed +100bps + tech recession"), Monte Carlo, efficient frontier comparisons. Builds on Scenario Bar + Copilot — shipped in Phase 2, not repositioned as the whole company.

---

## Ideal Customer Profiles (ICP)

### Primary (Year 1 revenue)
**Independent RIAs & small wealth teams (1–20 people)**
- 300K+ in US alone
- Need client-facing stress narratives weekly
- Pay $99–499/mo for white-label reports
- GTM: PLG free reports → paid seats

### Secondary (Year 1–2)
**Fintech / neobank product teams**
- Need embedded "what-if" differentiation
- Pay API usage or rev-share
- GTM: docs-first sandbox → integration call

### Tertiary (Year 2+)
**Mid-market insurers, corporate treasury, AI infra operators**
- Transition + compute modules unlock these buyers
- $2K–50K/mo contracts
- GTM: regulatory wedge + pilot → annual

---

## Product Tiers (Planned)

| Tier | Price | Includes |
|------|-------|----------|
| **Shaker** (Free) | $0 | 3 scenarios/mo, 1 copilot thread, watermarked PDF, community scenarios |
| **Stirred** (Pro) | $99/mo | Unlimited scenarios, white-label client PDFs, CSV upload (10 holdings), email delivery |
| **Shaken** (Team) | $499/mo | 5 seats, shared scenario library, API access (1K calls), custom branding |
| **Distillery** (API) | Usage-based | Embeddable stress API for fintech/insurtech, SLA, webhooks |
| **Enterprise** | Custom | SSO, audit logs, on-prem Ollama, transition + compute modules, dedicated scenarios |

*Pricing is illustrative for YC / investor conversations — validate with 20 advisor interviews.*

---

## Differentiation (Why Shocktail Wins)

```
                    Generic AI          Shocktail
                    ──────────          ─────────
Grounded math       ❌                  ✅ Factor shocks + cov matrix
Composable shocks   ❌                  ✅ Scenario Bar mixing
Explainability      ⚠️                  ✅ Methodology docs + context panel
Price               $20/mo chat         Free → $99/mo pro
Memorable brand     ❌                  ✅ "Shaken, not stirred"
Future moat         —                   Transition + GPU token modules
```

**Moat over time:** Living scenario library + client report history + proprietary calibration from transition/compute modules.

---

## Competitive Landscape

| Player | Weakness Shocktail exploits |
|--------|----------------------------|
| Bloomberg / FactSet | Expensive, not narrative-friendly for clients |
| Koyfin / TradingView | Charts, not stress narratives |
| ChatGPT / Magnifi | No grounded factor math |
| Jupiter / Cervest | Enterprise physical-only, six-figure |
| Internal bank models | Opaque, slow, no PLG |

---

## GTM Motion

### Phase 1: PLG (Months 0–6)
1. Free Streamlit app → shocktail.ai (or Streamlit subdomain)
2. "Scenario of the week" email from live macro events
3. Shareable shock report links (viral loop among advisors)
4. Metric: **reports generated / week**

### Phase 2: Pro conversion (Months 6–12)
1. White-label PDF + CRM export (Wealthbox, Redtail)
2. Case study: "How [RIA] answers client crash questions in 30 seconds"
3. Metric: **free → paid conversion > 3%**

### Phase 3: API & embed (Year 2)
1. `POST /v1/shock` — holdings + scenario → narrative + metrics
2. Fintech design partners (2–3)
3. Metric: **API calls → $/1K calls**

### Phase 4: Enterprise modules (Year 2–3)
1. Transition risk pathway shocks (NGFS-inspired, open data)
2. Power grid / data-center stress (EIA, grid operators)
3. GPU token usage forecasting (pricing APIs, utilization curves)

---

## YC-Style Pitch (Draft)

> **Shocktail.ai** — Market shocks, shaken not stirred.
>
> Advisors and mid-market risk teams can't afford Bloomberg or Verisk, and ChatGPT hallucinates on portfolio stress. Shocktail is an interactive scenario bar: mix factor shocks, run stress on real holdings, get AI narratives grounded in the math. We're starting with 50 paying advisors and expanding into transition risk and AI compute forecasting — the scenario layer for the $40T wealth management market.
>
> **Founder:** Built live risk dashboards (USGS, FEMA, Fama-French), LLM copilots, and production QA for AI platforms.

---

## Success Metrics

| Stage | North Star | Supporting |
|-------|------------|------------|
| MVP | Weekly active scenario runs | Copilot messages / session |
| PMF | 50 paying Pro users | NPS > 40, < 5% churn |
| Scale | $500K ARR | 2 API embed partners |
| Series A story | $2M ARR, 3 modules live | Transition + compute differentiated |

---

## Legal & Trust

- All outputs labeled **educational / illustrative** — not investment advice
- Methodology transparent (`docs/DATA_SOURCES_AND_METHODOLOGY.md`)
- API keys in Streamlit secrets; no portfolio data stored in MVP without consent
- Enterprise: SOC2 path, anonymization for LLM context

---

*Shocktail.ai — shake the factors, serve the insight.*