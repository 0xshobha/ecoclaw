"""orchestrator/core.py
EcoClawOrchestrator – the OpenClaw-compatible agent swarm coordinator.

Pipeline (sequential, with streaming progress callbacks):

    User Query
        → FetcherAgent      (NASA + Compression satellite data)
        → AnalyzerAgent     (NDVI change detection, risk score)
        → PredictorAgent    (FLock LLM + Z.AI compound reasoning)
        → Web3Agent         (on-chain alert hash + Animoca NFT)
        → Response dict

Each stage gate-checks the previous result; a failure short-circuits
the pipeline and returns an error response with the failing stage name.
"""

from __future__ import annotations

import asyncio
from typing import Any, Callable

from agents.analyzer import AnalyzerAgent
from agents.fetcher import FetcherAgent
from agents.predictor import PredictorAgent
from agents.web3_agent import Web3CoordinatorAgent
from utils.logger import log


# Default regions for scheduled scans
_DEFAULT_SCAN_REGIONS = ["amazon", "uk", "southeast asia", "australia"]


class EcoClawOrchestrator:
    """
    Coordinates the EcoClaw multi-agent swarm.

    Usage:
        orch = EcoClawOrchestrator()
        orch.on_progress(lambda msg: print(msg))
        result = await orch.process_query("scan for wildfires in amazon")
    """

    def __init__(self) -> None:
        self.fetcher = FetcherAgent()
        self.analyzer = AnalyzerAgent()
        self.predictor = PredictorAgent()
        self.web3 = Web3CoordinatorAgent()
        self._progress_cbs: list[Callable[[str], None]] = []
        log.info("EcoClawOrchestrator ready – 4-agent swarm loaded")

    # ── Public API ────────────────────────────────────────────────────────────

    def on_progress(self, callback: Callable[[str], None]) -> None:
        """Register a progress-update callback (e.g. to stream messages to Telegram)."""
        self._progress_cbs.append(callback)

    async def process_query(
        self,
        query: str,
        contributor_address: str = "0x0000000000000000000000000000000000000000",
    ) -> dict[str, Any]:
        """
        Run the full 4-stage pipeline for a user climate query.

        Returns a result dict with keys:
          query, region, fetch, analysis, prediction, web3, alert_message
        On failure: {error, stage}
        """
        log.info(f"[Orchestrator] New query: '{query[:80]}'")
        self._emit(f"🛰️ Dispatching EcoClaw agents for: *{query}*…")

        # ── Stage 1: Fetch ─────────────────────────────────────────────────
        fetch = await self.fetcher.run({"query": query})
        if not fetch.success:
            return self._error("fetch", fetch.error)
        self._emit(
            f"📡 Satellite data acquired – "
            f"{fetch.data['nasa_events']['count']} active events found.\n"
            "🔬 Running change-detection analysis…"
        )

        # ── Stage 2: Analyze ───────────────────────────────────────────────
        analyze = await self.analyzer.run({"raw_data": fetch.data})
        if not analyze.success:
            return self._error("analyze", analyze.error)
        risk = analyze.data["composite_risk_score"]
        self._emit(
            f"📊 Analysis complete – risk score *{risk}/100* "
            f"({analyze.data['risk_level'].upper()}).\n"
            "🤖 Running FLock + Z.AI prediction…"
        )

        # ── Stage 3: Predict ───────────────────────────────────────────────
        predict = await self.predictor.run({"analysis": analyze.data})
        if not predict.success:
            return self._error("predict", predict.error)
        self._emit(
            f"💡 Prediction ready – severity *{predict.data['severity'].upper()}*.\n"
            "🔗 Posting on-chain alert, storing on Unibase, registering on Virtual Protocol…"
        )

        # ── Stage 4: Web3 ─────────────────────────────────────────────────
        web3 = await self.web3.run(
            {
                "prediction": predict.data,
                "contributor_address": contributor_address,
            }
        )
        if not web3.success:
            # Web3 failure is non-fatal – pipeline still returns useful data
            log.warning(f"[Orchestrator] Web3 stage failed: {web3.error}")
            web3_data: dict[str, Any] = {"error": web3.error}
            alert_msg = ""
        else:
            web3_data = web3.data
            alert_msg = web3.data.get("alert_message", "")

        self._emit("✅ EcoClaw pipeline complete!")

        return {
            "query": query,
            "region": fetch.data.get("region"),
            "fetch": fetch.data,
            "analysis": analyze.data,
            "prediction": predict.data,
            "web3": web3_data,
            "alert_message": alert_msg,
        }

    async def scan_scheduled(
        self,
        regions: list[str] | None = None,
    ) -> list[dict[str, Any]]:
        """
        Run a cron-style scan across multiple regions concurrently.
        Returns only the successful results.
        """
        targets = regions or _DEFAULT_SCAN_REGIONS
        log.info(f"[Orchestrator] Scheduled scan – regions: {targets}")

        tasks = [self.process_query(f"scan for wildfires in {r}") for r in targets]
        outcomes = await asyncio.gather(*tasks, return_exceptions=True)

        valid = [r for r in outcomes if isinstance(r, dict) and "error" not in r]
        log.info(
            f"[Orchestrator] Scheduled scan complete – "
            f"{len(valid)}/{len(targets)} successful"
        )
        return valid

    def agent_states(self) -> dict[str, Any]:
        """Return the last-known state of each agent (useful for /status commands)."""
        return {
            "fetcher": self.fetcher.get_state(),
            "analyzer": self.analyzer.get_state(),
            "predictor": self.predictor.get_state(),
            "web3": self.web3.get_state(),
        }

    # ── Internal helpers ──────────────────────────────────────────────────────

    def _emit(self, message: str) -> None:
        for cb in self._progress_cbs:
            try:
                cb(message)
            except Exception:
                pass

    @staticmethod
    def _error(stage: str, error: str | None) -> dict[str, Any]:
        log.error(f"[Orchestrator] Pipeline failed at stage '{stage}': {error}")
        return {"error": error or "Unknown error", "stage": stage}
