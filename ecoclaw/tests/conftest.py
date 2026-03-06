"""tests/conftest.py
Shared pytest fixtures for the EcoClaw test suite.
"""

import os
import sys
from pathlib import Path

import pytest

# ── Make sure project root is importable ─────────────────────────────────────
sys.path.insert(0, str(Path(__file__).parent.parent))

# Force mock mode for ALL tests so no real API calls are made
os.environ.setdefault("MOCK_MODE", "true")
os.environ.setdefault("LOG_LEVEL", "WARNING")
os.environ.setdefault("TELEGRAM_TOKEN", "FAKE_TOKEN_FOR_TESTS")
os.environ.setdefault("FLOCK_API_KEY", "FAKE_FLOCK_KEY")
os.environ.setdefault("ZAI_API_KEY", "FAKE_ZAI_KEY")


@pytest.fixture
def mock_fetch_data() -> dict:
    """Realistic fetch output for downstream agent tests."""
    return {
        "region": "amazon",
        "event_type": "wildfires",
        "nasa_events": {
            "source": "mock",
            "category": "wildfires",
            "count": 3,
            "events": [
                {
                    "id": "MOCK_EVT_001",
                    "title": "Active wildfires – Amazon Basin",
                    "categories": [{"id": "wildfires", "title": "wildfires"}],
                    "geometries": [
                        {
                            "date": "2026-03-04T00:00:00Z",
                            "type": "Point",
                            "coordinates": [-60.0, -3.0],
                        }
                    ],
                }
            ],
        },
        "imagery_metadata": {
            "source": "nasa_earthdata_mock",
            "lat": -3.0,
            "lon": -60.0,
        },
        "compression_analysis": {
            "source": "compression_mock",
            "region": "amazon",
            "analysis_type": "wildfires",
            "change_percent": 12.5,
            "confidence": 0.87,
            "affected_area_km2": 340.2,
            "ndvi_delta": -0.14,
            "severity": "high",
            "insight": "Mock insight",
        },
    }


@pytest.fixture
def mock_analysis_data(mock_fetch_data) -> dict:
    """Pre-computed analysis output for predictor/web3 tests."""
    return {
        "region": "amazon",
        "event_type": "wildfires",
        "change_percent": 12.5,
        "affected_area_km2": 340.2,
        "confidence": 0.87,
        "severity": "high",
        "active_event_count": 3,
        "ndvi_stats": {
            "ndvi_mean_before": 0.55,
            "ndvi_mean_after": 0.48,
            "ndvi_delta": -0.07,
            "ndvi_std_before": 0.12,
            "ndvi_std_after": 0.13,
            "pixels_analysed": 256,
            "change_pct": 12.5,
        },
        "hotspots": [
            {"title": "Mock fire", "lon": -60.0, "lat": -3.0, "date": "2026-03-04"}
        ],
        "composite_risk_score": 75,
        "risk_level": "high",
        "chart_path": None,
    }


@pytest.fixture
def mock_prediction_data() -> dict:
    """Pre-computed prediction output for web3 agent tests."""
    return {
        "region": "amazon",
        "event_type": "wildfires",
        "flock_assessment": "Mock FLock assessment",
        "zai_summary": "Mock Z.AI summary",
        "zai_actions": ["Action 1", "Action 2"],
        "zai_sources": ["NASA EONET"],
        "risk_score": 75,
        "severity": "high",
        "confidence": 0.84,
    }
