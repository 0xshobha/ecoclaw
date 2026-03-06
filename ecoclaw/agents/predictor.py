"""agents/predictor.py
Agent 3 – Predictor

Combines:
  • FLock.io federated LLM  → climate-impact narrative
  • Z.AI compound reasoning → structured risk report (JSON)

Produces a unified prediction dict consumed by the Web3CoordinatorAgent
and surfaced to the end-user.
"""

from __future__ import annotations

from typing import Any

from agents.base import AgentResult, BaseAgent
from skills.flock_llm import FlockLLMSkill
from skills.zai_llm import ZAISkill
from utils.helpers import risk_score_to_severity
from utils.logger import log


class PredictorAgent(BaseAgent):
    """Generates climate risk predictions using FLock + Z.AI models."""

    name = "PredictorAgent"
    description = (
        "Runs FLock.io federated LLM inference and Z.AI compound reasoning "
        "to forecast environmental impacts and recommend actions."
    )

    def __init__(self, config: dict[str, Any] | None = None) -> None:
        super().__init__(config)
        self.flock = FlockLLMSkill()
        self.zai = ZAISkill()

    # ── BaseAgent interface ───────────────────────────────────────────────────

    async def run(self, task: dict[str, Any]) -> AgentResult:
        analysis: dict[str, Any] = task.get("analysis", {})
        if not analysis:
            return AgentResult(
                success=False, error="No analysis data supplied to PredictorAgent"
            )

        region = analysis.get("region", "unknown")
        event_type = analysis.get("event_type", "unknown")
        risk_score = analysis.get("composite_risk_score", 0)

        log.info(
            f"[{self.name}] region={region} | event={event_type} | score={risk_score}"
        )

        # ── Step 1: FLock climate narrative ──────────────────────────────────
        flock_assessment = await self.flock.predict_climate_impact(analysis)

        # ── Step 2: Z.AI structured compound reasoning ───────────────────────
        zai_result = await self.zai.compound_reasoning(
            context={**analysis, "flock_assessment": flock_assessment},
            objective=(
                f"Assess climate risk and produce action plan for {region} "
                f"({event_type} event, composite risk score {risk_score}/100)"
            ),
        )

        # Merge risk scores (Z.AI overrides if available, else use analyzer score)
        final_risk = int(zai_result.get("risk_score", risk_score))
        severity = risk_score_to_severity(final_risk)

        prediction: dict[str, Any] = {
            "region": region,
            "event_type": event_type,
            "flock_assessment": flock_assessment,
            "zai_summary": zai_result.get("summary", ""),
            "zai_actions": zai_result.get("actions", []),
            "zai_sources": zai_result.get("sources_used", []),
            "risk_score": final_risk,
            "severity": severity,
            "confidence": float(zai_result.get("confidence", 0.0)),
        }

        self.set_state("last_prediction", prediction)
        log.success(
            f"[{self.name}] Prediction complete – "
            f"severity={severity.upper()} risk={final_risk}"
        )
        return AgentResult(success=True, data=prediction)
