"""Thin FastAPI surface so other systems can trigger CCM runs.

Basic auth stub (replace with real auth in production).
Offline-replayable: returns the same audit pack metrics.
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


@app.post("/runs")
def run_ccm(user: str = Depends(_check_auth)) -> dict:
    """Trigger a deterministic CCM run and return metrics + action summary."""
    state = run_pipeline()
    return {
        "run_id": state.run_id,
        "metrics": state.metrics,
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
