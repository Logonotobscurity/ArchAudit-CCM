"""Multi-run history retention.

Keeps the last N compact evaluation snapshots in a JSONL file so operators
can see trends. Fully offline-friendly; no external store required.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.ccm.state import EvaluationResult

ROOT = Path(__file__).resolve().parents[2]
HISTORY_PATH = ROOT / "samples" / "run_history.jsonl"
DEFAULT_KEEP = 10


def append_run_snapshot(
    evaluations: list[EvaluationResult],
    run_id: str,
    keep: int = DEFAULT_KEEP,
) -> None:
    """Append a compact snapshot and trim to the last `keep` entries."""
    HISTORY_PATH.parent.mkdir(parents=True, exist_ok=True)
    snapshot = {
        "run_id": run_id,
        "recorded_at": datetime.now(timezone.utc).isoformat(),
        "evaluations": {
            ev.control_id: {"status": ev.status, "detail": ev.detail}
            for ev in evaluations
        },
    }
    # Read existing lines
    lines: list[str] = []
    if HISTORY_PATH.exists():
        lines = HISTORY_PATH.read_text().splitlines()
    lines.append(json.dumps(snapshot))
    # Keep only the last N
    lines = lines[-keep:]
    HISTORY_PATH.write_text("\n".join(lines) + "\n")


def load_recent_snapshots(limit: int = 5) -> list[dict[str, Any]]:
    """Return the most recent snapshots (newest last)."""
    if not HISTORY_PATH.exists():
        return []
    lines = HISTORY_PATH.read_text().splitlines()
    recent = lines[-limit:]
    return [json.loads(line) for line in recent if line.strip()]
