"""CCM shared state and evidence schemas (Pydantic v2) — ADR-001 v3.1 contracts.

Aligned with ISO 42001 evidence and governance expectations:
- typed Evidence with content_hash supports continuous, provenance-backed proof
- EvaluationResult.decision_basis records deterministic vs assisted vs manual
- ExceptionRecord + ActionRecord enable explicit human oversight and corrective action
Phase 4.3: ActionRecord status now includes verification outcomes.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Literal
from uuid import uuid4

from pydantic import BaseModel, Field


def _ulid() -> str:
    return uuid4().hex


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class EvidenceRecord(BaseModel):
    evidence_id: str = Field(default_factory=_ulid)
    control_id: str
    source: str
    collected_at: datetime = Field(default_factory=utcnow)
    content_hash: str
    payload: dict[str, Any] = Field(default_factory=dict)


class EvaluationResult(BaseModel):
    evaluation_id: str = Field(default_factory=_ulid)
    control_id: str
    status: Literal["pass", "fail", "unknown", "not_applicable"]
    decision_basis: Literal["deterministic", "assisted", "manual"] = "deterministic"
    evidence_ids: list[str] = Field(default_factory=list)
    rule: str | None = None
    detail: str | None = None


class DriftFinding(BaseModel):
    materiality: Literal["none", "informational", "material", "urgent"] = "none"
    previous_evaluation_id: str | None = None
    current_evaluation_id: str | None = None


class ExceptionRecord(BaseModel):
    """Policy-gated exception (ISO 42001 human oversight / risk treatment)."""
    exception_id: str = Field(default_factory=_ulid)
    control_id: str
    reason: str
    owner: str
    ttl_hours: int = 168  # default 7 days
    dual_control_required: bool = True
    approved_by: list[str] = Field(default_factory=list)
    status: Literal["open", "approved", "expired", "revoked"] = "open"
    created_at: datetime = Field(default_factory=utcnow)
    expires_at: datetime | None = None


class ActionRecord(BaseModel):
    """Outbound action from the governance plane (explicit, not agent-opaque).

    Status progression: pending → emitted → (verified | still_failing | expired)
    """
    action_id: str = Field(default_factory=_ulid)
    control_id: str
    action_type: Literal["webhook", "ticket", "agentbridge_event", "none"] = "none"
    payload: dict[str, Any] = Field(default_factory=dict)
    status: Literal["pending", "emitted", "failed", "suppressed", "verified", "still_failing"] = "pending"
    emitted_at: datetime | None = None
    verified_at: datetime | None = None
    reason: str | None = None


class CCMState(BaseModel):
    run_id: str = Field(default_factory=_ulid)
    evidence: list[EvidenceRecord] = Field(default_factory=list)
    evaluations: list[EvaluationResult] = Field(default_factory=list)
    drifts: list[DriftFinding] = Field(default_factory=list)
    exceptions: list[ExceptionRecord] = Field(default_factory=list)
    actions: list[ActionRecord] = Field(default_factory=list)
    metrics: dict[str, Any] = Field(default_factory=dict)
