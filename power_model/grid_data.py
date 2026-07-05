"""Free open-data fetchers for power / grid stress indicators."""

from __future__ import annotations

from datetime import datetime, timedelta
from io import StringIO

import pandas as pd
import requests
import streamlit as st

# Data-center / grid stress hotspot regions
GRID_HUBS = {
    "Northern Virginia (Data Center Alley)": {"lat": 38.95, "lon": -77.45},
    "Dallas / ERCOT": {"lat": 32.78, "lon": -96.80},
    "Silicon Valley / CAISO": {"lat": 37.34, "lon": -121.89},
    "Portland / PNW Grid": {"lat": 45.52, "lon": -122.68},
}


@st.cache_data(ttl=3600)
def fetch_regional_heat_stress() -> pd.DataFrame:
    """
    Open-Meteo daily max temps for grid hub regions (free, no API key).
    Returns stress score 0-100 vs 30-day average.
    """
    end = datetime.utcnow().date()
    start = end - timedelta(days=35)
    rows = []

    for region, coords in GRID_HUBS.items():
        url = (
            "https://archive-api.open-meteo.com/v1/archive?"
            f"latitude={coords['lat']}&longitude={coords['lon']}"
            f"&start_date={start}&end_date={end}"
            "&daily=temperature_2m_max&timezone=UTC"
        )
        try:
            data = requests.get(url, timeout=20).json()
            daily = data.get("daily", {})
            dates = daily.get("time", [])
            temps = daily.get("temperature_2m_max", [])
            if not dates or not temps:
                continue

            df = pd.DataFrame({"date": pd.to_datetime(dates), "temp_c": temps})
            df = df.dropna()
            recent_avg = df["temp_c"].tail(30).mean()
            latest = df["temp_c"].iloc[-1]
            anomaly = latest - recent_avg
            # ~8°C above recent avg ≈ high stress in summer
            stress = min(100, max(0, (anomaly / 8.0) * 100))

            rows.append({
                "region": region,
                "latest_max_c": round(latest, 1),
                "avg_30d_c": round(recent_avg, 1),
                "anomaly_c": round(anomaly, 1),
                "heat_stress_score": round(stress, 0),
            })
        except Exception:
            continue

    return pd.DataFrame(rows)


@st.cache_data(ttl=86400)
def fetch_electricity_cpi_trend() -> pd.DataFrame:
    """
    US electricity CPI from FRED public CSV export (free, no API key).
    Series: CUUR0000SEHE — Electricity in CPI
    """
    url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=CUUR0000SEHE"
    try:
        resp = requests.get(url, timeout=20)
        resp.raise_for_status()
        df = pd.read_csv(StringIO(resp.text))
        df.columns = ["date", "electricity_cpi"]
        df["date"] = pd.to_datetime(df["date"])
        df["electricity_cpi"] = pd.to_numeric(df["electricity_cpi"], errors="coerce")
        df = df.dropna().tail(60)
        if len(df) >= 13:
            df["yoy_pct"] = df["electricity_cpi"].pct_change(12) * 100
        return df
    except Exception:
        return pd.DataFrame()


def compute_aggregate_grid_stress(heat_df: pd.DataFrame) -> dict:
    """Combine regional heat into one grid stress summary."""
    if heat_df.empty:
        return {
            "aggregate_stress_score": None,
            "hottest_region": None,
            "max_heat_stress": None,
            "summary": "Heat data unavailable",
        }

    max_row = heat_df.loc[heat_df["heat_stress_score"].idxmax()]
    avg_stress = heat_df["heat_stress_score"].mean()
    result = {
        "aggregate_stress_score": round(avg_stress, 0),
        "hottest_region": max_row["region"],
        "max_heat_stress": round(max_row["heat_stress_score"], 0),
        "summary": (
            f"Avg heat stress {avg_stress:.0f}/100; "
            f"peak {max_row['region']} at {max_row['heat_stress_score']:.0f}/100"
        ),
    }
    if "latest_max_c" in max_row:
        result["max_temp_c"] = max_row["latest_max_c"]
    return result