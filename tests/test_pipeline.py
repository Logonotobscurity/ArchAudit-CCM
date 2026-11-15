"""Basic pipeline tests for the public vertical slice.

Covers:
- At least one known pass
- At least one known fail
- Pending action generated for the failure
- Metrics derived from evaluation results (not hardcoded)
"""
from src.ccm.nodes import run_pipeline


def test_known_pass_and_fail():
    state = run_pipeline()
    by_id = {e.control_id: e for e in state.evaluations}

    # Known pass (sample evidence has admin_mfa: true)
    assert "ACC-MFA-ADMIN" in by_id
    assert by_id["ACC-MFA-ADMIN"].status == "pass"
    assert by_id["ACC-MFA-ADMIN"].decision_basis == "deterministic"

    # Known fail (sample evidence has prod_change_has_ticket: false)
    assert "CHG-TICKET-PROD" in by_id
    assert by_id["CHG-TICKET-PROD"].status == "fail"
    assert by_id["CHG-TICKET-PROD"].decision_basis == "deterministic"


def test_pending_action_on_failure():
    state = run_pipeline()
    actions_by_control = {a.control_id: a for a in state.actions}

    assert "CHG-TICKET-PROD" in actions_by_control
    action = actions_by_control["CHG-TICKET-PROD"]
    assert action.status == "pending"
    assert action.action_type == "agentbridge_event"


def test_metrics_are_derived():
    state = run_pipeline()

    total = len(state.evaluations)
    passed = sum(1 for e in state.evaluations if e.status == "pass")
    expected_coverage = round((passed / total * 100) if total else 0.0, 1)

    assert state.metrics["evaluations_total"] == total
    assert state.metrics["evaluations_pass"] == passed
    assert state.metrics["control_coverage_pct"] == expected_coverage
    assert state.metrics["evaluations_fail"] >= 1
    assert state.metrics["pending_actions"] >= 1
    assert state.metrics["decision_basis"] == "deterministic"
