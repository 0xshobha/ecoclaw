"""tests/test_orchestrator.py
Integration-style tests for the EcoClawOrchestrator pipeline.

All four agents are patched to return pre-baked AgentResult objects so
the tests run fast and fully offline.
"""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest


# ── Helpers ───────────────────────────────────────────────────────────────────


def _make_agent_result(
    success: bool, data: dict | None = None, error: str | None = None
):
    from agents.base import AgentResult

    return AgentResult(success=success, data=data or {}, error=error)


def _make_orchestrator_with_mocks(
    fetch_data,
    analysis_data,
    prediction_data,
    web3_data,
    fetch_ok=True,
    analysis_ok=True,
    predict_ok=True,
    web3_ok=True,
):
    from orchestrator.core import EcoClawOrchestrator

    orch = EcoClawOrchestrator()

    # Patch each agent's run() directly
    orch.fetcher.run = AsyncMock(
        return_value=_make_agent_result(
            fetch_ok,
            fetch_data,
            error=None if fetch_ok else "fetch failed",
        )
    )
    orch.analyzer.run = AsyncMock(
        return_value=_make_agent_result(
            analysis_ok,
            analysis_data,
            error=None if analysis_ok else "analysis failed",
        )
    )
    orch.predictor.run = AsyncMock(
        return_value=_make_agent_result(
            predict_ok,
            prediction_data,
            error=None if predict_ok else "predict failed",
        )
    )
    orch.web3.run = AsyncMock(
        return_value=_make_agent_result(
            web3_ok,
            web3_data,
            error=None if web3_ok else "web3 failed",
        )
    )
    return orch


# ── TestEcoClawOrchestrator ───────────────────────────────────────────────────


class TestEcoClawOrchestrator:
    """Tests for orchestrator/core.py EcoClawOrchestrator."""

    @pytest.mark.asyncio
    async def test_full_pipeline_success(
        self, mock_fetch_data, mock_analysis_data, mock_prediction_data
    ):
        """Happy path: all 4 stages succeed, result contains expected keys."""
        web3_data = {
            "alert": {"id": "ALERT_001"},
            "alert_message": "🚨 TEST ALERT",
            "tx_hash": "0xDEAD",
            "nft": {"token_id": "1"},
            "unibase": {"cid": "bafybeiTEST"},
            "virtual_protocol": {"action_id": "vp-TEST"},
        }

        orch = _make_orchestrator_with_mocks(
            mock_fetch_data, mock_analysis_data, mock_prediction_data, web3_data
        )
        result = await orch.process_query("wildfires in amazon")

        assert "error" not in result
        assert result["query"] == "wildfires in amazon"
        assert "fetch" in result
        assert "analysis" in result
        assert "prediction" in result
        assert "web3" in result
        assert "alert_message" in result
        assert result["alert_message"] == "🚨 TEST ALERT"

    @pytest.mark.asyncio
    async def test_pipeline_fetch_failure_short_circuits(
        self, mock_fetch_data, mock_analysis_data, mock_prediction_data
    ):
        """Fetcher failure should short-circuit and return {error, stage}."""
        orch = _make_orchestrator_with_mocks(
            mock_fetch_data,
            mock_analysis_data,
            mock_prediction_data,
            web3_data={},
            fetch_ok=False,
        )
        result = await orch.process_query("wildfires in amazon")

        assert "error" in result
        assert result["stage"] == "fetch"
        # Downstream agents must NOT have been called
        orch.analyzer.run.assert_not_called()
        orch.predictor.run.assert_not_called()
        orch.web3.run.assert_not_called()

    @pytest.mark.asyncio
    async def test_pipeline_analysis_failure_short_circuits(
        self, mock_fetch_data, mock_analysis_data, mock_prediction_data
    ):
        orch = _make_orchestrator_with_mocks(
            mock_fetch_data,
            mock_analysis_data,
            mock_prediction_data,
            web3_data={},
            analysis_ok=False,
        )
        result = await orch.process_query("wildfires in amazon")

        assert result["stage"] == "analyze"
        orch.predictor.run.assert_not_called()
        orch.web3.run.assert_not_called()

    @pytest.mark.asyncio
    async def test_pipeline_predict_failure_short_circuits(
        self, mock_fetch_data, mock_analysis_data, mock_prediction_data
    ):
        orch = _make_orchestrator_with_mocks(
            mock_fetch_data,
            mock_analysis_data,
            mock_prediction_data,
            web3_data={},
            predict_ok=False,
        )
        result = await orch.process_query("wildfires in amazon")

        assert result["stage"] == "predict"
        orch.web3.run.assert_not_called()

    @pytest.mark.asyncio
    async def test_pipeline_web3_failure_is_non_fatal(
        self, mock_fetch_data, mock_analysis_data, mock_prediction_data
    ):
        """Web3 failure should NOT short-circuit – pipeline still returns analysis."""
        orch = _make_orchestrator_with_mocks(
            mock_fetch_data,
            mock_analysis_data,
            mock_prediction_data,
            web3_data={},
            web3_ok=False,
        )
        result = await orch.process_query("wildfires in amazon")

        # Should NOT have a top-level "error" key
        assert "error" not in result
        # Web3 sub-dict should contain the error
        assert "error" in result["web3"]
        # Upstream data still present
        assert "analysis" in result
        assert "prediction" in result

    @pytest.mark.asyncio
    async def test_progress_callbacks_fired(
        self, mock_fetch_data, mock_analysis_data, mock_prediction_data
    ):
        """Registered progress callbacks should be called during the pipeline."""
        web3_data = {
            "alert_message": "msg",
            "tx_hash": "0x01",
            "nft": {},
            "unibase": {"cid": "baf"},
            "virtual_protocol": {"action_id": "vp"},
        }
        orch = _make_orchestrator_with_mocks(
            mock_fetch_data, mock_analysis_data, mock_prediction_data, web3_data
        )

        messages: list[str] = []
        orch.on_progress(messages.append)

        await orch.process_query("wildfires in amazon")

        assert len(messages) >= 4  # at least one per stage + final

    @pytest.mark.asyncio
    async def test_scan_scheduled_returns_list(
        self, mock_fetch_data, mock_analysis_data, mock_prediction_data
    ):
        """scan_scheduled() should gather results for all supplied regions."""
        web3_data = {
            "alert_message": "msg",
            "tx_hash": "0x01",
            "nft": {},
            "unibase": {"cid": "baf"},
            "virtual_protocol": {"action_id": "vp"},
        }
        orch = _make_orchestrator_with_mocks(
            mock_fetch_data, mock_analysis_data, mock_prediction_data, web3_data
        )
        results = await orch.scan_scheduled(regions=["amazon", "uk"])

        assert isinstance(results, list)
        assert len(results) == 2

    @pytest.mark.asyncio
    async def test_scan_scheduled_skips_failed_regions(
        self, mock_fetch_data, mock_analysis_data, mock_prediction_data
    ):
        """Regions that raise exceptions during scan should be silently skipped."""
        from orchestrator.core import EcoClawOrchestrator

        orch = EcoClawOrchestrator()

        call_count = 0

        async def _failing_process(query, **kwargs):
            nonlocal call_count
            call_count += 1
            if "amazon" in query:
                raise RuntimeError("Simulated scan failure")
            return {
                "query": query,
                "fetch": mock_fetch_data,
                "analysis": mock_analysis_data,
                "prediction": mock_prediction_data,
                "web3": {},
                "alert_message": "",
            }

        orch.process_query = _failing_process  # type: ignore[method-assign]
        results = await orch.scan_scheduled(regions=["amazon", "uk"])

        assert call_count == 2
        # amazon failed → only uk in valid results
        assert len(results) == 1

    @pytest.mark.asyncio
    async def test_agent_states_returns_all_four(
        self, mock_fetch_data, mock_analysis_data, mock_prediction_data
    ):
        web3_data = {
            "alert_message": "",
            "tx_hash": "0x01",
            "nft": {},
            "unibase": {"cid": "baf"},
            "virtual_protocol": {"action_id": "vp"},
        }
        orch = _make_orchestrator_with_mocks(
            mock_fetch_data, mock_analysis_data, mock_prediction_data, web3_data
        )
        states = orch.agent_states()
        assert set(states.keys()) == {"fetcher", "analyzer", "predictor", "web3"}
