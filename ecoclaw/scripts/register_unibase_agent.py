#!/usr/bin/env python3
"""scripts/register_unibase_agent.py
One-time script to register EcoClaw as a named agent on the Unibase AIP platform.

Run once before going live:
    source venv/bin/activate
    python scripts/register_unibase_agent.py

The resulting agent_id is informational; the handle "ecoclaw_climate" is what
callers use.
"""

import asyncio
import os
import sys

# Ensure project root is on PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from dotenv import load_dotenv
load_dotenv()

from config.settings import settings
from skills.unibase import register_ecoclaw_agent
from utils.logger import log


async def main() -> None:
    wallet = settings.wallet_address or ""
    if not wallet:
        log.error("WALLET_ADDRESS not set in .env – cannot register agent")
        sys.exit(1)

    log.info(f"Registering EcoClaw agent | wallet={wallet[:12]}…")
    agent_id = await register_ecoclaw_agent(wallet)

    if agent_id:
        print(f"\n✓ EcoClaw registered on Unibase AIP!")
        print(f"  agent_id : {agent_id}")
        print(f"  handle   : ecoclaw_climate")
        print(f"  endpoint : http://api.aip.unibase.com")
        print("\nUpdate .env: AIP_AGENT_ID=" + agent_id)
    else:
        print("\n✗ Registration failed – check logs above.")
        print("  Tip: The AIP platform may be starting; retry in a few minutes.")
        print("  Unibase Discord: https://discord.gg/unibase for test credentials.")


if __name__ == "__main__":
    asyncio.run(main())
