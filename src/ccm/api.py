"""Thin FastAPI surface so other systems can trigger CCM runs or push evidence.

Basic auth stub (replace with real auth in production).
Offline-replayable: returns the same audit pack metrics plus journey status.
Webhook ingest supports event-driven collection.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel

from src.ccm.nodes import run_pipeline
from src.ccm.state import EvidenceRecord

app = FastAPI(title="ArchAudit CCM", version="0.1.0")
security = HTTPBasic()

# Stub credentials — replace with proper secret management
_VALID_USER = "ccm"
_VALID_PASS = "changeme"
INBOUND_DIR = Path(__file__).resolve().parents[2] / "samples" / "inbound"


def _check_auth(credentials: HTTPBasicCredentials = Depends(security)) -> str:
    if credentials.username != _VALID_USER or credentials.password != _VALID_PASS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


def _journey_status(metrics: dict) -> str:
    fails = metrics.get("evaluations_fail", 0)
    emitted = metrics.get("emitted_actions", 0)
    pending = metrics.get("pending_actions", 0)
    suppressed = metrics.get("suppressed_by_exception", 0)
    if fails == 0:
        return "all_controls_passing"
    if emitted > 0 and pending == 0:
        return "actions_emitted_awaiting_verification"
    if pending > 0:
        return "pending_actions_need_emission"
    if suppressed == fails:
        return "failures_suppressed_by_exception"
    return "failures_open"


class EvidencePayload(BaseModel):
    control_id: str
    source: str = "webhook"
    payload: dict[str, Any]
    content_hash: str | None = None


@app.post("/runs")
def run_ccm(user: str = Depends(_check_auth)) -> dict:
    """Trigger a deterministic CCM run and return metrics + journey status."""
    state = run_pipeline()
    metrics = state.metrics
    return {
        "run_id": state.run_id,
        "journey_status": _journey_status(metrics),
        "metrics": metrics,
        "actions": [
            {
                "control_id": a.control_id,
                "action_type": a.action_type,
                "status": a.status,
                "reason": a.reason,
            }
            for a in state.actions
        ],
        "triggered_by": user,
    }


@app.post("/webhooks/evidence")
def ingest_evidence(
    body: EvidencePayload,
    user: str = Depends(_check_auth),
    trigger_run: bool = False,
) -> dict:
    """Event-driven ingest: accept typed evidence via webhook and optionally run the pipeline.

    Stores the payload under samples/inbound/ so it survives and can be replayed.
    """
    INBOUND_DIR.mkdir(parents=True, exist_ok=True)
    # Simple content hash if not supplied
    import hashlib
    raw = json.dumps(body.payload, sort_keys=True, default=str).encode()
    ch = body.content_hash or hashlib.sha256(raw).hexdigest()
    record = {
        "control_id": body.control_id,
        "source": body.source,
        "content_hash": ch,
        "payload": body.payload,
    }
    path = INBOUND_DIR / f"{body.control_id}_{ch[:8]}.json"
    path.write_text(json.dumps(record, indent=2))

    result: dict[str, Any] = {
        "status": "stored",
        "path": str(path),
        "control_id": body.control_id,
        "content_hash": ch,
        "ingested_by": user,
    }
    if trigger_run:
        state = run_pipeline()
        result["run"] = {
            "run_id": state.run_id,
            "journey_status": _journey_status(state.metrics),
            "metrics": state.metrics,
        }
    return result


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
