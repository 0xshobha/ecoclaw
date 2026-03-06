"""skills/animoca_web3.py
Animoca Brands / Base-chain Web3 skill.

Responsibilities:
  • post_on_chain_alert  – stores an alert hash on the Base blockchain
  • mint_contributor_nft – mints an ERC-721 NFT reward for a contributor

Uses web3.py when WALLET_PRIVATE_KEY is set and MOCK_MODE=false.
Gracefully falls back to mock transactions otherwise.
"""

from __future__ import annotations

import hashlib
from typing import Any

from config.settings import settings
from utils.logger import log
from utils.helpers import utcnow_iso

# ── Optional web3 import ─────────────────────────────────────────────────────
try:
    from web3 import Web3
    from eth_account import Account

    _WEB3_AVAILABLE = True
except ImportError:
    _WEB3_AVAILABLE = False
    log.warning("[AnimocaWeb3] web3 package not installed – running in mock mode")

# ── Minimal ERC-721 ABI (safeMint only) ─────────────────────────────────────
_ERC721_ABI = [
    {
        "inputs": [
            {"internalType": "address", "name": "to", "type": "address"},
            {"internalType": "string", "name": "tokenURI", "type": "string"},
        ],
        "name": "safeMint",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "nonpayable",
        "type": "function",
    }
]


class AnimocaWeb3Skill:
    """Animoca Brands NFT rewards + Base-chain on-chain alerts."""

    def __init__(self) -> None:
        self._w3: Any = None
        self._account: Any = None
        self._live = False

        if _WEB3_AVAILABLE and settings.wallet_private_key and not settings.mock_mode:
            try:
                self._w3 = Web3(Web3.HTTPProvider(settings.web3_rpc_url))
                self._account = Account.from_key(settings.wallet_private_key)
                # Only go live if contract is not the zero-address placeholder
                _null = "0x" + "0" * 40
                _has_contract = settings.nft_contract_address.lower() != _null.lower()
                self._live = self._w3.is_connected() and _has_contract
                log.info(
                    f"[AnimocaWeb3] Connected to Base chain "
                    f"(address={self._account.address[:10]}…, live={self._live}, "
                    f"contract={'set' if _has_contract else 'placeholder-only'})"
                )
            except Exception as exc:
                log.warning(f"[AnimocaWeb3] Init error: {exc} – mock mode")

    # ── Public API ────────────────────────────────────────────────────────────

    async def post_on_chain_alert(self, alert: dict[str, Any]) -> str:
        """
        Commit an alert hash to the Base blockchain.
        Returns the transaction hash (real or mock).
        """
        alert_hash = self._hash_alert(alert)

        if self._live:
            return self._live_store(alert_hash)

        mock_tx = "0x" + hashlib.sha256(alert_hash.encode()).hexdigest()
        log.info(f"[AnimocaWeb3] Mock on-chain alert: {mock_tx[:20]}…")
        return mock_tx

    async def mint_contributor_nft(
        self,
        recipient_address: str,
        alert_id: str,
        region: str,
        severity: str,
    ) -> dict[str, Any]:
        """
        Mint an ERC-721 NFT reward for a verified climate contributor.
        Returns a dict with tx_hash and metadata.
        """
        token_uri = self._build_token_uri(alert_id, region, severity)

        if self._live:
            return self._live_mint(recipient_address, token_uri)

        return self._mock_mint(recipient_address, alert_id, token_uri)

    # ── Live (on-chain) helpers ───────────────────────────────────────────────

    def _live_store(self, alert_hash: str) -> str:
        """Emit a transaction that stores the alert hash on-chain."""
        try:
            contract = self._w3.eth.contract(
                address=Web3.to_checksum_address(settings.nft_contract_address),
                abi=_ERC721_ABI,
            )
            tx = contract.functions.safeMint(
                self._account.address, alert_hash
            ).build_transaction(
                {
                    "from": self._account.address,
                    "nonce": self._w3.eth.get_transaction_count(self._account.address),
                    "gas": 200_000,
                    "gasPrice": self._w3.eth.gas_price,
                }
            )
            signed = self._w3.eth.account.sign_transaction(tx, self._account.key)
            tx_hash = self._w3.eth.send_raw_transaction(signed.raw_transaction)
            log.info(f"[AnimocaWeb3] Alert stored on-chain: {tx_hash.hex()[:20]}…")
            return tx_hash.hex()
        except Exception as exc:
            log.warning(f"[AnimocaWeb3] Live store error: {exc}")
            return "0x" + hashlib.sha256(alert_hash.encode()).hexdigest()

    def _live_mint(self, recipient: str, token_uri: str) -> dict[str, Any]:
        """Mint NFT on-chain via the ERC-721 contract."""
        try:
            contract = self._w3.eth.contract(
                address=Web3.to_checksum_address(settings.nft_contract_address),
                abi=_ERC721_ABI,
            )
            tx = contract.functions.safeMint(
                Web3.to_checksum_address(recipient), token_uri
            ).build_transaction(
                {
                    "from": self._account.address,
                    "nonce": self._w3.eth.get_transaction_count(self._account.address),
                    "gas": 250_000,
                    "gasPrice": self._w3.eth.gas_price,
                }
            )
            signed = self._w3.eth.account.sign_transaction(tx, self._account.key)
            tx_hash = self._w3.eth.send_raw_transaction(signed.raw_transaction)
            log.info(f"[AnimocaWeb3] NFT minted: {tx_hash.hex()[:20]}…")
            return {
                "success": True,
                "tx_hash": tx_hash.hex(),
                "recipient": recipient,
                "token_uri": token_uri,
                "network": settings.web3_rpc_url,
                "minted_at": utcnow_iso(),
            }
        except Exception as exc:
            log.warning(f"[AnimocaWeb3] Live mint error: {exc} – returning mock")
            return self._mock_mint(recipient, "fallback", token_uri)

    # ── Mock fallbacks ────────────────────────────────────────────────────────

    def _mock_mint(
        self,
        recipient: str,
        alert_id: str,
        token_uri: str,
    ) -> dict[str, Any]:
        mock_tx = "0x" + hashlib.sha256(f"{recipient}{alert_id}".encode()).hexdigest()
        return {
            "success": True,
            "tx_hash": mock_tx,
            "recipient": recipient,
            "token_uri": token_uri,
            "network": "base-mock",
            "minted_at": utcnow_iso(),
            "note": "Mock tx – set WALLET_PRIVATE_KEY and MOCK_MODE=false for live minting",
        }

    # ── Utilities ─────────────────────────────────────────────────────────────

    @staticmethod
    def _hash_alert(alert: dict[str, Any]) -> str:
        import json

        data = json.dumps(alert, sort_keys=True, default=str)
        return hashlib.sha256(data.encode()).hexdigest()

    @staticmethod
    def _build_token_uri(alert_id: str, region: str, severity: str) -> str:
        slug = region.replace(" ", "_").lower()
        return f"https://ecoclaw.io/nft/{alert_id}?region={slug}&severity={severity}"
