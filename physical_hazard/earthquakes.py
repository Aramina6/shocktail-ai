"""Earthquakes module - Physical Hazard Risk Tool.

This module handles fetching and rendering USGS earthquake data.
It is intentionally separated so the main app.py stays clean and focused
on the financial / factor stress testing experience.

Business Context:
- Earthquake data is used by insurers for property exposure in seismic zones
  (California, Japan, etc.).
- It helps with accumulation control and reinsurance pricing.
- In a full factor model, "Earthquake intensity in California" can become
  an additional risk factor that is shocked together with market factors.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from datetime import datetime, timedelta

@st.cache_data(ttl=1800)
def fetch_earthquakes_month():
    """Fetch recent earthquakes from USGS FDSN web service."""
    end = datetime.utcnow().strftime("%Y-%m-%d")
    start = (datetime.utcnow() - timedelta(days=30)).strftime("%Y-%m-%d")
    url = (
        f"https://earthquake.usgs.gov/fdsnws/event/1/query?"
        f"format=geojson&starttime={start}&endtime={end}"
        f"&minmagnitude=1&orderby=time"
    )
    try:
        data = requests.get(url, timeout=15).json()
        rows = []
        for f in data.get("features", []):
            p = f["properties"]
            g = f["geometry"]["coordinates"]
            rows.append({
                "name": f"M{p['mag']:.1f}",
                "location": p["place"],
                "impact": f"{p.get('felt', 0)} felt reports",
                "tsunami": bool(p.get("tsunami", 0)),
                "depth_km": g[2],
                "detail_url": p.get("detail", ""),
                "magnitude": p["mag"],
                "time_utc": pd.to_datetime(p["time"], unit="ms"),
                "lat": g[1],
                "lon": g[0],
                "severity": min(int(p["mag"] * 2), 10)
            })
        return pd.DataFrame(rows).sort_values("time_utc", ascending=False)
    except Exception as e:
        st.error(f"Earthquakes error: {e}")
        return pd.DataFrame()


def render():
    """Render the Earthquakes physical hazard module."""
    st.subheader("🌍 Earthquakes (USGS) - Last 30 Days")
    min_mag = st.slider("Minimum Magnitude", 0.0, 10.0, 1.0, 0.5, key="eq_slider")
    df = fetch_earthquakes_month()
    if not df.empty:
        df = df[df["magnitude"] >= min_mag]
        col1, col2 = st.columns([2, 1])
        with col1:
            fig = px.scatter_mapbox(
                df, lat="lat", lon="lon",
                size="severity", color="magnitude",
                color_continuous_scale="Reds",
                hover_name="name",
                hover_data=["location", "depth_km", "impact", "tsunami"],
                zoom=1, height=500
            )
            fig.update_layout(mapbox_style="open-street-map")
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            st.dataframe(df.head(12), use_container_width=True)
    else:
        st.info("No earthquake data available.")
