"""Scenario Library for Market Factor Stress Testing."""

SCENARIOS = {
    "Custom (Manual Shocks)": {
        "cocktail_name": "Build Your Own",
        "factor_shocks": {
            "Mkt-RF": 0,
            "SMB": 0,
            "HML": 0,
            "RMW": 0,
            "CMA": 0,
            "VIX": 0,
        },
        "industries_impacted": ["All sectors (user-defined)"],
        "description": "Start with zero shocks and manually adjust factors using the sliders.",
    },
    "Iran-Iraq War (1980-88) / Major Middle East Oil Shock": {
        "cocktail_name": "The OPEC Old Fashioned",
        "factor_shocks": {
            "Mkt-RF": -22,
            "SMB": 8,
            "HML": 25,
            "RMW": -5,
            "CMA": -12,
            "VIX": 45,
        },
        "industries_impacted": [
            "Energy (strongly positive - oil price spike)",
            "Financials (mixed - credit risk up, some lenders benefit)",
            "Consumer Discretionary (negative - higher energy costs hurt spending)",
            "Transportation & Airlines (strongly negative)",
            "Utilities (mixed - higher input costs)",
            "Materials (positive if commodity exposure)",
        ],
        "description": (
            "Prolonged conflict caused major oil supply disruptions and price spikes. "
            "Energy stocks outperformed while broad markets sold off."
        ),
    },
    "1990 Gulf War (Iraq invades Kuwait)": {
        "cocktail_name": "The Desert Storm",
        "factor_shocks": {
            "Mkt-RF": -18,
            "SMB": 5,
            "HML": 18,
            "RMW": -3,
            "CMA": -8,
            "VIX": 35,
        },
        "industries_impacted": [
            "Energy",
            "Aerospace & Defense (positive)",
            "Financials (mixed)",
            "Consumer Staples (relative outperformer)",
        ],
        "description": (
            "Sudden invasion led to sharp oil price spike and brief recession fears. "
            "Strong rotation into Value and Energy."
        ),
    },
    "2008 Global Financial Crisis": {
        "cocktail_name": "The Lehman Last Call",
        "factor_shocks": {
            "Mkt-RF": -45,
            "SMB": -25,
            "HML": -15,
            "RMW": -20,
            "CMA": -10,
            "VIX": 120,
        },
        "industries_impacted": [
            "Financials (devastated - banking crisis)",
            "Real Estate (collapse)",
            "Consumer Discretionary (sharp drop in spending)",
            "Industrials",
            "Energy (hit late in the crisis)",
        ],
        "description": (
            "Systemic banking and liquidity crisis. Massive negative shocks across "
            "almost all factors, especially Market and Size."
        ),
    },
    "2020 COVID-19 Crash & Recovery": {
        "cocktail_name": "The Lockdown Lime",
        "factor_shocks": {
            "Mkt-RF": -35,
            "SMB": -15,
            "HML": -25,
            "RMW": 10,
            "CMA": -5,
            "VIX": 85,
        },
        "industries_impacted": [
            "Energy (worst hit - demand collapse)",
            "Financials",
            "Industrials & Travel / Airlines (devastated)",
            "Technology (relative outperformer after initial crash)",
            "Healthcare & Consumer Staples (defensive winners)",
        ],
        "description": (
            "Sharp liquidity-driven selloff followed by unprecedented monetary and fiscal response."
        ),
    },
    "2022 Russia-Ukraine Invasion + Inflation Shock": {
        "cocktail_name": "The Stagflation Sour",
        "factor_shocks": {
            "Mkt-RF": -22,
            "SMB": -8,
            "HML": 12,
            "RMW": -8,
            "CMA": -5,
            "VIX": 40,
        },
        "industries_impacted": [
            "Energy (strong positive - commodity spike)",
            "Materials & Commodities",
            "Financials (mixed - higher rates help net interest margins)",
            "Consumer Discretionary (negative - inflation + war uncertainty)",
            "Technology Growth (negative - higher discount rates)",
        ],
        "description": (
            "Geopolitical shock combined with sudden inflation spike. Strong rotation "
            "into Value, Energy, and Commodities."
        ),
    },
}


def get_scenario_names():
    return list(SCENARIOS.keys())


def get_scenario(name: str):
    return SCENARIOS.get(name, SCENARIOS["Custom (Manual Shocks)"])