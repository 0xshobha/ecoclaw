"""skills/zai_llm.py
Z.AI compound-reasoning skill.

Z.AI specialises in multi-step "compound AI" inference – it synthesises
evidence from multiple sources into a structured, JSON-formatted report.
Falls back to a rich mock when MOCK_MODE=true or the key is absent.
"""

from __future__ import annotations

import json
from typing import Any

from openai import AsyncOpenAI

from config.settings import settings
from utils.logger import log

_SYSTEM_PROMPT = (
    "You are Z.AI's compound reasoning engine for EcoClaw. "
    "You receive multi-source climate data and produce structured, "
    "actionable intelligence for autonomous agent systems. "
    "Always respond with valid JSON matching the requested schema."
)

_SCHEMA_DESCRIPTION = (
    "Respond with a JSON object containing exactly these keys:\n"
    "  summary        (string)  – 2-3 sentence executive summary\n"
    "  risk_score     (integer) – 0-100 composite risk\n"
    "  actions        (list)    – 3-5 concrete recommended actions (strings)\n"
    "  confidence     (float)   – 0.0-1.0 model confidence\n"
    "  sources_used   (list)    – data sources considered (strings)"
)


class ZAISkill:
    """Z.AI compound AI – multi-step reasoning and synthesis."""

    def __init__(self) -> None:
        self._client = AsyncOpenAI(
            api_key=settings.zai_api_key,
            base_url=settings.zai_api_base,
        )
        self._model = settings.zai_model

    # ── Public interface ─────────────────────────────────────────────────────

    async def compound_reasoning(
        self,
        context: dict[str, Any],
        objective: str,
    ) -> dict[str, Any]:
        """
        Run multi-step reasoning over *context* to achieve *objective*.
        Returns a structured dict with summary, risk_score, actions, etc.
        """
        if self._is_mock():
            return self._mock_reasoning(context, objective)

        user_prompt = (
            f"Objective: {objective}\n\n"
            f"Context (JSON):\n{json.dumps(context, default=str, indent=2)}\n\n"
            f"{_SCHEMA_DESCRIPTION}"
        )

        try:
            resp = await self._client.chat.completions.create(
                model=self._model,
                messages=[
                    {"role": "system", "content": _SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
                response_format={"type": "json_object"},
                temperature=0.3,
                max_tokens=800,
            )
            raw = resp.choices[0].message.content or "{}"
            return json.loads(raw)
        except json.JSONDecodeError as exc:
            log.warning(f"[ZAI] JSON parse error: {exc} – using mock")
        except Exception as exc:
            log.warning(f"[ZAI] API error: {exc} – using mock")

        return self._mock_reasoning(context, objective)

    # ── Internal ─────────────────────────────────────────────────────────────

    def _is_mock(self) -> bool:
        return settings.mock_mode or settings.zai_api_key.startswith("YOUR_")

    def _mock_reasoning(
        self,
        context: dict[str, Any],
        objective: str,
    ) -> dict[str, Any]:
        region = context.get("region", "unknown region")
        risk = context.get("composite_risk_score", 65)
        return {
            "summary": (
                f"Z.AI compound analysis for '{objective}': "
                f"Multi-source evidence confirms elevated environmental risk in {region}. "
                f"Composite risk score: {risk}/100. Immediate coordinated response advised."
            ),
            "risk_score": risk,
            "actions": [
                f"Issue high-priority climate alert for {region}",
                "Activate community ground-truth reporting via Telegram bot",
                "Post on-chain alert with NFT reward for verified contributor reports",
                "Notify regional environmental authorities via automated API call",
                "Schedule follow-up satellite scan in 48 hours",
            ],
            "confidence": 0.84,
            "sources_used": [
                "NASA EONET events feed",
                "Compression Company satellite analytics",
                "FLock federated climate model",
            ],
        }
