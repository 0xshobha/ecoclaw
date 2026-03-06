"""orchestrator/scheduler.py
APScheduler-based cron runner for EcoClaw.

Schedules:
  • Hourly  – quick scan of highest-risk regions
  • Daily   – full multi-region deep scan + summary log

The scheduler is started by main.py alongside the Telegram bot.
"""

from __future__ import annotations

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

from orchestrator.core import EcoClawOrchestrator
from utils.logger import log

# Regions included in the hourly quick-scan
_HOURLY_REGIONS = ["amazon", "uk"]

# Regions included in the full daily scan
_DAILY_REGIONS = ["amazon", "uk", "southeast asia", "australia", "california", "africa"]


class EcoClawScheduler:
    """Wraps APScheduler to drive periodic EcoClaw scans."""

    def __init__(self, orchestrator: EcoClawOrchestrator) -> None:
        self._orch = orchestrator
        self._scheduler = AsyncIOScheduler(timezone="UTC")

    # ── Public API ────────────────────────────────────────────────────────────

    def start(self) -> None:
        """Register jobs and start the async scheduler."""
        # Hourly quick scan (top-risk regions)
        self._scheduler.add_job(
            self._hourly_scan,
            trigger=IntervalTrigger(hours=1),
            id="hourly_scan",
            name="EcoClaw Hourly Quick Scan",
            replace_existing=True,
        )

        # Daily deep scan at 06:00 UTC
        self._scheduler.add_job(
            self._daily_scan,
            trigger=CronTrigger(hour=6, minute=0),
            id="daily_deep_scan",
            name="EcoClaw Daily Deep Scan",
            replace_existing=True,
        )

        self._scheduler.start()
        log.info(
            "[Scheduler] Started – hourly quick-scan + daily deep-scan at 06:00 UTC"
        )

    def stop(self) -> None:
        self._scheduler.shutdown(wait=False)
        log.info("[Scheduler] Stopped")

    # ── Job handlers ─────────────────────────────────────────────────────────

    async def _hourly_scan(self) -> None:
        log.info("[Scheduler] Hourly quick-scan running…")
        results = await self._orch.scan_scheduled(regions=_HOURLY_REGIONS)
        for r in results:
            analysis = r.get("analysis", {})
            risk = analysis.get("composite_risk_score", 0)
            region = r.get("region", "?")
            if risk >= 60:
                log.warning(f"[Scheduler] HIGH RISK – {region} score={risk}/100")
            else:
                log.info(f"[Scheduler] OK – {region} score={risk}/100")

    async def _daily_scan(self) -> None:
        log.info("[Scheduler] Daily deep-scan running…")
        results = await self._orch.scan_scheduled(regions=_DAILY_REGIONS)
        critical = [
            r
            for r in results
            if r.get("analysis", {}).get("composite_risk_score", 0) >= 80
        ]
        log.info(
            f"[Scheduler] Daily scan complete – "
            f"{len(results)} regions scanned, {len(critical)} critical"
        )
        for r in critical:
            log.warning(
                f"[Scheduler] CRITICAL – {r.get('region')} | "
                f"tx={r.get('web3', {}).get('tx_hash', 'n/a')[:20]}…"
            )
