"""Power and grid stress scenario library."""

POWER_SCENARIOS = {
    "Normal Operations": {
        "cocktail_name": "The Steady Current",
        "grid_stress_score": 10,
        "factor_shock_hints": {"Mkt-RF": 0, "HML": 0, "VIX": 0},
        "sectors_impacted": ["Utilities (stable)", "Data center REITs (normal)"],
        "description": "Baseline grid and power market conditions.",
    },
    "Texas Summer Heat Wave": {
        "cocktail_name": "The ERCOT Squeeze",
        "grid_stress_score": 75,
        "factor_shock_hints": {"Mkt-RF": -5, "HML": 8, "VIX": 15},
        "sectors_impacted": [
            "Utilities / Independent Power Producers (margin pressure + spot spikes)",
            "Data centers in ERCOT (cooling cost surge)",
            "Industrials (curtailment risk)",
            "Renewables (high output but grid congestion)",
        ],
        "description": (
            "Extreme heat drives record cooling load. ERCOT-style tight reserves, "
            "spot power spikes, and data-center uptime risk."
        ),
    },
    "AI Data Center Demand Spike": {
        "cocktail_name": "The GPU Grid Drain",
        "grid_stress_score": 65,
        "factor_shock_hints": {"Mkt-RF": -3, "SMB": 5, "HML": 10, "VIX": 12},
        "sectors_impacted": [
            "Hyperscaler capex beneficiaries (NVDA supply chain)",
            "Utilities in VA/TX/OR data-center corridors",
            "Power equipment (transformers, switchgear)",
            "Commercial real estate / data-center REITs",
        ],
        "description": (
            "Rapid AI workload growth strains regional grids. Long-lead power contracts "
            "and utility capex accelerate; energy-intensive compute becomes a portfolio factor."
        ),
    },
    "Regional Blackout (Grid Failure)": {
        "cocktail_name": "The Blackout Bitter",
        "grid_stress_score": 95,
        "factor_shock_hints": {"Mkt-RF": -12, "SMB": -8, "HML": -5, "VIX": 35},
        "sectors_impacted": [
            "Utilities (liability + regulatory scrutiny)",
            "Insurance (business interruption claims)",
            "Industrials & manufacturing (production halt)",
            "Retail & logistics (supply chain disruption)",
        ],
        "description": (
            "Multi-day regional outage from equipment failure or cascading fault. "
            "Analogous to major weather-driven blackouts with sharp near-term growth hit."
        ),
    },
    "Renewable Intermittency Shock": {
        "cocktail_name": "The Duck Curve",
        "grid_stress_score": 55,
        "factor_shock_hints": {"Mkt-RF": -2, "HML": 6, "CMA": 5},
        "sectors_impacted": [
            "Solar/wind operators (negative pricing hours)",
            "Gas peaker plants (margin uplift)",
            "Battery storage developers",
            "Grid operators (balancing costs)",
        ],
        "description": (
            "Low wind + evening demand ramp forces expensive peaker dispatch. "
            "Highlights transition risk in power-heavy portfolios."
        ),
    },
}


def get_power_scenario_names():
    return list(POWER_SCENARIOS.keys())


def get_power_scenario(name: str):
    return POWER_SCENARIOS.get(name, POWER_SCENARIOS["Normal Operations"])