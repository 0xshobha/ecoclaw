"""agents/web3_agent.py
Agent 4 – Web3 Coordinator

Responsibilities:
  • Build a structured climate alert from prediction data
  • Commit the alert hash to the Base blockchain (Animoca / BGA)
  • Mint an ERC-721 NFT reward for the contributor
  • Store the full alert payload on Unibase (permanent decentralised storage)
  • Register the agent action on Virtual Protocol (agent-NFT reputation)
  • Return all on-chain transaction hashes + formatted alert message
"""

from __future__ import annotations

from typing import Any

from agents.base import AgentResult, BaseAgent
from config.settings import settings
from skills.animoca_web3 import AnimocaWeb3Skill
from skills.unibase import UnibaseSkill
from skills.virtual_protocol import VirtualProtocolSkill
from utils.helpers import build_alert, format_alert_message
from utils.logger import log


class Web3CoordinatorAgent(BaseAgent):
    """Posts climate alerts on-chain, stores payloads on Unibase, and
    registers agent actions on Virtual Protocol."""

    name = "Web3CoordinatorAgent"
    description = (
        "Stores climate alert hashes on the Base blockchain (Animoca), "
        "persists full payloads on Unibase decentralised storage, and "
        "registers agent actions on Virtual Protocol for on-chain reputation."
    )

    def __init__(self, config: dict[str, Any] | None = None) -> None:
        super().__init__(config)
        self.animoca = AnimocaWeb3Skill()
        self.unibase = UnibaseSkill()
        self.virtual_protocol = VirtualProtocolSkill()

    # ── BaseAgent interface ───────────────────────────────────────────────

    async def run(self, task: dict[str, Any]) -> AgentResult:
        prediction: dict[str, Any] = task.get("prediction", {})
        contributor: str = task.get(
            "contributor_address",
            "0x0000000000000000000000000000000000000000",
        )

        if not prediction:
            return AgentResult(
                success=False,
                error="No prediction data supplied to Web3CoordinatorAgent",
            )

        region = prediction.get("region", "unknown")
        severity = prediction.get("severity", "medium")
        event_type = prediction.get("event_type", "climate_event")
        risk_score = prediction.get("risk_score", 0)
        confidence = prediction.get("confidence", 0.0)

        log.info(
            f"[{self.name}] Posting on-chain alert | "
            f"region={region} severity={severity}"
        )

        # ── Build alert object ───────────────────────────────────────────────
        alert = build_alert(
            event_type=event_type,
            region=region,
            severity=severity,
            details={
                "risk_score": risk_score,
                "confidence": round(confidence, 2),
                "models": "FLock + Z.AI",
                "event_type": event_type,
            },
        )

        # ── 1. Animoca: on-chain alert hash (Base) ───────────────────────────
        tx_hash = await self.animoca.post_on_chain_alert(alert)
        alert["tx_hash"] = tx_hash

        # ── 2. Animoca: mint contributor NFT reward ──────────────────────────
        nft_result = await self.animoca.mint_contributor_nft(
            recipient_address=contributor,
            alert_id=alert["id"],
            region=region,
            severity=severity,
        )

        # ── 3. Unibase: persist full alert payload permanently ───────────────
        unibase_result = await self.unibase.store_alert(alert)
        log.info(f"[{self.name}] Unibase CID: {unibase_result.get('cid', '')[:20]}…")

        # ── 4. Virtual Protocol: register agent action for reputation ─────────
        vp_result = await self.virtual_protocol.register_agent_action(
            agent_id=settings.virtual_protocol_agent_id,
            action="climate_alert_posted",
            metadata={
                "alert_id": alert["id"],
                "region": region,
                "severity": severity,
                "risk_score": risk_score,
                "unibase_cid": unibase_result.get("cid", ""),
                "tx_hash": tx_hash,
            },
        )

        result: dict[str, Any] = {
            "alert": alert,
            "alert_message": format_alert_message(alert),
            "tx_hash": tx_hash,
            "nft": nft_result,
            "unibase": unibase_result,
            "virtual_protocol": vp_result,
        }

        self.set_state("last_web3_action", result)
        log.success(
            f"[{self.name}] All on-chain steps done | "
            f"tx={tx_hash[:22]}… "
            f"cid={unibase_result.get('cid','')[:16]}… "
            f"vp={vp_result.get('action_id','')[:16]}…"
        )
        return AgentResult(success=True, data=result)
