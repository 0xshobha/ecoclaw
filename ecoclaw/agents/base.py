"""agents/base.py
OpenClaw-compatible abstract base agent.

Every agent in the EcoClaw swarm inherits from BaseAgent and implements
the `run()` coroutine.  Agents carry a lightweight persistent state dict
so results can be queried between runs (e.g. by the Telegram /status command).
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class AgentResult:
    """Uniform return type for all agent `run()` calls."""

    __slots__ = ("success", "data", "error")

    def __init__(
        self,
        success: bool,
        data: Any = None,
        error: str | None = None,
    ) -> None:
        self.success = success
        self.data = data
        self.error = error

    def __repr__(self) -> str:  # pragma: no cover
        return (
            f"AgentResult(success={self.success}, "
            f"data={type(self.data).__name__}, "
            f"error={self.error!r})"
        )


class BaseAgent(ABC):
    """
    OpenClaw-compatible base agent.

    Sub-classes must set class attributes `name` and `description`,
    then implement the `run()` coroutine.
    """

    name: str = "BaseAgent"
    description: str = ""

    def __init__(self, config: dict[str, Any] | None = None) -> None:
        self.config: dict[str, Any] = config or {}
        self._state: dict[str, Any] = {}

    # ── OpenClaw channel hook ─────────────────────────────────────────────────

    async def on_message(self, message: str) -> AgentResult:
        """
        Handle a raw user message from an OpenClaw channel
        (Telegram / Slack / WhatsApp).  Delegates to `run()`.
        """
        return await self.run({"query": message})

    # ── Abstract interface ────────────────────────────────────────────────────

    @abstractmethod
    async def run(self, task: dict[str, Any]) -> AgentResult:
        """Execute the agent's primary task and return an AgentResult."""
        ...

    # ── Persistent state helpers ──────────────────────────────────────────────

    def get_state(self) -> dict[str, Any]:
        return self._state.copy()

    def set_state(self, key: str, value: Any) -> None:
        self._state[key] = value

    # ── Introspection ─────────────────────────────────────────────────────────

    def describe(self) -> dict[str, str]:
        return {"name": self.name, "description": self.description}
