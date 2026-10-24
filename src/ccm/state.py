"""CCM shared state and evidence schemas (Pydantic v2) — ADR-001 v3 contracts."""
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


class DriftFinding(BaseModel):
    materiality: Literal["none", "informational", "material", "urgent"] = "none"
    previous_evaluation_id: str | None = None
    current_evaluation_id: str | None = None


class CCMState(BaseModel):
    run_id: str = Field(default_factory=_ulid)
    evidence: list[EvidenceRecord] = Field(default_factory=list)
    evaluations: list[EvaluationResult] = Field(default_factory=list)
    drifts: list[DriftFinding] = Field(default_factory=list)
    metrics: dict[str, Any] = Field(default_factory=dict)
