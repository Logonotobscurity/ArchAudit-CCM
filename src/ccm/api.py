"""Thin FastAPI surface so other systems can trigger CCM runs.

Basic auth stub (replace with real auth in production).
Offline-replayable: returns the same audit pack metrics plus journey status.
"""
from __future__ import annotations

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from src.ccm.nodes import run_pipeline

app = FastAPI(title="ArchAudit CCM", version="0.1.0")
security = HTTPBasic()

# Stub credentials — replace with proper secret management
_VALID_USER = "ccm"
_VALID_PASS = "changeme"


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


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
