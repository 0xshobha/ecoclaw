"""skills/satellite.py
Satellite & environmental event data skill.

Live sources:
  • NASA EONET  – open disaster / wildfire / flood events feed
  • NASA Earth Imagery – Landsat tile for a lat/lon
  • Compression Company SDK – specialist satellite analytics
    (falls back gracefully to mock when API key is absent)
"""

from __future__ import annotations

from typing import Any

import aiohttp
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from config.settings import settings
from utils.logger import log

# ── Retry decorator shared across all HTTP helpers ───────────────────────────
_http_retry = retry(
    retry=retry_if_exception_type((aiohttp.ClientError, TimeoutError)),
    wait=wait_exponential(multiplier=1, min=1, max=10),
    stop=stop_after_attempt(3),
    reraise=False,
)

# ── NASA public endpoints ─────────────────────────────────────────────────────
_EONET_URL = "https://eonet.gsfc.nasa.gov/api/v3/events"
_EARTH_IMG_URL = "https://api.nasa.gov/planetary/earth/imagery"

# ── Region → (lat, lon) lookup ───────────────────────────────────────────────
REGION_COORDS: dict[str, tuple[float, float]] = {
    "amazon": (-3.0, -60.0),
    "uk": (51.5, -0.1),
    "southeast asia": (2.0, 104.0),
    "indonesia": (-0.8, 115.0),
    "siberia": (60.0, 100.0),
    "australia": (-25.0, 133.0),
    "africa": (0.0, 20.0),
    "california": (36.7, -119.4),
    "brazil": (-14.0, -51.0),
    "india": (20.0, 78.0),
}

# ── EONET category slugs ─────────────────────────────────────────────────────
_EVENT_CATEGORIES: dict[str, str] = {
    "wildfires": "wildfires",
    "floods": "floods",
    "severeStorms": "severeStorms",
    "drought": "drought",
    "earthquakes": "earthquakes",
    "volcanoes": "volcanoes",
}


class SatelliteSkill:
    """Fetch real satellite and environmental data from NASA & Compression APIs."""

    # ── Public interface ─────────────────────────────────────────────────────

    @_http_retry
    async def fetch_nasa_events(
        self,
        event_type: str = "wildfires",
        days: int = 7,
        limit: int = 20,
    ) -> dict[str, Any]:
        """Return open NASA EONET events for the given category."""
        category = _EVENT_CATEGORIES.get(event_type, "wildfires")
        params = {
            "category": category,
            "days": days,
            "status": "open",
            "limit": limit,
        }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    _EONET_URL,
                    params=params,
                    timeout=aiohttp.ClientTimeout(total=12),
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        events = data.get("events", [])
                        log.info(
                            f"[SatelliteSkill] NASA EONET: {len(events)} '{event_type}' events"
                        )
                        return {
                            "source": "nasa_eonet",
                            "category": category,
                            "events": events,
                            "count": len(events),
                        }
                    log.warning(f"[SatelliteSkill] EONET HTTP {resp.status}")
        except Exception as exc:
            log.warning(f"[SatelliteSkill] EONET error: {exc} – using mock")

        return self._mock_events(event_type)

    @_http_retry
    async def fetch_earth_imagery_meta(
        self,
        lat: float,
        lon: float,
        date: str = "2024-06-01",
    ) -> dict[str, Any]:
        """Fetch Landsat imagery metadata from NASA Earth Imagery API."""
        params = {
            "lat": lat,
            "lon": lon,
            "date": date,
            "dim": 0.025,
            "api_key": settings.nasa_api_key,
        }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    _EARTH_IMG_URL,
                    params=params,
                    timeout=aiohttp.ClientTimeout(total=15),
                ) as resp:
                    if resp.status == 200:
                        ctype = resp.content_type or ""
                        if "image" in ctype:
                            body = await resp.read()
                            log.info(
                                f"[SatelliteSkill] Landsat tile {len(body):,} bytes "
                                f"@ ({lat}, {lon})"
                            )
                            return {
                                "source": "nasa_earthdata",
                                "lat": lat,
                                "lon": lon,
                                "date": date,
                                "bytes": len(body),
                                "content_type": ctype,
                            }
                        # API returned JSON (asset info)
                        return {
                            "source": "nasa_earthdata",
                            "lat": lat,
                            "lon": lon,
                            "date": date,
                            "meta": await resp.json(),
                        }
                    log.warning(f"[SatelliteSkill] Earth Imagery HTTP {resp.status}")
        except Exception as exc:
            log.warning(f"[SatelliteSkill] Earth Imagery error: {exc}")

        return {
            "source": "nasa_earthdata_mock",
            "lat": lat,
            "lon": lon,
            "date": date,
            "bytes": 0,
        }

    @_http_retry
    async def fetch_compression_analysis(
        self,
        region: str,
        analysis_type: str = "deforestation",
    ) -> dict[str, Any]:
        """
        Compression Company SDK.
        Uses live API when COMPRESSION_API_KEY is set and MOCK_MODE=false,
        otherwise falls back to realistic mock data.
        """
        if not settings.compression_api_key or settings.mock_mode:
            log.info("[SatelliteSkill] Compression SDK: mock mode")
            return self._mock_compression(region, analysis_type)

        headers = {
            "Authorization": f"Bearer {settings.compression_api_key}",
            "Content-Type": "application/json",
        }
        payload = {"region": region, "analysis_type": analysis_type}

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{settings.compression_api_base}/analyze",
                    json=payload,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=25),
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        log.info(
                            f"[SatelliteSkill] Compression analysis done for '{region}'"
                        )
                        return data
                    log.warning(f"[SatelliteSkill] Compression SDK HTTP {resp.status}")
        except Exception as exc:
            log.warning(f"[SatelliteSkill] Compression SDK error: {exc}")

        return self._mock_compression(region, analysis_type)

    # ── Mock fallbacks ───────────────────────────────────────────────────────

    def _mock_events(self, event_type: str) -> dict[str, Any]:
        return {
            "source": "mock",
            "category": event_type,
            "events": [
                {
                    "id": "MOCK_EVT_001",
                    "title": f"Active {event_type} – Amazon Basin",
                    "categories": [{"id": event_type, "title": event_type}],
                    "geometries": [
                        {
                            "date": "2026-03-04T00:00:00Z",
                            "type": "Point",
                            "coordinates": [-60.0, -3.0],
                        }
                    ],
                },
                {
                    "id": "MOCK_EVT_002",
                    "title": f"Severe {event_type} – Southeast Asia",
                    "categories": [{"id": event_type, "title": event_type}],
                    "geometries": [
                        {
                            "date": "2026-03-03T00:00:00Z",
                            "type": "Point",
                            "coordinates": [104.0, 2.0],
                        }
                    ],
                },
                {
                    "id": "MOCK_EVT_003",
                    "title": f"Emerging {event_type} – Sub-Saharan Africa",
                    "categories": [{"id": event_type, "title": event_type}],
                    "geometries": [
                        {
                            "date": "2026-03-02T00:00:00Z",
                            "type": "Point",
                            "coordinates": [20.0, 5.0],
                        }
                    ],
                },
            ],
            "count": 3,
        }

    def _mock_compression(
        self,
        region: str,
        analysis_type: str,
    ) -> dict[str, Any]:
        severity_lookup = {
            "deforestation": "high",
            "floods": "critical",
            "wildfires": "high",
            "drought": "medium",
        }
        return {
            "source": "compression_mock",
            "region": region,
            "analysis_type": analysis_type,
            "change_percent": 12.5,
            "confidence": 0.87,
            "affected_area_km2": 340.2,
            "ndvi_delta": -0.14,
            "timestamp": "2026-03-04T12:00:00Z",
            "severity": severity_lookup.get(analysis_type, "medium"),
            "insight": (
                f"Significant {analysis_type} activity detected in {region} "
                f"over the past 30 days. Affected area: ~340 km². "
                f"Confidence: 87 %."
            ),
        }
