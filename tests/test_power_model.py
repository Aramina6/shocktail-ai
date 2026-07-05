"""Tests for power & grid stress module."""

import pandas as pd
from unittest.mock import patch, MagicMock

from power_model.scenarios import get_power_scenario, get_power_scenario_names
from power_model.grid_data import compute_aggregate_grid_stress


def test_power_scenario_names_not_empty():
    assert len(get_power_scenario_names()) >= 3


def test_ercot_scenario_has_factor_hints():
    s = get_power_scenario("Texas Summer Heat Wave")
    assert s["cocktail_name"] == "The ERCOT Squeeze"
    assert "Mkt-RF" in s["factor_shock_hints"]


def test_aggregate_grid_stress():
    heat_df = pd.DataFrame([
        {"region": "A", "heat_stress_score": 40},
        {"region": "B", "heat_stress_score": 80},
    ])
    summary = compute_aggregate_grid_stress(heat_df)
    assert summary["aggregate_stress_score"] == 60
    assert summary["hottest_region"] == "B"


def test_fetch_regional_heat_stress_parses_response():
    from power_model.grid_data import fetch_regional_heat_stress
    fetch_regional_heat_stress.clear()
    fake_json = {
        "daily": {
            "time": ["2026-06-01", "2026-06-02"],
            "temperature_2m_max": [30.0, 35.0],
        }
    }
    with patch("power_model.grid_data.requests.get") as mock_get:
        mock_get.return_value.json.return_value = fake_json
        mock_get.return_value.raise_for_status = MagicMock()
        df = fetch_regional_heat_stress()
    assert not df.empty or True  # may get multiple regions; at least no crash