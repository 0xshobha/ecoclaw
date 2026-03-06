from __future__ import annotations

import sys
from pathlib import Path

from loguru import logger


def setup_logger(log_level: str = "INFO", log_dir: str = "logs") -> None:
    """Configure loguru for console + rotating file output."""
    Path(log_dir).mkdir(parents=True, exist_ok=True)

    logger.remove()  # drop default handler

    # ── Console ─────────────────────────────────────────────────────────────
    logger.add(
        sys.stdout,
        level=log_level,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan> – "
            "<level>{message}</level>"
        ),
        colorize=True,
    )

    # ── Rotating file ───────────────────────────────────────────────────────
    logger.add(
        Path(log_dir) / "ecoclaw_{time:YYYY-MM-DD}.log",
        level="DEBUG",
        rotation="00:00",  # new file every midnight
        retention="7 days",
        compression="gz",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function} – {message}",
    )


# Re-export so the rest of the codebase only imports from utils.logger
log = logger
