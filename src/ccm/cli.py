"""Operator CLI for ArchAudit CCM.

Usage:
  python -m src.ccm.cli run
  python -m src.ccm.cli status
  python -m src.ccm.cli verify-replay
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from src.ccm.nodes import run_pipeline

ROOT = Path(__file__).resolve().parents[2]
AUDIT_PACK = ROOT / "samples" / "audit_pack"


def cmd_run(_: argparse.Namespace) -> None:
    state = run_pipeline()
    print(json.dumps({"run_id": state.run_id, "journey_status": state.metrics.get("journey_status"), "coverage": state.metrics.get("control_coverage_pct")}, indent=2))


def cmd_status(_: argparse.Namespace) -> None:
    metrics_path = AUDIT_PACK / "metrics.json"
    if not metrics_path.exists():
        print("No audit pack found. Run first.")
        return
    print(metrics_path.read_text())


def cmd_verify_replay(_: argparse.Namespace) -> None:
    s1 = run_pipeline()
    s2 = run_pipeline()
    c1 = s1.metrics.get("evidence_chain_root")
    c2 = s2.metrics.get("evidence_chain_root")
    if c1 == c2:
        print("Offline replay stable — chain root identical")
    else:
        print(f"Chain root mismatch: {c1} vs {c2}")
        sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(description="ArchAudit CCM operator CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("run", help="Trigger a deterministic CCM run").set_defaults(func=cmd_run)
    sub.add_parser("status", help="Show latest metrics").set_defaults(func=cmd_status)
    sub.add_parser("verify-replay", help="Assert offline replay stability").set_defaults(func=cmd_verify_replay)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
