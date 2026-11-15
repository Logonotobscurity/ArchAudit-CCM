"""Generate a static HTML view of recent run history.

Reads samples/run_history.jsonl and writes a simple trend page.
File-based; no external services required.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HISTORY_PATH = ROOT / "samples" / "run_history.jsonl"
OUTPUT_PATH = ROOT / "samples" / "audit_pack" / "history.html"


def write_history_html(limit: int = 10) -> Path:
    """Write a simple HTML table of recent runs."""
    rows = []
    if HISTORY_PATH.exists():
        lines = HISTORY_PATH.read_text().splitlines()
        for line in lines[-limit:]:
            if not line.strip():
                continue
            snap = json.loads(line)
            fails = sum(1 for v in snap.get("evaluations", {}).values() if v.get("status") == "fail")
            total = len(snap.get("evaluations", {}))
            rows.append({
                "run_id": snap.get("run_id", "")[:8],
                "recorded_at": snap.get("recorded_at", "")[:19],
                "total": total,
                "fails": fails,
            })

    html = ["<!DOCTYPE html><html><head><title>CCM Run History</title></head><body>",
            "<h1>Recent CCM Runs</h1>",
            "<table border='1'><tr><th>Run</th><th>Time</th><th>Total</th><th>Fails</th></tr>"]
    for r in rows:
        html.append(f"<tr><td>{r['run_id']}</td><td>{r['recorded_at']}</td><td>{r['total']}</td><td>{r['fails']}</td></tr>")
    html.append("</table></body></html>")

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text("\n".join(html))
    return OUTPUT_PATH
