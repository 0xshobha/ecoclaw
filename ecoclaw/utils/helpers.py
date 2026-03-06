from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any


# ── Time helpers ─────────────────────────────────────────────────────────────


def utcnow_iso() -> str:
    """Return current UTC time as ISO-8601 string."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def short_hash(data: str, length: int = 12) -> str:
    """Stable, short hex digest of an arbitrary string."""
    return hashlib.sha256(data.encode()).hexdigest()[:length]


# ── Alert builders ────────────────────────────────────────────────────────────


def build_alert(
    event_type: str,
    region: str,
    severity: str,
    details: dict[str, Any],
    tx_hash: str | None = None,
) -> dict[str, Any]:
    """Construct a structured climate alert object."""
    ts = utcnow_iso()
    return {
        "id": short_hash(f"{event_type}{region}{ts}"),
        "event_type": event_type,
        "region": region,
        "severity": severity,
        "details": details,
        "tx_hash": tx_hash,
        "created_at": ts,
    }


def format_alert_message(alert: dict[str, Any]) -> str:
    """Format an alert dict into a Telegram-friendly Markdown string."""
    severity_emoji = {
        "low": "🟢",
        "medium": "🟡",
        "high": "🔴",
        "critical": "🚨",
    }.get(str(alert.get("severity", "")).lower(), "⚪")

    lines = [
        f"{severity_emoji} *EcoClaw Climate Alert*",
        f"📍 Region: `{alert['region']}`",
        f"⚡ Event: `{alert['event_type']}`",
        f"🔥 Severity: *{str(alert['severity']).upper()}*",
        "─────────────────────",
    ]

    for key, val in alert.get("details", {}).items():
        lines.append(f"  • {key}: `{val}`")

    if alert.get("tx_hash"):
        lines.append(f"🔗 On-chain TX: `{alert['tx_hash'][:20]}...`")

    lines.append(f"🕒 {alert['created_at']}")
    return "\n".join(lines)


# ── Misc ─────────────────────────────────────────────────────────────────────


def risk_score_to_severity(score: int) -> str:
    """Map a 0-100 integer risk score to a named severity level."""
    if score >= 80:
        return "critical"
    if score >= 60:
        return "high"
    if score >= 40:
        return "medium"
    return "low"


def safe_json(obj: Any) -> str:
    """Serialize obj to JSON, falling back to str() for non-serialisable types."""
    try:
        return json.dumps(obj, default=str, indent=2)
    except Exception:
        return str(obj)
