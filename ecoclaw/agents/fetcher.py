"""agents/fetcher.py
Agent 1 – Data Fetcher

Scrapes real environmental event data and satellite imagery metadata from:
  • NASA EONET  (active disaster events)
  • NASA Earth Imagery API  (Landsat tile metadata)
  • Compression Company SDK  (specialist satellite analytics)
"""

from __future__ import annotations

import re
from typing import Any

from agents.base import AgentResult, BaseAgent
from skills.satellite import REGION_COORDS, SatelliteSkill
from utils.logger import log

# Natural-language keyword → EONET category mapping (longest match wins)
_EVENT_MAP: dict[str, str] = {
    "deforestation": "wildfires",
    "flooding": "floods",
    "wildfire": "wildfires",
    "hurricane": "severeStorms",
    "cyclone": "severeStorms",
    "earthquake": "earthquakes",
    "volcano": "volcanoes",
    "drought": "drought",
    "flood": "floods",
    "storm": "severeStorms",
    "fire": "wildfires",
    "ice": "seaAndLakeIce",
    "snow": "severeStorms",
    "landslide": "landslides",
}

# Pre-compiled region pattern (multi-word regions ordered longest-first)
_REGION_PATTERN = re.compile(
    r"|".join(re.escape(r) for r in sorted(REGION_COORDS, key=len, reverse=True)),
    re.IGNORECASE,
)


class FetcherAgent(BaseAgent):
    """Fetches satellite imagery and environmental event data."""

    name = "FetcherAgent"
    description = (
        "Fetches real-time satellite imagery metadata and active "
        "environmental event data from NASA and the Compression Company SDK."
    )

    def __init__(self, config: dict[str, Any] | None = None) -> None:
        super().__init__(config)
        self.satellite = SatelliteSkill()

    # ── BaseAgent interface ───────────────────────────────────────────────────

    async def run(self, task: dict[str, Any]) -> AgentResult:
        query: str = task.get("query", "").lower()
        region = self._extract_region(query)
        event_type = self._extract_event_type(query)

        log.info(
            f"[{self.name}] query='{query[:60]}' | region={region} | event={event_type}"
        )

        # Parallel-ish: fetch events first, then imagery + compression
        events = await self.satellite.fetch_nasa_events(event_type)

        coords = REGION_COORDS.get(region, (-3.0, -60.0))
        imagery_meta = await self.satellite.fetch_earth_imagery_meta(
            lat=coords[0], lon=coords[1]
        )
        compression = await self.satellite.fetch_compression_analysis(
            region=region, analysis_type=event_type
        )

        result: dict[str, Any] = {
            "region": region,
            "event_type": event_type,
            "nasa_events": events,
            "imagery_metadata": imagery_meta,
            "compression_analysis": compression,
        }

        self.set_state("last_fetch", result)
        log.success(f"[{self.name}] Fetch complete – {events['count']} active events")
        return AgentResult(success=True, data=result)

    # ── Private helpers ───────────────────────────────────────────────────────

    def _extract_region(self, query: str) -> str:
        """Return the first (longest) region name found in query."""
        m = _REGION_PATTERN.search(query)
        if m:
            return m.group(0).lower()
        return "amazon"  # sensible default

    def _extract_event_type(self, query: str) -> str:
        """Return the EONET category for the first matching keyword (longest key first)."""
        for keyword in sorted(_EVENT_MAP, key=len, reverse=True):
            if re.search(rf"\b{re.escape(keyword)}\b", query, re.IGNORECASE):
                return _EVENT_MAP[keyword]
        return "wildfires"
