"""Governance plane tests (Ticket 3)."""
from datetime import datetime, timedelta, timezone

from src.ccm.nodes import run_pipeline
from src.ccm.state import ExceptionRecord


def test_pending_action_without_exception():
    state = run_pipeline()
    actions = {a.control_id: a for a in state.actions}
    assert actions["CHG-TICKET-PROD"].status == "pending"
    assert any(e.get("decision") == "pending_action" for e in state.metrics.get("decision_log", []))


def test_valid_exception_suppresses_action(tmp_path, monkeypatch):
    """A dual-control approved exception suppresses the action."""
    # Create a temporary exceptions file by injecting into state after load
    # (full file isolation would require more mocking; this exercises the logic)
    state = run_pipeline()

    # Manually add a valid exception and re-run governance conceptually
    from src.ccm.nodes import govern_check
    now = datetime.now(timezone.utc)
    exc = ExceptionRecord(
        control_id="CHG-TICKET-PROD",
        reason="temporary waiver",
        owner="security-lead",
        status="approved",
        dual_control_required=True,
        approved_by=["alice", "bob"],
        expires_at=now + timedelta(days=7),
    )
    state.exceptions = [exc]
    state.actions = []  # clear previous
    state = govern_check(state)

    actions = {a.control_id: a for a in state.actions}
    assert actions["CHG-TICKET-PROD"].status == "suppressed"
    assert actions["CHG-TICKET-PROD"].reason == "valid dual-control exception"
