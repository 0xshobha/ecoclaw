#!/usr/bin/env python3
"""
EcoClaw – AI Multi-Agent Network for Climate Good
UK AI Agent Hackathon EP4 × OpenClaw

Usage
-----
  python main.py              Start Telegram bot (default)
  python main.py --demo       Run a demo pipeline query and exit
  python main.py --scan       Run a one-off scheduled scan and exit
  python main.py --query "…"  Use a custom query with --demo / --scan
"""
from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

# ── Ensure project root is on PYTHONPATH ─────────────────────────────────────
sys.path.insert(0, str(Path(__file__).parent))

from utils.logger import log, setup_logger
from config.settings import settings


# ── CLI ───────────────────────────────────────────────────────────────────────


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="ecoclaw",
        description="EcoClaw – Climate AI Agent Swarm",
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run a single demo pipeline query and print the results",
    )
    parser.add_argument(
        "--scan",
        action="store_true",
        help="Run a one-off scheduled multi-region scan and exit",
    )
    parser.add_argument(
        "--query",
        type=str,
        default="scan for wildfires in amazon",
        help="Climate query to use with --demo or --scan",
    )
    return parser.parse_args()


# ── Demo runner ───────────────────────────────────────────────────────────────


async def _run_demo(query: str) -> None:
    from orchestrator.core import EcoClawOrchestrator

    orch = EcoClawOrchestrator()

    def _progress(msg: str) -> None:
        # Strip markdown for clean console output
        clean = msg.replace("*", "").replace("_", "").replace("`", "")
        print(f"  → {clean}")

    orch.on_progress(_progress)

    print()
    print("=" * 64)
    print("  EcoClaw Demo Pipeline")
    print(f"  Query : {query}")
    print(f"  Mode  : {'MOCK' if settings.mock_mode else 'LIVE'}")
    print("=" * 64)

    result = await orch.process_query(query)

    if "error" in result:
        print(f"\n  ✗ Pipeline failed at stage '{result['stage']}': {result['error']}")
        return

    analysis = result.get("analysis", {})
    prediction = result.get("prediction", {})
    web3 = result.get("web3", {})

    print()
    print("─" * 64)
    print("  RESULTS")
    print("─" * 64)
    print(f"  Region         : {result.get('region')}")
    print(f"  Event type     : {analysis.get('event_type')}")
    print(f"  Risk score     : {analysis.get('composite_risk_score', 0)}/100")
    print(f"  Risk level     : {analysis.get('risk_level', 'N/A').upper()}")
    print(f"  Severity       : {prediction.get('severity', 'N/A').upper()}")
    print(f"  Confidence     : {prediction.get('confidence', 0):.0%}")
    print(f"  Change %       : {analysis.get('change_percent', 0):.1f} %")
    print(f"  Affected area  : {analysis.get('affected_area_km2', 0):.1f} km²")
    ndvi = analysis.get("ndvi_stats", {})
    print(f"  NDVI Δ         : {ndvi.get('ndvi_delta', 0):.4f}")
    print(f"  Active events  : {analysis.get('active_event_count', 0)}")

    print()
    flock = prediction.get("flock_assessment", "")
    if flock:
        print("  FLock Assessment:")
        for line in flock.split("\n")[:6]:
            print(f"    {line}")

    actions = prediction.get("zai_actions", [])
    if actions:
        print("\n  Z.AI Recommended Actions:")
        for i, action in enumerate(actions, 1):
            print(f"    {i}. {action}")

    tx = web3.get("tx_hash", "")
    if tx:
        print(f"\n  On-chain TX    : {tx[:50]}…")
    nft_tx = web3.get("nft", {}).get("tx_hash", "")
    if nft_tx:
        print(f"  NFT reward TX  : {nft_tx[:50]}…")

    print()
    print("=" * 64)
    print()


# ── Scan runner ───────────────────────────────────────────────────────────────


async def _run_scan() -> None:
    from orchestrator.core import EcoClawOrchestrator

    orch = EcoClawOrchestrator()
    results = await orch.scan_scheduled()

    print(f"\n  Scheduled scan complete – {len(results)} region(s) processed\n")
    for r in results:
        analysis = r.get("analysis", {})
        print(
            f"  {r.get('region', '?'):20s} "
            f"risk={analysis.get('composite_risk_score', 0):3d}/100  "
            f"level={analysis.get('risk_level', 'N/A').upper()}"
        )
    print()


# ── Bot runner ────────────────────────────────────────────────────────────────


def _run_bot() -> None:
    from interfaces.telegram_bot import EcoClawTelegramBot
    from orchestrator.scheduler import EcoClawScheduler

    bot = EcoClawTelegramBot()
    app = bot.build()

    # Attach background scheduler to the same orchestrator
    scheduler = EcoClawScheduler(bot._orch)

    async def _on_startup(application):  # noqa: ANN001
        scheduler.start()
        log.info("[main] Telegram bot + scheduler running")

    async def _on_shutdown(application):  # noqa: ANN001
        scheduler.stop()
        log.info("[main] Shutdown complete")

    app.post_init = _on_startup
    app.post_shutdown = _on_shutdown

    log.info("[main] Starting Telegram bot…")
    app.run_polling(drop_pending_updates=True)


# ── Entry point ───────────────────────────────────────────────────────────────


def main() -> None:
    setup_logger(log_level=settings.log_level, log_dir=settings.log_dir)
    args = _parse_args()

    log.info(
        f"EcoClaw starting | mock_mode={settings.mock_mode} | "
        f"log_level={settings.log_level}"
    )

    if args.demo:
        asyncio.run(_run_demo(args.query))
    elif args.scan:
        asyncio.run(_run_scan())
    else:
        _run_bot()


if __name__ == "__main__":
    main()
