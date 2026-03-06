"""skills/flock_llm.py
FLock.io federated LLM skill – OpenAI-compatible endpoint.

FLock provides cost-effective, federated language models.
The client is a drop-in openai.AsyncOpenAI pointed at FLock's base URL.
Falls back to a deterministic mock when MOCK_MODE=true or the key is absent.
"""

from __future__ import annotations

from typing import Any

from openai import AsyncOpenAI

from config.settings import settings
from utils.logger import log


class FlockLLMSkill:
    """Interact with FLock.io federated language models."""

    def __init__(self) -> None:
        self._client = AsyncOpenAI(
            api_key=settings.flock_api_key,
            base_url=settings.flock_api_base,
        )
        self._model = settings.flock_model

    # ── Public helpers ───────────────────────────────────────────────────────

    async def chat(
        self,
        messages: list[dict[str, str]],
        temperature: float = 0.6,
        max_tokens: int = 512,
    ) -> str:
        """Single-turn chat completion; returns assistant text."""
        if self._is_mock():
            return self._mock_response(messages[-1].get("content", ""))

        try:
            resp = await self._client.chat.completions.create(
                model=self._model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return resp.choices[0].message.content or ""
        except Exception as exc:
            log.warning(f"[FlockLLM] API error: {exc} – falling back to mock")
            return self._mock_response(messages[-1].get("content", ""))

    async def predict_climate_impact(self, analysis_data: dict[str, Any]) -> str:
        """
        Generate a climate-risk narrative from structured analysis data.
        Uses FLock as the inference backend.
        """
        user_prompt = (
            "You are an expert climate scientist reviewing satellite analysis data.\n\n"
            f"Data:\n{analysis_data}\n\n"
            "Provide a concise risk assessment (3-5 sentences) covering:\n"
            "1. Overall risk level (low / medium / high / critical)\n"
            "2. Key environmental impacts\n"
            "3. Recommended immediate actions"
        )
        return await self.chat(
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are EcoClaw's climate AI, powered by FLock federated models. "
                        "Be precise, data-driven, and action-oriented."
                    ),
                },
                {"role": "user", "content": user_prompt},
            ]
        )

    # ── Internal ─────────────────────────────────────────────────────────────

    def _is_mock(self) -> bool:
        key = settings.flock_api_key
        _placeholder = key.startswith("YOUR_") or len(key) < 20
        return settings.mock_mode or _placeholder

    def _mock_response(self, query: str) -> str:
        return (
            "[FLock Mock Response] Analysis complete.\n\n"
            "Risk level: HIGH. Satellite data indicates accelerated environmental "
            "degradation with 12.5 % vegetation cover loss in the target region over 30 days. "
            "Key impacts: biodiversity loss, disrupted water cycle, increased carbon emissions. "
            "Recommended actions: (1) Issue high-priority alert to regional authorities, "
            "(2) activate community ground-truth reporting, "
            "(3) schedule follow-up scan in 48 h.\n\n"
            f"[Query context: '{query[:80]}']"
        )
