"""skills/virtual_protocol.py
Virtual Protocol agent-NFT skill.

Virtual Protocol lets you tokenise autonomous agents as on-chain entities
(agent NFTs / "virtuals").  EcoClaw registers each scan cycle as a signed
agent action so the EcoClaw agent accumulates an on-chain reputation.

Live mode  : VIRTUAL_PROTOCOL_API_KEY set + MOCK_MODE=false
Mock mode  : returns deterministic stub data with no network call

Tenacity retries protect against transient API failures.
"""

from __future__ import annotations

import hashlib
from typing import Any

import aiohttp
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from config.settings import settings
from utils.helpers import utcnow_iso
from utils.logger import log

_VP_BASE = "https://api.virtual.protocol/v1"


class VirtualProtocolSkill:
    """Register EcoClaw agent actions on Virtual Protocol."""

    # ── Public API ────────────────────────────────────────────────────────────

    async def register_agent_action(
        self,
        agent_id: str,
        action: str,
        metadata: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Record an agent action on Virtual Protocol.

        Returns:
            {
              action_id    : unique VP action ID
              agent_id     : echoed agent identifier
              tx_hash      : settlement transaction
              vp_url       : Virtual Protocol explorer URL
              registered_at: ISO-8601 timestamp
              mock         : bool
            }
        """
        if not settings.virtual_protocol_api_key or settings.mock_mode:
            return self._mock_action(agent_id, action)

        return await self._live_register(agent_id, action, metadata)

    async def get_agent_profile(self, agent_id: str) -> dict[str, Any] | None:
        """Fetch the on-chain profile for an EcoClaw agent."""
        if not settings.virtual_protocol_api_key or settings.mock_mode:
            return self._mock_profile(agent_id)

        try:
            headers = {"Authorization": f"Bearer {settings.virtual_protocol_api_key}"}
            async with aiohttp.ClientSession() as s:
                async with s.get(
                    f"{_VP_BASE}/agents/{agent_id}",
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=10),
                ) as r:
                    if r.status == 200:
                        return await r.json()
        except Exception as exc:
            log.warning(f"[VirtualProtocol] get_agent_profile error: {exc}")
        return None

    # ── Live path ─────────────────────────────────────────────────────────────

    @retry(
        retry=retry_if_exception_type((aiohttp.ClientError, TimeoutError)),
        wait=wait_exponential(multiplier=1, min=1, max=8),
        stop=stop_after_attempt(3),
        reraise=False,
    )
    async def _live_register(
        self,
        agent_id: str,
        action: str,
        metadata: dict[str, Any],
    ) -> dict[str, Any]:
        headers = {
            "Authorization": f"Bearer {settings.virtual_protocol_api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "agent_id": agent_id,
            "action": action,
            "metadata": metadata,
            "timestamp": utcnow_iso(),
        }
        try:
            async with aiohttp.ClientSession() as s:
                async with s.post(
                    f"{_VP_BASE}/actions",
                    json=payload,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=15),
                ) as resp:
                    if resp.status in (200, 201):
                        data = await resp.json()
                        log.info(
                            f"[VirtualProtocol] Action registered | "
                            f"action_id={data.get('action_id', '?')}"
                        )
                        return {**data, "mock": False}
                    log.warning(f"[VirtualProtocol] HTTP {resp.status}")
        except Exception as exc:
            log.warning(f"[VirtualProtocol] Live register error: {exc}")

        return self._mock_action(agent_id, action)

    # ── Mock path ─────────────────────────────────────────────────────────────

    def _mock_action(self, agent_id: str, action: str) -> dict[str, Any]:
        action_id = (
            "vp_" + hashlib.sha256(f"{agent_id}{action}".encode()).hexdigest()[:16]
        )
        tx = "0x" + hashlib.sha256(action_id.encode()).hexdigest()
        log.info(f"[VirtualProtocol] Mock action | action_id={action_id}")
        return {
            "action_id": action_id,
            "agent_id": agent_id,
            "tx_hash": tx,
            "vp_url": f"https://app.virtual.protocol/agent/{agent_id}",
            "registered_at": utcnow_iso(),
            "mock": True,
            "note": "Set VIRTUAL_PROTOCOL_API_KEY and MOCK_MODE=false for live registration",
        }

    def _mock_profile(self, agent_id: str) -> dict[str, Any]:
        return {
            "agent_id": agent_id,
            "name": "EcoClaw Climate Agent",
            "version": "1.0.0",
            "actions_count": 42,
            "reputation_score": 87,
            "vp_url": f"https://app.virtual.protocol/agent/{agent_id}",
            "mock": True,
        }
