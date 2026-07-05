"""Unit tests for data fetchers in the Physical Hazard Risk Tool."""

import pytest
from unittest.mock import patch, MagicMock

from physical_hazard.space_hazards import fetch_kp_index
from physical_hazard.nfip_insurance import (
    fetch_nfip_claims_state_summary,
    fetch_fema_disaster_declarations,
)


@pytest.fixture(autouse=True)
def clear_streamlit_caches():
    """Ensure @st.cache_data functions don't return stale real data during tests."""
    try:
        fetch_kp_index.clear()
        fetch_nfip_claims_state_summary.clear()
        fetch_fema_disaster_declarations.clear()
    except Exception:
        pass
    yield


class TestFetchKpIndex:
    def test_returns_empty_on_api_failure(self):
        with patch("physical_hazard.space_hazards.requests.get") as mock_get:
            fetch_kp_index.clear()
            mock_response = MagicMock()
            mock_response.json.return_value = []
            mock_get.return_value = mock_response
            df = fetch_kp_index()
            assert df.empty

    def test_parses_new_dict_format(self):
        fake_data = [
            {"time_tag": "2026-05-01T00:00:00", "Kp": 3.5},
            {"time_tag": "2026-05-01T03:00:00", "Kp": 4.2},
        ]
        with patch("physical_hazard.space_hazards.requests.get") as mock_get:
            fetch_kp_index.clear()
            mock_get.return_value.json.return_value = fake_data
            df = fetch_kp_index()
            assert not df.empty
            assert "kp" in df.columns
            assert df["kp"].max() == 4.2


class TestFetchNifpClaims:
    def test_returns_empty_when_no_data(self):
        with patch("physical_hazard.nfip_insurance.requests.get") as mock_get:
            mock_get.return_value.json.return_value = {"FimaNfipClaims": []}
            df = fetch_nfip_claims_state_summary(years_back=2)
            assert df.empty

    def test_correctly_sums_payment_fields(self):
        fake_claims = [
            {
                "state": "FL",
                "yearOfLoss": 2024,
                "amountPaidOnBuildingClaim": 100000,
                "amountPaidOnContentsClaim": 20000,
                "amountPaidOnIncreasedCostOfComplianceClaim": 5000,
            },
            {
                "state": "FL",
                "yearOfLoss": 2024,
                "amountPaidOnBuildingClaim": 50000,
                "amountPaidOnContentsClaim": 10000,
                "amountPaidOnIncreasedCostOfComplianceClaim": 0,
            },
        ]
        with patch("physical_hazard.nfip_insurance.requests.get") as mock_get:
            fetch_nfip_claims_state_summary.clear()
            mock_get.return_value.json.return_value = {"FimaNfipClaims": fake_claims}
            summary = fetch_nfip_claims_state_summary(years_back=2)

            assert not summary.empty
            row = summary.query("state == 'FL' and yearOfLoss == 2024").iloc[0]
            assert row["total_paid"] == 185000
            assert row["claims_count"] == 2


class TestFetchDisasterDeclarations:
    def test_handles_empty_response(self):
        with patch("physical_hazard.nfip_insurance.requests.get") as mock_get:
            mock_get.return_value.json.return_value = {"DisasterDeclarationsSummaries": []}
            df = fetch_fema_disaster_declarations(years_back=1)
            assert df.empty