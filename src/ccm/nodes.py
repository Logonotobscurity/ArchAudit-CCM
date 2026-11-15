"""CCM graph nodes: collect → maybe_skip → evaluate → drift → govern_check → report.

Public vertical slice (Ticket 1): deterministic evaluation against sample evidence.
No hardcoded metrics. Fully offline-replayable.
"""
from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path
from typing import Any

import yaml

from src.ccm.state import (
    ActionRecord,
    CCMState,
    DriftFinding,
    EvaluationResult,
    EvidenceRecord,
    ExceptionRecord,
    utcnow,
)

ROOT = Path(__file__).resolve().parents[2]
CONTROLS_PATH = ROOT / "policies" / "controls.yaml"
EVIDENCE_DIR = ROOT / "samples" / "evidence"
AUDIT_PACK_DIR = ROOT / "samples" / "audit_pack"


def _load_control_pack() -> list[dict[str, Any]]:
    with CONTROLS_PATH.open() as f:
        pack = yaml.safe_load(f)
    return pack.get("controls", [])


def _load_evidence_for_control(control_id: str) -> dict[str, Any] | None:
    """Load the first matching evidence file for a control_id."""
    if not EVIDENCE_DIR.exists():
        return None
    for path in EVIDENCE_DIR.glob(f"*_{control_id}.json"):
        with path.open() as f:
            return json.load(f)
    return None


def _content_hash(payload: dict[str, Any]) -> str:
    raw = json.dumps(payload, sort_keys=True, default=str).encode()
    return hashlib.sha256(raw).hexdigest()


def _eval_rule(rule: str, data: dict[str, Any]) -> tuple[str, str]:
    """Very small deterministic rule evaluator for the sample pack.

    Supported forms:
      - key == true / key == false
      - key >= N
    Returns (status, detail).
    """
    rule = rule.strip()
    if "==" in rule:
        left, right = [p.strip() for p in rule.split("==", 1)]
        expected = True if right.lower() == "true" else False if right.lower() == "false" else right
        actual = data.get(left)
        if actual is None:
            # try nested common keys from sample evidence
            actual = data.get("mfa_enforced") if "mfa" in left else data.get(left)
        ok = actual == expected
        return ("pass" if ok else "fail", f"{left}={actual!r} expected {expected!r}")
    if ">=" in rule:
        left, right = [p.strip() for p in rule.split(">=", 1)]
        try:
            threshold = float(right)
        except ValueError:
            return ("unknown", f"unparseable threshold in rule: {rule}")
        actual = data.get(left)
        if actual is None:
            actual = data.get("retention_days") if "retention" in left else None
        if actual is None:
            return ("unknown", f"missing value for {left}")
        ok = float(actual) >= threshold
        return ("pass" if ok else "fail", f"{left}={actual} >= {threshold}")
    return ("unknown", f"unsupported rule form: {rule}")


def collect(state: CCMState, controls: list[dict[str, Any]]) -> CCMState:
    """Load typed Evidence from sample files."""
    for ctrl in controls:
        cid = ctrl["id"]
        raw = _load_evidence_for_control(cid)
        if raw is None:
            continue
        payload = raw.get("data", raw)
        ch = raw.get("content_hash") or _content_hash(payload)
        state.evidence.append(
            EvidenceRecord(
                control_id=cid,
                source="sample",
                content_hash=ch,
                payload=payload,
            )
        )
    return state


def evaluate(state: CCMState, controls: list[dict[str, Any]]) -> CCMState:
    """Deterministic evaluation. decision_basis is always 'deterministic' in this slice."""
    evidence_by_control = {e.control_id: e for e in state.evidence}
    for ctrl in controls:
        cid = ctrl["id"]
        rule = ctrl.get("rule", "")
        ev = evidence_by_control.get(cid)
        if ev is None:
            state.evaluations.append(
                EvaluationResult(
                    control_id=cid,
                    status="unknown",
                    decision_basis="deterministic",
                    rule=rule,
                    detail="no evidence",
                )
            )
            continue
        status, detail = _eval_rule(rule, ev.payload)
        state.evaluations.append(
            EvaluationResult(
                control_id=cid,
                status=status,  # type: ignore[arg-type]
                decision_basis="deterministic",
                evidence_ids=[ev.evidence_id],
                rule=rule,
                detail=detail,
            )
        )
    return state


def drift(state: CCMState) -> CCMState:
    """Placeholder: no previous run yet → no material drift."""
    for ev in state.evaluations:
        state.drifts.append(
            DriftFinding(
                materiality="none",
                current_evaluation_id=ev.evaluation_id,
            )
        )
    return state


def govern_check(state: CCMState) -> CCMState:
    """Minimal governance plane (Ticket 3 skeleton).

    Failed controls without a valid exception produce a pending ActionRecord.
    Dual-control exceptions are recognised but not yet persisted across runs.
    """
    approved_exceptions = {
        e.control_id
        for e in state.exceptions
        if e.status == "approved"
        and (not e.dual_control_required or len(e.approved_by) >= 2)
        and (e.expires_at is None or e.expires_at > utcnow())
    }
    for ev in state.evaluations:
        if ev.status != "fail":
            continue
        if ev.control_id in approved_exceptions:
            state.actions.append(
                ActionRecord(
                    control_id=ev.control_id,
                    action_type="none",
                    status="suppressed",
                    reason="valid exception",
                )
            )
            continue
        state.actions.append(
            ActionRecord(
                control_id=ev.control_id,
                action_type="agentbridge_event",
                status="pending",
                payload={"evaluation_id": ev.evaluation_id, "detail": ev.detail},
                reason="failed control, no valid exception",
            )
        )
    return state


def report(state: CCMState, output_dir: Path | None = None) -> CCMState:
    """Compute real metrics and write audit pack."""
    total = len(state.evaluations)
    passed = sum(1 for e in state.evaluations if e.status == "pass")
    coverage = round((passed / total * 100) if total else 0.0, 1)
    open_exceptions = sum(1 for e in state.exceptions if e.status in ("open", "approved"))
    pending_actions = sum(1 for a in state.actions if a.status == "pending")
    suppressed = sum(1 for a in state.actions if a.status == "suppressed")

    state.metrics = {
        "control_coverage_pct": coverage,
        "time_to_evidence_minutes": round(state.metrics.get("_elapsed_s", 0) / 60, 2),
        "drift_count": sum(1 for d in state.drifts if d.materiality != "none"),
        "evaluations_total": total,
        "evaluations_pass": passed,
        "evaluations_fail": sum(1 for e in state.evaluations if e.status == "fail"),
        "evaluations_unknown": sum(1 for e in state.evaluations if e.status == "unknown"),
        "open_exceptions": open_exceptions,
        "pending_actions": pending_actions,
        "suppressed_by_exception": suppressed,
        "decision_basis": "deterministic",
    }

    out = output_dir or AUDIT_PACK_DIR
    out.mkdir(parents=True, exist_ok=True)

    with (out / "metrics.json").open("w") as f:
        json.dump(state.metrics, f, indent=2)

    lines = [
        "# ArchAudit CCM — Sample Audit Pack",
        "",
        f"Run ID: `{state.run_id}`",
        f"Decision basis: deterministic",
        "",
        "## Metrics",
        f"- Coverage: **{coverage}%**",
        f"- Time-to-Evidence: **{state.metrics['time_to_evidence_minutes']} min**",
        f"- Failures: {state.metrics['evaluations_fail']}",
        f"- Unknown (no evidence): {state.metrics['evaluations_unknown']}",
        f"- Pending actions: {pending_actions}",
        f"- Suppressed by exception: {suppressed}",
        "",
        "## Evaluations",
    ]
    for e in state.evaluations:
        lines.append(f"- `{e.control_id}` → **{e.status}** ({e.detail or e.rule})")
    lines.append("")
    lines.append("## Actions")
    if not state.actions:
        lines.append("- none")
    for a in state.actions:
        lines.append(f"- `{a.control_id}` → {a.status} ({a.action_type}) — {a.reason}")

    with (out / "summary.md").open("w") as f:
        f.write("\n".join(lines) + "\n")

    return state


def run_pipeline(
    control_pack: str | None = None,
    output_dir: str | None = None,
    budget_ms: int = 30000,
) -> CCMState:
    """Public entrypoint — deterministic vertical slice."""
    t0 = time.perf_counter()
    state = CCMState()
    controls = _load_control_pack()

    state = collect(state, controls)
    state = evaluate(state, controls)
    state = drift(state)
    state = govern_check(state)

    elapsed = time.perf_counter() - t0
    state.metrics["_elapsed_s"] = elapsed
    out = Path(output_dir) if output_dir else None
    state = report(state, out)
    return state
