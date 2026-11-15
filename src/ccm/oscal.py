"""Phased OSCAL Assessment Results exporter.

Maps ArchAudit CCM state (evaluations, drifts, actions, metrics) into a minimal
OSCAL AR JSON structure suitable for continuous monitoring exchange.
Not a full OSCAL 1.1+ document; focuses on the results + observations that
auditors and other systems can consume.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

from src.ccm.state import CCMState


def _iso(dt: datetime | None = None) -> str:
    if dt is None:
        dt = datetime.now(timezone.utc)
    return dt.isoformat().replace("+00:00", "Z")


def to_oscal_assessment_results(state: CCMState) -> dict[str, Any]:
    """Produce a minimal OSCAL Assessment Results document."""
    now = _iso()
    result_uuid = str(uuid4())
    ar = {
        "assessment-results": {
            "uuid": str(uuid4()),
            "metadata": {
                "title": f"ArchAudit CCM Assessment Results {state.run_id}",
                "last-modified": now,
                "version": "0.1.0",
                "oscal-version": "1.1.2",
                "props": [
                    {"name": "decision-basis", "value": state.metrics.get("decision_basis", "deterministic")},
                    {"name": "journey-status", "value": state.metrics.get("journey_status", "")},
                    {"name": "evidence-chain-root", "value": state.metrics.get("evidence_chain_root", "")},
                ],
            },
            "results": [
                {
                    "uuid": result_uuid,
                    "title": f"CCM run {state.run_id}",
                    "description": "Deterministic continuous control monitoring results from ArchAudit.",
                    "start": now,
                    "end": now,
                    "reviewed-controls": {
                        "control-selections": [
                            {
                                "description": "Controls evaluated in this run",
                                "include-controls": [
                                    {"control-id": e.control_id} for e in state.evaluations
                                ],
                            }
                        ]
                    },
                    "observations": [
                        {
                            "uuid": str(uuid4()),
                            "title": f"Evaluation {ev.control_id}",
                            "description": ev.detail or ev.rule or "",
                            "methods": ["TEST"],
                            "collected": now,
                            "props": [
                                {"name": "status", "value": ev.status},
                                {"name": "decision-basis", "value": ev.decision_basis},
                            ],
                            "relevant-evidence": [
                                {"href": f"#evidence-{eid}", "description": "content-hashed evidence"}
                                for eid in ev.evidence_ids
                            ],
                        }
                        for ev in state.evaluations
                    ],
                    "findings": [
                        {
                            "uuid": str(uuid4()),
                            "title": f"Finding for {ev.control_id}",
                            "description": ev.detail or "",
                            "target": {
                                "type": "objective-id",
                                "target-id": ev.control_id,
                                "status": {"state": "satisfied" if ev.status == "pass" else "not-satisfied"},
                            },
                        }
                        for ev in state.evaluations
                        if ev.status in ("pass", "fail")
                    ],
                }
            ],
        }
    }
    return ar


def write_oscal(state: CCMState, output_dir: Path | None = None) -> Path:
    """Write OSCAL AR JSON next to the audit pack."""
    out = output_dir or Path(__file__).resolve().parents[2] / "samples" / "audit_pack"
    out.mkdir(parents=True, exist_ok=True)
    path = out / "assessment-results.oscal.json"
    data = to_oscal_assessment_results(state)
    with path.open("w") as f:
        json.dump(data, f, indent=2, default=str)
    return path
