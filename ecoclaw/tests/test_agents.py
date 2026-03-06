"""tests/test_agents.py
Unit tests for EcoClaw's four agents.

All skills / LLM calls are patched out so these tests run fully offline.
"""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

# ── FetcherAgent ──────────────────────────────────────────────────────────────


class TestFetcherAgent:
    """Tests for agents/fetcher.py FetcherAgent."""

    # -- _extract_region ---------------------------------------------------------

    def test_extract_region_simple(self):
        from agents.fetcher import FetcherAgent

        agent = FetcherAgent()
        assert agent._extract_region("wildfire in amazon rainforest") == "amazon"

    def test_extract_region_multi_word(self):
        from agents.fetcher import FetcherAgent

        agent = FetcherAgent()
        # "southeast asia" is a multi-word region – must be matched before "asia"
        region = agent._extract_region("floods in southeast asia")
        assert region == "southeast asia"

    def test_extract_region_case_insensitive(self):
        from agents.fetcher import FetcherAgent

        agent = FetcherAgent()
        assert agent._extract_region("FIRES IN AUSTRALIA") == "australia"

    def test_extract_region_fallback(self):
        from agents.fetcher import FetcherAgent

        agent = FetcherAgent()
        assert agent._extract_region("global climate emergency") == "amazon"

    # -- _extract_event_type -----------------------------------------------------

    def test_extract_event_type_wildfire(self):
        from agents.fetcher import FetcherAgent

        agent = FetcherAgent()
        assert (
            agent._extract_event_type("active wildfires spreading fast") == "wildfires"
        )

    def test_extract_event_type_deforestation_beats_fire(self):
        """'deforestation' keyword should take priority over 'fire'."""
        from agents.fetcher import FetcherAgent

        agent = FetcherAgent()
        result = agent._extract_event_type("deforestation and forest fire activity")
        assert result == "wildfires"  # deforestation maps to wildfires

    def test_extract_event_type_flood(self):
        from agents.fetcher import FetcherAgent

        agent = FetcherAgent()
        assert agent._extract_event_type("severe flooding downstream") == "floods"

    def test_extract_event_type_word_boundary(self):
        """'ice' should not match inside 'service'."""
        from agents.fetcher import FetcherAgent

        agent = FetcherAgent()
        # "service" contains "ice" but word-boundary regex must not match
        result = agent._extract_event_type("national weather service update")
        assert result == "wildfires"  # falls back to default

    def test_extract_event_type_fallback(self):
        from agents.fetcher import FetcherAgent

        agent = FetcherAgent()
        assert agent._extract_event_type("just checking") == "wildfires"

    # -- run() -------------------------------------------------------------------

    @pytest.mark.asyncio
    async def test_run_returns_success(self, mock_fetch_data):
        """FetcherAgent.run() should return AgentResult(success=True) with mocked satellite."""
        from agents.fetcher import FetcherAgent

        mock_satellite = MagicMock()
        mock_satellite.fetch_nasa_events = AsyncMock(
            return_value=mock_fetch_data["nasa_events"]
        )
        mock_satellite.fetch_earth_imagery_meta = AsyncMock(
            return_value=mock_fetch_data["imagery_metadata"]
        )
        mock_satellite.fetch_compression_analysis = AsyncMock(
            return_value=mock_fetch_data["compression_analysis"]
        )

        with patch("agents.fetcher.SatelliteSkill", return_value=mock_satellite):
            agent = FetcherAgent()
            result = await agent.run({"query": "wildfires in amazon"})

        assert result.success is True
        assert "region" in result.data
        assert "nasa_events" in result.data
        assert result.data["region"] == "amazon"

    @pytest.mark.asyncio
    async def test_run_empty_query_falls_back(self):
        """FetcherAgent should still succeed with an empty/no-keyword query."""
        from agents.fetcher import FetcherAgent

        with patch("agents.fetcher.SatelliteSkill") as MockSat:
            instance = MockSat.return_value
            instance.fetch_nasa_events = AsyncMock(
                return_value={"source": "mock", "count": 0, "events": []}
            )
            instance.fetch_earth_imagery_meta = AsyncMock(
                return_value={"source": "mock"}
            )
            instance.fetch_compression_analysis = AsyncMock(
                return_value={
                    "source": "mock",
                    "change_percent": 0.0,
                    "confidence": 0.5,
                    "affected_area_km2": 0.0,
                    "ndvi_delta": 0.0,
                    "severity": "low",
                }
            )
            agent = FetcherAgent()
            result = await agent.run({"query": ""})

        assert result.success is True


# ── AnalyzerAgent ─────────────────────────────────────────────────────────────


class TestAnalyzerAgent:
    """Tests for agents/analyzer.py AnalyzerAgent."""

    def _make_agent(self):
        from agents.analyzer import AnalyzerAgent

        return AnalyzerAgent()

    # -- _ndvi_change_detection --------------------------------------------------

    def test_ndvi_keys_present(self):
        agent = self._make_agent()
        stats = agent._ndvi_change_detection(10.0)
        for key in (
            "ndvi_mean_before",
            "ndvi_mean_after",
            "ndvi_delta",
            "ndvi_std_before",
            "ndvi_std_after",
            "pixels_analysed",
        ):
            assert key in stats, f"Missing key: {key}"

    def test_ndvi_zero_change(self):
        agent = self._make_agent()
        stats = agent._ndvi_change_detection(0.0)
        # With 0% change, after should be close to before
        assert abs(stats["ndvi_mean_after"] - stats["ndvi_mean_before"]) < 0.1

    def test_ndvi_high_change(self):
        agent = self._make_agent()
        stats = agent._ndvi_change_detection(80.0)
        # After should be meaningfully lower than before
        assert stats["ndvi_mean_after"] < stats["ndvi_mean_before"]

    def test_ndvi_pixels_analysed(self):
        agent = self._make_agent()
        stats = agent._ndvi_change_detection(25.0)
        assert stats["pixels_analysed"] == 256

    # -- _composite_risk_score ---------------------------------------------------

    def test_risk_score_zero_input(self):
        agent = self._make_agent()
        score = agent._composite_risk_score(
            change_pct=0.0, event_count=0, confidence=0.0, severity_raw="low"
        )
        assert 0 <= score <= 100

    def test_risk_score_max_input(self):
        agent = self._make_agent()
        score = agent._composite_risk_score(
            change_pct=100.0, event_count=20, confidence=1.0, severity_raw="critical"
        )
        assert 0 <= score <= 100
        assert score > 70  # high inputs must yield high score

    def test_risk_score_clamped(self):
        """Score must always stay in [0, 100]."""
        agent = self._make_agent()
        for change in (0, 25, 50, 75, 100):
            score = agent._composite_risk_score(
                change_pct=change, event_count=5, confidence=0.8, severity_raw="high"
            )
            assert 0 <= score <= 100

    # -- _extract_hotspots -------------------------------------------------------

    def test_extract_hotspots_empty(self):
        agent = self._make_agent()
        assert agent._extract_hotspots([]) == []

    def test_extract_hotspots_single_event(self):
        agent = self._make_agent()
        events = [
            {
                "title": "Fire front advancing",
                "geometries": [
                    {
                        "date": "2026-01-01T00:00:00Z",
                        "type": "Point",
                        "coordinates": [-55.0, -5.0],
                    }
                ],
            }
        ]
        hotspots = agent._extract_hotspots(events)
        assert len(hotspots) == 1
        assert hotspots[0]["lon"] == -55.0
        assert hotspots[0]["lat"] == -5.0

    # -- run() -------------------------------------------------------------------

    @pytest.mark.asyncio
    async def test_run_success(self, mock_fetch_data):
        from agents.analyzer import AnalyzerAgent

        agent = AnalyzerAgent()
        with patch.object(agent, "_generate_ndvi_chart", return_value=None):
            result = await agent.run({"raw_data": mock_fetch_data})

        assert result.success is True
        data = result.data
        assert "composite_risk_score" in data
        assert "risk_level" in data
        assert "ndvi_stats" in data
        assert "hotspots" in data
        assert "chart_path" in data
        assert 0 <= data["composite_risk_score"] <= 100

    @pytest.mark.asyncio
    async def test_run_no_raw_data_fails(self):
        from agents.analyzer import AnalyzerAgent

        agent = AnalyzerAgent()
        result = await agent.run({})
        assert result.success is False
        assert "No raw_data" in (result.error or "")


# ── PredictorAgent ────────────────────────────────────────────────────────────


class TestPredictorAgent:
    """Tests for agents/predictor.py PredictorAgent."""

    @pytest.mark.asyncio
    async def test_run_returns_prediction(self, mock_analysis_data):
        from agents.predictor import PredictorAgent

        mock_flock_response = (
            "High fire danger in the Amazon. Immediate intervention needed."
        )
        mock_zai_response = {
            "summary": "Critical wildfire risk",
            "actions": ["Deploy drones", "Issue evacuation order"],
            "confidence": 0.91,
            "severity": "critical",
            "sources": ["NASA EONET"],
        }

        with (
            patch("agents.predictor.FlockLLMSkill") as MockFlock,
            patch("agents.predictor.ZAISkill") as MockZAI,
        ):
            flock_instance = MockFlock.return_value
            flock_instance.predict_climate_impact = AsyncMock(
                return_value=mock_flock_response
            )

            zai_instance = MockZAI.return_value
            zai_instance.compound_reasoning = AsyncMock(return_value=mock_zai_response)

            agent = PredictorAgent()
            result = await agent.run({"analysis": mock_analysis_data})

        assert result.success is True
        data = result.data
        assert "flock_assessment" in data
        assert "zai_summary" in data
        assert "risk_score" in data
        assert "severity" in data

    @pytest.mark.asyncio
    async def test_run_missing_analysis_fails(self):
        from agents.predictor import PredictorAgent

        with (
            patch("agents.predictor.FlockLLMSkill"),
            patch("agents.predictor.ZAISkill"),
        ):
            agent = PredictorAgent()
            result = await agent.run({})

        assert result.success is False


# ── Web3CoordinatorAgent ──────────────────────────────────────────────────────


class TestWeb3CoordinatorAgent:
    """Tests for agents/web3_agent.py Web3CoordinatorAgent."""

    def _mock_web3_agent(self):
        """Return a Web3CoordinatorAgent with all skills pre-patched."""
        from agents.web3_agent import Web3CoordinatorAgent

        agent = Web3CoordinatorAgent()
        agent.animoca = MagicMock()
        agent.animoca.post_on_chain_alert = AsyncMock(return_value="0xDEADBEEF00000001")
        agent.animoca.mint_contributor_nft = AsyncMock(
            return_value={
                "token_id": "1",
                "recipient": "0x0000000000000000000000000000000000000000",
                "tx_hash": "0xDEADBEEF00000002",
                "mock": True,
            }
        )
        agent.unibase = MagicMock()
        agent.unibase.store_alert = AsyncMock(
            return_value={
                "cid": "bafybeiTEST",
                "tx_hash": "0xUNIBASE_TX",
                "url": "https://gateway.unibase.io/ipfs/bafybeiTEST",
                "stored_at": "2026-03-04T12:00:00Z",
                "mock": True,
            }
        )
        agent.virtual_protocol = MagicMock()
        agent.virtual_protocol.register_agent_action = AsyncMock(
            return_value={
                "action_id": "vp-action-TEST",
                "agent_id": "ecoclaw-agent-v1",
                "tx_hash": "0xVP_TX",
                "vp_url": "https://app.virtual.protocol/actions/vp-action-TEST",
                "registered_at": "2026-03-04T12:00:00Z",
                "mock": True,
            }
        )
        return agent

    @pytest.mark.asyncio
    async def test_run_all_four_steps(self, mock_prediction_data):
        """All 4 on-chain steps should be called and result keys present."""
        agent = self._mock_web3_agent()
        result = await agent.run({"prediction": mock_prediction_data})

        assert result.success is True
        data = result.data

        # Verify all 4 result keys
        assert "tx_hash" in data
        assert "nft" in data
        assert "unibase" in data
        assert "virtual_protocol" in data
        assert "alert_message" in data

        # Verify each skill was called exactly once
        agent.animoca.post_on_chain_alert.assert_called_once()
        agent.animoca.mint_contributor_nft.assert_called_once()
        agent.unibase.store_alert.assert_called_once()
        agent.virtual_protocol.register_agent_action.assert_called_once()

    @pytest.mark.asyncio
    async def test_run_unibase_cid_present(self, mock_prediction_data):
        agent = self._mock_web3_agent()
        result = await agent.run({"prediction": mock_prediction_data})

        assert result.data["unibase"]["cid"] == "bafybeiTEST"

    @pytest.mark.asyncio
    async def test_run_vp_action_id_present(self, mock_prediction_data):
        agent = self._mock_web3_agent()
        result = await agent.run({"prediction": mock_prediction_data})

        assert result.data["virtual_protocol"]["action_id"] == "vp-action-TEST"

    @pytest.mark.asyncio
    async def test_run_no_prediction_fails(self):
        agent = self._mock_web3_agent()
        result = await agent.run({})

        assert result.success is False
        assert "No prediction" in (result.error or "")

    @pytest.mark.asyncio
    async def test_run_saves_state(self, mock_prediction_data):
        agent = self._mock_web3_agent()
        await agent.run({"prediction": mock_prediction_data})

        state = agent.get_state().get("last_web3_action")
        assert state is not None
        assert "alert" in state
