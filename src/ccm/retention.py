"""Inbound evidence retention.

Removes files in samples/inbound/ older than a configurable age (default 7 days)
or exceeding a max count. Deterministic and offline-safe.
"""
from __future__ import annotations

import os
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INBOUND_DIR = ROOT / "samples" / "inbound"
DEFAULT_MAX_AGE_DAYS = 7
DEFAULT_MAX_FILES = 100


def cleanup_inbound(
    max_age_days: int | None = None,
    max_files: int | None = None,
) -> int:
    """Delete stale inbound evidence files. Returns number removed."""
    if not INBOUND_DIR.exists():
        return 0
    max_age = max_age_days or int(os.environ.get("ARCHAUDIT_INBOUND_MAX_AGE_DAYS", DEFAULT_MAX_AGE_DAYS))
    max_count = max_files or int(os.environ.get("ARCHAUDIT_INBOUND_MAX_FILES", DEFAULT_MAX_FILES))
    cutoff = time.time() - (max_age * 86400)

    files = sorted(INBOUND_DIR.glob("*.json"), key=lambda p: p.stat().st_mtime)
    removed = 0

    # Age-based
    for p in files:
        if p.stat().st_mtime < cutoff:
            p.unlink()
            removed += 1

    # Count-based (keep newest)
    remaining = sorted(INBOUND_DIR.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    for p in remaining[max_count:]:
        p.unlink()
        removed += 1

    return removed
