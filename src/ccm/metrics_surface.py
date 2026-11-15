"""Lightweight metrics surface.

Generates a simple self-contained HTML view of the latest audit-pack metrics.
No server required; open the file or serve statically. Fits offline / low-bandwidth contexts.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
AUDIT_PACK = ROOT / "samples" / "audit_pack"


def render_html(metrics: dict | None = None) -> str:
    if metrics is None:
        metrics_path = AUDIT_PACK / "metrics.json"
        if metrics_path.exists():
            metrics = json.loads(metrics_path.read_text())
        else:
            metrics = {}
    cov = metrics.get("control_coverage_pct", 0)
    tte = metrics.get("time_to_evidence_minutes", 0)
    drift = metrics.get("drift_count", 0)
    fails = metrics.get("evaluations_fail", 0)
    open_ex = metrics.get("open_exceptions", 0)
    emitted = metrics.get("emitted_actions", 0)
    status = metrics.get("journey_status", "unknown")
    chain = metrics.get("evidence_chain_root", "")[:16] + "..." if metrics.get("evidence_chain_root") else ""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>ArchAudit CCM Metrics</title>
<style>
  body {{ font-family: system-ui, sans-serif; margin: 2rem; background: #111; color: #eee; }}
  .card {{ background: #222; padding: 1rem; margin: 0.5rem 0; border-radius: 8px; }}
  .metric {{ font-size: 1.4rem; font-weight: bold; }}
  .status {{ color: #4ade80; }}
</style>
</head>
<body>
<h1>ArchAudit CCM — Metrics Surface</h1>
<p>Journey status: <span class="status">{status}</span></p>
<div class="card"><div>Coverage</div><div class="metric">{cov}%</div></div>
<div class="card"><div>Time-to-Evidence</div><div class="metric">{tte} min</div></div>
<div class="card"><div>Drift count</div><div class="metric">{drift}</div></div>
<div class="card"><div>Failures</div><div class="metric">{fails}</div></div>
<div class="card"><div>Open exceptions</div><div class="metric">{open_ex}</div></div>
<div class="card"><div>Emitted actions</div><div class="metric">{emitted}</div></div>
<div class="card"><div>Evidence chain root</div><div class="metric">{chain}</div></div>
<p><small>Generated from samples/audit_pack/metrics.json — offline-friendly.</small></p>
</body>
</html>
"""


def write_html(output_path: Path | None = None) -> Path:
    path = output_path or AUDIT_PACK / "metrics.html"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_html())
    return path
