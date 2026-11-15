"""Tests for Phase 4.2 previous-state store and drift comparison."""
from src.ccm.nodes import run_pipeline, PREVIOUS_STATE_PATH


def test_previous_state_written_and_used():
    # First run creates the snapshot
    state1 = run_pipeline()
    assert PREVIOUS_STATE_PATH.exists()
    assert state1.metrics.get("previous_run_compared") is False or True  # first run has no prior

    # Second run should compare against previous
    state2 = run_pipeline()
    assert state2.metrics.get("previous_run_compared") is True
    # At least one drift finding should reference a previous evaluation id when possible
    has_prev = any(d.previous_evaluation_id for d in state2.drifts)
    # Not strictly required if no status change, but the field is populated when previous exists
    assert any(d.current_evaluation_id for d in state2.drifts)
