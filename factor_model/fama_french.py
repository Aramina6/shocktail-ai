"""Fama-French factor data loader for the Physical Hazard Risk Tool."""

import pandas as pd
import requests
from io import BytesIO
from zipfile import ZipFile

import streamlit as st


@st.cache_data(ttl=86400)
def fetch_fama_french_factors() -> pd.DataFrame:
    """
    Download daily Fama-French 5-Factor data from Ken French.
    Returns a DataFrame indexed by date with decimal returns.
    """
    url = (
        "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/"
        "F-F_Research_Data_5_Factors_2x3_daily_CSV.zip"
    )

    response = requests.get(url, timeout=30)
    response.raise_for_status()

    with ZipFile(BytesIO(response.content)) as z:
        csv_name = [name for name in z.namelist() if ".CSV" in name.upper()][0]
        with z.open(csv_name) as f:
            df = pd.read_csv(f, skiprows=3)

    df.columns = ["Date", "Mkt-RF", "SMB", "HML", "RMW", "CMA", "RF"]
    df = df.dropna()
    df["Date"] = pd.to_datetime(df["Date"], format="%Y%m%d")
    df = df.set_index("Date")
    df = df.apply(pd.to_numeric, errors="coerce") / 100.0

    return df


def get_factor_covariance_matrix(lookback_days: int = 1260) -> pd.DataFrame:
    """Annualized covariance matrix of the 5 Fama-French factors."""
    df = fetch_fama_french_factors()
    recent = df[["Mkt-RF", "SMB", "HML", "RMW", "CMA"]].dropna().tail(lookback_days)
    return recent.cov() * 252