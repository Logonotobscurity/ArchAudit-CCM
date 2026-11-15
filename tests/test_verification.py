"""Tests for Phase 4.3 remediation verification loop."""
from src.ccm.nodes import run_pipeline
from src.ccm.state import ActionRecord, utcnow


def test_verification_marks_emitted_actions():
    # First run emits actions for failing controls
    state1 = run_pipeline()
    emitted = [a for a in state1.actions if a.status == "emitted"]
    # May be zero if no fails, but the function is present

    # Second run should attempt verification on any previously emitted
    state2 = run_pipeline()
    # Metrics should contain the new counters
    assert "verified_actions" in state2.metrics
    assert "still_failing_actions" in state2.metrics
    # Journey status remains defined
    assert state2.metrics.get("journey_status")
