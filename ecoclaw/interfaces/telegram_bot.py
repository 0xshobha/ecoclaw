"""interfaces/telegram_bot.py
EcoClaw Telegram bot – human-in-the-loop channel.

Implements both "Claw for Human" (agents assist users) and
"Human for Claw" (users approve / refine agent actions).

Commands:
  /start | /help  – welcome message
  /scan <query>   – run the full 4-agent pipeline
  /status         – last scan summary
  /register <0x>  – link wallet for NFT rewards
  /agents         – list loaded agents

Free-text messages that sound like climate queries trigger an
inline confirmation keyboard (human-in-the-loop gate) before
the agent swarm is dispatched.
"""

from __future__ import annotations

import asyncio
from typing import Any

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
)
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from config.settings import settings
from orchestrator.core import EcoClawOrchestrator
from utils.logger import log

# ── Static message templates ─────────────────────────────────────────────────

_WELCOME = """\
🌍 *Welcome to EcoClaw* – AI Agent Network for Climate Good

I coordinate a swarm of autonomous agents that monitor the planet using:
  • 🛰️ Satellite imagery (NASA + Compression Company)
  • 🤖 FLock federated LLMs + Z.AI compound reasoning
  • 🔗 Animoca NFT rewards on the Base blockchain
  • 💾 Unibase decentralised storage for immutable alerts
  • 🤖 Virtual Protocol for on-chain agent reputation

*Commands*
`/scan <region> <event>` – run a climate scan
`/status` – show last scan summary
`/register <0x…>` – link your wallet for NFT rewards
`/agents` – list active agents
`/help` – this message

_Example: `/scan amazon deforestation`_
"""

_CLIMATE_KEYWORDS = {
    "scan",
    "analyze",
    "analyse",
    "monitor",
    "flood",
    "fire",
    "wildfire",
    "deforestation",
    "drought",
    "storm",
    "hurricane",
    "climate",
    "satellite",
    "forest",
    "deforest",
}


class EcoClawTelegramBot:
    """Telegram interface for the EcoClaw multi-agent system."""

    def __init__(self) -> None:
        self._orch = EcoClawOrchestrator()
        self._wallets: dict[int, str] = {}  # user_id → wallet address
        self._app: Application | None = None

    # ── Build & run ───────────────────────────────────────────────────────────

    def build(self) -> Application:
        self._app = Application.builder().token(settings.telegram_token).build()

        # Commands
        self._app.add_handler(CommandHandler(["start", "help"], self._cmd_help))
        self._app.add_handler(CommandHandler("scan", self._cmd_scan))
        self._app.add_handler(CommandHandler("status", self._cmd_status))
        self._app.add_handler(CommandHandler("register", self._cmd_register))
        self._app.add_handler(CommandHandler("agents", self._cmd_agents))

        # Inline keyboard callbacks
        self._app.add_handler(
            CallbackQueryHandler(self._cb_confirm, pattern=r"^confirm_scan:")
        )
        self._app.add_handler(
            CallbackQueryHandler(self._cb_cancel, pattern=r"^confirm_cancel$")
        )

        # Free-text messages
        self._app.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self._handle_text)
        )

        log.info("[TelegramBot] Handlers registered")
        return self._app

    def run(self) -> None:
        app = self.build()
        if settings.webhook_url:
            # ── Webhook mode (preferred for production) ──────────────────
            log.info(f"[TelegramBot] Webhook mode → {settings.webhook_url}")
            app.run_webhook(
                listen="0.0.0.0",
                port=settings.webhook_port,
                url_path=settings.telegram_token,
                webhook_url=f"{settings.webhook_url}/{settings.telegram_token}",
                secret_token=settings.webhook_secret,
                drop_pending_updates=True,
            )
        else:
            # ── Polling mode (dev / local) ────────────────────────────────
            log.info("[TelegramBot] Polling mode…")
            app.run_polling(drop_pending_updates=True)

    # ── Command handlers ──────────────────────────────────────────────────────

    async def _cmd_help(self, update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text(_WELCOME, parse_mode=ParseMode.MARKDOWN)

    async def _cmd_scan(self, update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
        if not ctx.args:
            await update.message.reply_text(
                "Usage: `/scan <region> [event_type]`\n"
                "Example: `/scan amazon deforestation`",
                parse_mode=ParseMode.MARKDOWN,
            )
            return
        query = " ".join(ctx.args)
        await self._run_pipeline(update, query)

    async def _cmd_status(self, update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
        states = self._orch.agent_states()
        fetch_state = states.get("fetcher", {}).get("last_fetch", {})
        analyze_state = states.get("analyzer", {}).get("last_analysis", {})

        if not fetch_state:
            await update.message.reply_text(
                "No scans run yet. Try `/scan amazon deforestation`.",
                parse_mode=ParseMode.MARKDOWN,
            )
            return

        msg = (
            "📊 *Last Scan Summary*\n"
            "─────────────────────\n"
            f"📍 Region: `{fetch_state.get('region', 'N/A')}`\n"
            f"⚡ Event: `{fetch_state.get('event_type', 'N/A')}`\n"
            f"🌐 Active events: `{fetch_state.get('nasa_events', {}).get('count', 0)}`\n"
            f"📊 Risk score: *{analyze_state.get('composite_risk_score', 'N/A')}/100*\n"
            f"🔥 Level: *{str(analyze_state.get('risk_level', 'N/A')).upper()}*\n"
            f"📐 Affected: `{analyze_state.get('affected_area_km2', 0):.1f} km²`"
        )
        await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)

    async def _cmd_register(
        self, update: Update, ctx: ContextTypes.DEFAULT_TYPE
    ) -> None:
        if not ctx.args:
            await update.message.reply_text(
                "Usage: `/register <0x_wallet_address>`",
                parse_mode=ParseMode.MARKDOWN,
            )
            return

        wallet = ctx.args[0].strip()
        if not (wallet.startswith("0x") and len(wallet) == 42):
            await update.message.reply_text(
                "❌ Invalid address. Must be `0x…` (42 chars).",
                parse_mode=ParseMode.MARKDOWN,
            )
            return

        user_id = update.effective_user.id
        self._wallets[user_id] = wallet
        await update.message.reply_text(
            f"✅ Wallet registered: `{wallet[:6]}…{wallet[-4:]}`\n"
            "You'll receive NFT rewards for verified climate contributions!",
            parse_mode=ParseMode.MARKDOWN,
        )

    async def _cmd_agents(self, update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
        agents = [
            self._orch.fetcher,
            self._orch.analyzer,
            self._orch.predictor,
            self._orch.web3,
        ]
        lines = ["🤖 *Loaded EcoClaw Agents*\n"]
        for i, agent in enumerate(agents, 1):
            lines.append(f"{i}. *{agent.name}*\n   _{agent.description}_")
        await update.message.reply_text("\n".join(lines), parse_mode=ParseMode.MARKDOWN)

    # ── Free-text handler (human-in-the-loop) ────────────────────────────────

    async def _handle_text(
        self, update: Update, ctx: ContextTypes.DEFAULT_TYPE
    ) -> None:
        text = update.message.text.lower()
        words = set(text.split())

        if words & _CLIMATE_KEYWORDS:
            # Present confirmation keyboard before dispatching agents
            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "✅ Dispatch Agents",
                            callback_data=f"confirm_scan:{text[:200]}",
                        ),
                        InlineKeyboardButton(
                            "❌ Cancel",
                            callback_data="confirm_cancel",
                        ),
                    ]
                ]
            )
            await update.message.reply_text(
                f"🤖 EcoClaw detected a climate query:\n\n*{text[:120]}*\n\n"
                "Confirm to dispatch the 4-agent swarm?",
                reply_markup=keyboard,
                parse_mode=ParseMode.MARKDOWN,
            )
        else:
            await update.message.reply_text(
                "I'm EcoClaw 🌍 – a climate AI agent swarm.\n"
                "Try `/scan amazon deforestation` or `/help`.",
                parse_mode=ParseMode.MARKDOWN,
            )

    # ── Inline keyboard callbacks ─────────────────────────────────────────────

    async def _cb_confirm(self, update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
        query = update.callback_query
        await query.answer()

        task_query = query.data.split(":", 1)[1]
        await query.edit_message_text(
            f"🚀 Dispatching agents for:\n*{task_query[:120]}*",
            parse_mode=ParseMode.MARKDOWN,
        )
        # Hand off to the pipeline (sends results to same chat)
        await self._run_pipeline(query, task_query, from_callback=True)

    async def _cb_cancel(self, update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text("❌ Scan cancelled.")

    # ── Core pipeline runner ─────────────────────────────────────────────────

    async def _run_pipeline(
        self,
        update_or_query: Any,
        query_text: str,
        from_callback: bool = False,
    ) -> None:
        """Dispatch the orchestrator pipeline and send streaming updates."""
        # Resolve the chat object
        if from_callback:
            message = update_or_query.message
        else:
            message = update_or_query.message

        user_id = (
            update_or_query.effective_user.id
            if hasattr(update_or_query, "effective_user")
            and update_or_query.effective_user
            else 0
        )
        wallet = self._wallets.get(
            user_id, "0x0000000000000000000000000000000000000000"
        )

        # Create a mutable "status" message we'll edit as stages complete
        status_msg = await message.reply_text(
            "⏳ Agents dispatched – scanning…", parse_mode=ParseMode.MARKDOWN
        )

        # Register progress callback to keep status_msg updated
        async def _update_status(text: str) -> None:
            try:
                await status_msg.edit_text(text, parse_mode=ParseMode.MARKDOWN)
            except Exception:
                pass  # edit may fail if message is too old or unchanged

        progress_queue: asyncio.Queue[str] = asyncio.Queue()

        def _sync_cb(msg: str) -> None:
            progress_queue.put_nowait(msg)

        # Wire progress callback
        self._orch.on_progress(_sync_cb)

        # Consume progress updates while the pipeline runs
        async def _drain() -> None:
            while True:
                msg = await progress_queue.get()
                await _update_status(msg)
                if msg.startswith("✅"):
                    break

        pipeline_task = asyncio.create_task(
            self._orch.process_query(query_text, wallet)
        )
        drain_task = asyncio.create_task(_drain())

        result = await pipeline_task
        await drain_task

        # ── Render final response ────────────────────────────────────────
        if "error" in result:
            await status_msg.edit_text(
                f"❌ Pipeline error at stage `{result.get('stage', '?')}`:\n"
                f"{result['error']}",
                parse_mode=ParseMode.MARKDOWN,
            )
            return

        analysis = result.get("analysis", {})
        prediction = result.get("prediction", {})
        web3 = result.get("web3", {})

        response = (
            "🛰️ *EcoClaw Scan Results*\n"
            "━━━━━━━━━━━━━━━━\n"
            f"📍 Region: `{result.get('region', 'N/A')}`\n"
            f"⚡ Event: `{analysis.get('event_type', 'N/A')}`\n"
            f"📊 Risk Score: *{analysis.get('composite_risk_score', 0)}/100*\n"
            f"🔥 Level: *{prediction.get('severity', 'N/A').upper()}*\n"
            f"📐 Affected Area: `{analysis.get('affected_area_km2', 0):.1f} km²`\n"
            f"🌿 NDVI Δ: `{analysis.get('ndvi_stats', {}).get('ndvi_delta', 0):.4f}`\n"
            f"🔄 Change: `{analysis.get('change_percent', 0):.1f}%`\n"
            "━━━━━━━━━━━━━━━━\n"
        )

        flock_text = prediction.get("flock_assessment", "")[:320]
        if flock_text:
            response += f"🤖 *FLock Assessment:*\n_{flock_text}_\n\n"

        zai_summary = prediction.get("zai_summary", "")[:240]
        if zai_summary:
            response += f"⚙️ *Z.AI Reasoning:*\n_{zai_summary}_\n\n"

        actions = prediction.get("zai_actions", [])
        if actions:
            response += "✅ *Recommended Actions:*\n"
            for i, action in enumerate(actions[:4], 1):
                response += f"  {i}\\. {action}\n"
            response += "\n"

        tx = web3.get("tx_hash", "")
        if tx:
            response += f"🔗 *On-chain Alert:* `{tx[:22]}…`\n"

        nft_tx = web3.get("nft", {}).get("tx_hash", "")
        if nft_tx:
            response += f"🏆 *NFT Reward Minted:* `{nft_tx[:22]}…`\n"

        unibase_cid = web3.get("unibase", {}).get("cid", "")
        if unibase_cid:
            response += f"💾 *Unibase CID:* `{unibase_cid[:22]}…`\n"

        vp_action = web3.get("virtual_protocol", {}).get("action_id", "")
        if vp_action:
            response += f"🤖 *VP Action:* `{vp_action[:22]}…`\n"

        # Edit the status message to the full result
        try:
            await status_msg.edit_text(response, parse_mode=ParseMode.MARKDOWN)
        except Exception:
            # Fallback: send as new message if edit fails (e.g., too long)
            await message.reply_text(response, parse_mode=ParseMode.MARKDOWN)

        # ── Send NDVI chart as photo if available ────────────────────────
        chart_path = analysis.get("chart_path")
        if chart_path:
            try:
                from pathlib import Path

                p = Path(chart_path)
                if p.exists():
                    with p.open("rb") as f:
                        await message.reply_photo(
                            photo=f,
                            caption=f"📊 NDVI Change Chart – {result.get('region', '')}",
                        )
            except Exception as exc:
                log.warning(f"[TelegramBot] Could not send chart: {exc}")
