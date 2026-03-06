from __future__ import annotations

from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # ── Telegram ────────────────────────────────────────────────────────────
    telegram_token: str = "YOUR_TELEGRAM_BOT_TOKEN"

    # ── FLock.io  (OpenAI-compatible federated LLM) ─────────────────────────
    flock_api_key: str = "YOUR_FLOCK_API_KEY"
    flock_api_base: str = "https://api.flock.io/v1"
    flock_model: str = "flock-eco-large"

    # ── Z.AI  (compound AI reasoning) ───────────────────────────────────────
    zai_api_key: str = "YOUR_ZAI_API_KEY"
    zai_api_base: str = "https://api.z.ai/v1"
    zai_model: str = "z-compound-v1"

    # ── NASA Earthdata / EONET  (free) ──────────────────────────────────────
    nasa_api_key: str = "DEMO_KEY"

    # ── Compression Company Satellite SDK ───────────────────────────────────
    compression_api_key: Optional[str] = None
    compression_api_base: str = "https://api.compressionco.io/v1"

    # ── Web3 / Animoca  (Base chain) ────────────────────────────────────────
    web3_rpc_url: str = "https://mainnet.base.org"
    wallet_private_key: Optional[str] = None
    wallet_address: Optional[str] = None          # Public address (0x...)
    nft_contract_address: str = "0x0000000000000000000000000000000000000000"

    # ── Unibase  (on-chain storage) ──────────────────────────────────────────
    unibase_api_key: Optional[str] = None   # Legacy; AIP uses wallet identity now
    aip_endpoint: str = "http://api.aip.unibase.com"
    aip_gateway_url: str = "http://gateway.aip.unibase.com"

    # ── Virtual Protocol  (agent NFTs) ──────────────────────────────────────
    virtual_protocol_api_key: Optional[str] = None
    virtual_protocol_agent_id: str = "ecoclaw-agent-v1"

    # ── Telegram webhook  (set for production; leave empty for polling) ──────
    webhook_url: Optional[str] = None  # e.g. https://yourdomain.com/webhook
    webhook_port: int = 8443
    webhook_secret: Optional[str] = None

    # ── Application ─────────────────────────────────────────────────────────
    mock_mode: bool = True  # flip False when live keys are present
    log_level: str = "INFO"
    data_dir: str = "data"
    log_dir: str = "logs"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
