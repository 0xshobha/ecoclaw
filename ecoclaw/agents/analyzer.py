"""agents/analyzer.py
Agent 2 – Analyzer

Processes raw satellite/event data to:
  • Compute a composite risk score (0-100)
  • Simulate NDVI change detection with NumPy
  • Extract geographical hotspot coordinates
  • Classify severity level

No external API calls – pure analytics over the FetcherAgent output.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np

from agents.base import AgentResult, BaseAgent
from config.settings import settings
from utils.helpers import risk_score_to_severity
from utils.logger import log

try:
    import matplotlib

    matplotlib.use("Agg")  # headless – no display needed
    import matplotlib.pyplot as plt

    _HAS_MPL = True
except ImportError:
    _HAS_MPL = False
    log.warning("[AnalyzerAgent] matplotlib not available – charts disabled")


class AnalyzerAgent(BaseAgent):
    """Processes raw satellite data and computes environmental risk metrics."""

    name = "AnalyzerAgent"
    description = (
        "Processes satellite imagery data using NumPy-based NDVI change detection, "
        "computes a composite risk score, and extracts geographic hotspots."
    )

    # ── BaseAgent interface ───────────────────────────────────────────────────

    async def run(self, task: dict[str, Any]) -> AgentResult:
        raw: dict[str, Any] = task.get("raw_data", {})
        if not raw:
            return AgentResult(
                success=False, error="No raw_data supplied to AnalyzerAgent"
            )

        log.info(
            f"[{self.name}] Analysing data for region='{raw.get('region', 'unknown')}'"
        )

        comp = raw.get("compression_analysis", {})
        events = raw.get("nasa_events", {})

        change_pct: float = float(comp.get("change_percent", 0.0))
        affected_km2: float = float(comp.get("affected_area_km2", 0.0))
        confidence: float = float(comp.get("confidence", 0.0))
        severity_raw: str = str(comp.get("severity", "medium")).lower()
        event_count: int = int(events.get("count", 0))

        ndvi_stats = self._ndvi_change_detection(change_pct)
        hotspots = self._extract_hotspots(events.get("events", []))
        risk_score = self._composite_risk_score(
            change_pct=change_pct,
            event_count=event_count,
            confidence=confidence,
            severity_raw=severity_raw,
        )
        region_slug = str(raw.get("region", "unknown")).replace(" ", "_")
        chart_path = self._generate_ndvi_chart(ndvi_stats, region_slug)

        analysis: dict[str, Any] = {
            "region": raw.get("region", "unknown"),
            "event_type": raw.get("event_type", "unknown"),
            "change_percent": change_pct,
            "affected_area_km2": affected_km2,
            "confidence": confidence,
            "severity": severity_raw,
            "active_event_count": event_count,
            "ndvi_stats": ndvi_stats,
            "hotspots": hotspots,
            "composite_risk_score": risk_score,
            "risk_level": risk_score_to_severity(risk_score),
            "chart_path": chart_path,
        }

        self.set_state("last_analysis", analysis)
        log.success(
            f"[{self.name}] Analysis done – "
            f"risk_score={risk_score} level={analysis['risk_level']}"
        )
        return AgentResult(success=True, data=analysis)

    # ── Analytics helpers ─────────────────────────────────────────────────────

    def _ndvi_change_detection(self, change_pct: float) -> dict[str, float]:
        """
        Simulate NDVI (Normalised Difference Vegetation Index) before/after
        comparison using NumPy random arrays seeded for reproducibility.
        """
        rng = np.random.default_rng(seed=42)
        n_pixels = 256

        ndvi_before = rng.uniform(0.3, 0.8, size=n_pixels)
        noise = rng.normal(0.0, 0.02, size=n_pixels)
        ndvi_after = np.clip(ndvi_before * (1.0 - change_pct / 100.0) + noise, 0.0, 1.0)

        delta = float(np.mean(ndvi_after) - np.mean(ndvi_before))
        return {
            "ndvi_mean_before": round(float(np.mean(ndvi_before)), 4),
            "ndvi_mean_after": round(float(np.mean(ndvi_after)), 4),
            "ndvi_delta": round(delta, 4),
            "ndvi_std_before": round(float(np.std(ndvi_before)), 4),
            "ndvi_std_after": round(float(np.std(ndvi_after)), 4),
            "pixels_analysed": n_pixels,
            "change_pct": round(change_pct, 2),
        }

    def _extract_hotspots(self, events: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Pick the first coordinate from each event geometry."""
        hotspots: list[dict[str, Any]] = []
        for event in events[:10]:
            for geo in event.get("geometries", []):
                coords = geo.get("coordinates", [])
                if isinstance(coords, list) and len(coords) >= 2:
                    hotspots.append(
                        {
                            "title": event.get("title", "Unknown event"),
                            "lon": coords[0],
                            "lat": coords[1],
                            "date": geo.get("date", ""),
                        }
                    )
                    break  # one point per event is enough
        return hotspots

    def _generate_ndvi_chart(
        self, ndvi_stats: dict[str, float], region_slug: str
    ) -> str | None:
        """Render a before/after NDVI bar chart, save to data/ and return the path."""
        if not _HAS_MPL:
            return None
        try:
            data_dir = Path(settings.data_dir)
            data_dir.mkdir(parents=True, exist_ok=True)

            labels = ["NDVI Before", "NDVI After"]
            values = [
                ndvi_stats.get("ndvi_mean_before", 0.0),
                ndvi_stats.get("ndvi_mean_after", 0.0),
            ]
            colors = ["#2ecc71", "#e74c3c"]  # green vs red

            fig, ax = plt.subplots(figsize=(6, 3.5))
            bars = ax.bar(labels, values, color=colors, width=0.45, edgecolor="white")

            ax.set_ylim(0, 1.0)
            ax.set_ylabel("Mean NDVI")
            ax.set_title(
                f"NDVI Change – {region_slug.replace('_', ' ').title()}\n"
                f"Δ = {ndvi_stats.get('ndvi_delta', 0):.4f}  "
                f"({ndvi_stats.get('change_pct', 0):.1f} % vegetation loss)",
                fontsize=10,
            )
            ax.set_facecolor("#1a1a2e")
            fig.patch.set_facecolor("#16213e")
            ax.tick_params(colors="white")
            ax.title.set_color("white")
            ax.yaxis.label.set_color("white")
            ax.spines[:].set_color("#444")

            for bar, val in zip(bars, values):
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    val + 0.02,
                    f"{val:.3f}",
                    ha="center",
                    color="white",
                    fontsize=10,
                    fontweight="bold",
                )

            out_path = data_dir / f"ndvi_{region_slug}.png"
            plt.tight_layout()
            plt.savefig(out_path, dpi=120, bbox_inches="tight")
            plt.close(fig)
            log.info(f"[AnalyzerAgent] NDVI chart saved → {out_path}")
            return str(out_path)
        except Exception as exc:
            log.warning(f"[AnalyzerAgent] Chart generation failed: {exc}")
            return None

    @staticmethod
    def _composite_risk_score(
        change_pct: float,
        event_count: int,
        confidence: float,
        severity_raw: str,
    ) -> int:
        """
        Weighted composite risk score in range [0, 100].

        Weights:
          • % vegetation / area change  → up to 40 pts
          • active event count          → up to 25 pts
          • model confidence            → up to 15 pts
          • severity label              → up to 20 pts
        """
        severity_pts = {"low": 0, "medium": 5, "high": 12, "critical": 20}

        score = (
            min(change_pct * 3.2, 40.0)
            + min(event_count * 8.0, 25.0)
            + confidence * 15.0
            + severity_pts.get(severity_raw, 5)
        )
        return int(min(round(score), 100))
