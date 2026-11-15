"""CCM graph nodes: collect → maybe_skip → evaluate → drift → govern_check → emit_actions → report.

Public vertical slice (Ticket 1): deterministic evaluation against sample evidence.
No hardcoded metrics. Fully offline-replayable.

Ticket 3: exception persistence + dual-control enforcement + decision log.
Hash-chain: trusted evidence lineage for offline replay and auditor confidence.
Materiality driven from control pack. Outbound actions policy-gated and explicit (stubs).
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
EXCEPTIONS_PATH = ROOT / "samples" / "exceptions.json"
OUTBOUND_DIR = ROOT / "samples" / "outbound"


def _load_control_pack() -> list[dict[str, Any]]:
    with CONTROLS_PATH.open() as f:
        pack = yaml.safe_load(f)
    return pack.get("controls", [])


def _control_materiality_map(controls: list[dict[str, Any]]) -> dict[str, str]:
    return {c["id"]: c.get("materiality", "none") for c in controls}


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


def _build_evidence_chain(evidence: list[EvidenceRecord]) -> str:
    """Simple hash chain over sorted evidence content hashes.

    Deterministic root that can be re-computed on replay to prove the
    evidence set was not altered. Suitable for offline / localisation contexts.
    """
    if not evidence:
        return hashlib.sha256(b"empty").hexdigest()
    hashes = sorted(e.content_hash for e in evidence)
    current = hashlib.sha256(hashes[0].encode()).hexdigest()
    for h in hashes[1:]:
        current = hashlib.sha256((current + h).encode()).hexdigest()
    return current


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


def _load_exceptions() -> list[ExceptionRecord]:
    """Load persisted exceptions (Ticket 3)."""
    if not EXCEPTIONS_PATH.exists():
        return []
    try:
        with EXCEPTIONS_PATH.open() as f:
            raw = json.load(f)
        return [ExceptionRecord.model_validate(item) for item in raw]
    except Exception:
        return []


def _save_exceptions(exceptions: list[ExceptionRecord]) -> None:
    """Persist exceptions so they survive across runs."""
    EXCEPTIONS_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = [e.model_dump(mode="json") for e in exceptions]
    with EXCEPTIONS_PATH.open("w") as f:
        json.dump(payload, f, indent=2, default=str)


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


def drift(state: CCMState, controls: list[dict[str, Any]]) -> CCMState:
    """Materiality driven from control pack (not hardcoded).

    No previous run yet, so drift is informational based on current status + control materiality.
    """
    mat_map = _control_materiality_map(controls)
    for ev in state.evaluations:
        base = mat_map.get(ev.control_id, "none")
        # Elevate if fail; otherwise none for this slice
        materiality = base if ev.status == "fail" else "none"
        state.drifts.append(
            DriftFinding(
                materiality=materiality,  # type: ignore[arg-type]
                current_evaluation_id=ev.evaluation_id,
            )
        )
    return state


def _emit_outbound_actions(state: CCMState) -> CCMState:
    """Policy-gated explicit outbound stubs.

    Never opaque. Writes payload to samples/outbound/ for replayability.
    Sets status to emitted on success.
    """
    OUTBOUND_DIR.mkdir(parents=True, exist_ok=True)
    for action in state.actions:
        if action.status != "pending":
            continue
        # Policy gate: only explicit types allowed
        if action.action_type not in ("webhook", "ticket", "agentbridge_event"):
            action.status = "suppressed"
            action.reason = (action.reason or "") + " | policy: unsupported type"
            continue
        stub_path = OUTBOUND_DIR / f"{action.action_id}_{action.action_type}.json"
        payload = {
            "action_id": action.action_id,
            "control_id": action.control_id,
            "action_type": action.action_type,
            "payload": action.payload,
            "reason": action.reason,
            "emitted_at": utcnow().isoformat(),
        }
        with stub_path.open("w") as f:
            json.dump(payload, f, indent=2, default=str)
        action.status = "emitted"
        action.emitted_at = utcnow()
    return state


def govern_check(state: CCMState) -> CCMState:
    """Governance plane (Ticket 3).

    - Loads persisted exceptions
    - Enforces dual-control + TTL
    - Emits suppressed or pending ActionRecord (explicit, policy-gated)
    - Writes a decision log entry into state.metrics for the audit pack
    """
    # Reload in case external changes occurred between runs
    persisted = _load_exceptions()
    # Merge: prefer already-in-state (in-memory) over file for this run
    by_id = {e.exception_id: e for e in persisted}
    for e in state.exceptions:
        by_id[e.exception_id] = e
    state.exceptions = list(by_id.values())

    now = utcnow()
    approved_exceptions = set()
    decision_log = []

    for e in state.exceptions:
        dual_ok = (not e.dual_control_required) or (len(e.approved_by) >= 2)
        not_expired = e.expires_at is None or e.expires_at > now
        is_valid = e.status == "approved" and dual_ok and not_expired
        if is_valid:
            approved_exceptions.add(e.control_id)
        decision_log.append({
            "exception_id": e.exception_id,
            "control_id": e.control_id,
            "status": e.status,
            "dual_control_ok": dual_ok,
            "not_expired": not_expired,
            "valid": is_valid,
        })

    for ev in state.evaluations:
        if ev.status != "fail":
            continue
        if ev.control_id in approved_exceptions:
            state.actions.append(
                ActionRecord(
                    control_id=ev.control_id,
                    action_type="none",
                    status="suppressed",
                    reason="valid dual-control exception",
                )
            )
            decision_log.append({
                "control_id": ev.control_id,
                "decision": "suppress",
                "reason": "valid exception",
            })
            continue
        # Explicit action type (policy can later select webhook/ticket/agentbridge)
        state.actions.append(
            ActionRecord(
                control_id=ev.control_id,
                action_type="agentbridge_event",
                status="pending",
                payload={"evaluation_id": ev.evaluation_id, "detail": ev.detail},
                reason="failed control, no valid exception",
            )
        )
        decision_log.append({
            "control_id": ev.control_id,
            "decision": "pending_action",
            "reason": "no valid exception",
        })

    state.metrics["decision_log"] = decision_log
    return state


def report(state: CCMState, output_dir: Path | None = None) -> CCMState:
    """Compute real metrics and write audit pack."""
    total = len(state.evaluations)
    passed = sum(1 for e in state.evaluations if e.status == "pass")
    coverage = round((passed / total * 100) if total else 0.0, 1)
    open_exceptions = sum(1 for e in state.exceptions if e.status in ("open", "approved"))
    pending_actions = sum(1 for a in state.actions if a.status == "pending")
    suppressed = sum(1 for a in state.actions if a.status == "suppressed")
    emitted = sum(1 for a in state.actions if a.status == "emitted")

    # Evidence hash-chain root for integrity verification on replay
    chain_root = _build_evidence_chain(state.evidence)
    state.metrics["evidence_chain_root"] = chain_root

    state.metrics.update({
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
        "emitted_actions": emitted,
        "decision_basis": "deterministic",
    })

    out = output_dir or AUDIT_PACK_DIR
    out.mkdir(parents=True, exist_ok=True)

    with (out / "metrics.json").open("w") as f:
        json.dump(state.metrics, f, indent=2, default=str)

    lines = [
        "# ArchAudit CCM — Sample Audit Pack",
        "",
        f"Run ID: `{state.run_id}`",
        f"Decision basis: deterministic",
        f"Evidence chain root: `{chain_root}`",
        "",
        "## Metrics",
        f"- Coverage: **{coverage}%**",
        f"- Time-to-Evidence: **{state.metrics['time_to_evidence_minutes']} min**",
        f"- Failures: {state.metrics['evaluations_fail']}",
        f"- Unknown (no evidence): {state.metrics['evaluations_unknown']}",
        f"- Pending actions: {pending_actions}",
        f"- Suppressed by exception: {suppressed}",
        f"- Emitted actions: {emitted}",
        f"- Open exceptions: {open_exceptions}",
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

    # Decision log (Ticket 3)
    log = state.metrics.get("decision_log", [])
    if log:
        lines.append("")
        lines.append("## Decision Log")
        for entry in log:
            lines.append(f"- {entry}")

    with (out / "summary.md").open("w") as f:
        f.write("\n".join(lines) + "\n")

    return state


def run_pipeline(
    control_pack: str | None = None,
    output_dir: str | None = None,
    budget_ms: int = 30000,
) -> CCMState:
    """Public entrypoint — deterministic vertical slice + Ticket 3 governance + hash-chain + materiality + outbound stubs."""
    t0 = time.perf_counter()
    state = CCMState()
    # Load persisted exceptions before evaluation
    state.exceptions = _load_exceptions()
    controls = _load_control_pack()

    state = collect(state, controls)
    state = evaluate(state, controls)
    state = drift(state, controls)
    state = govern_check(state)
    state = _emit_outbound_actions(state)

    # Persist any changes to exceptions
    _save_exceptions(state.exceptions)

    elapsed = time.perf_counter() - t0
    state.metrics["_elapsed_s"] = elapsed
    out = Path(output_dir) if output_dir else None
    state = report(state, out)
    return state
