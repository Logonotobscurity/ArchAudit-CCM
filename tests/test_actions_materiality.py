"""Tests for materiality from control pack and outbound action stubs."""
from src.ccm.nodes import run_pipeline


def test_materiality_driven_from_control_pack():
    state = run_pipeline()
    # CHG-TICKET-PROD fails and has materiality: urgent in controls.yaml
    drifts = {d.current_evaluation_id: d for d in state.drifts}
    fail_evals = [e for e in state.evaluations if e.status == "fail"]
    assert fail_evals, "expected at least one failure"
    for ev in fail_evals:
        d = next((d for d in state.drifts if d.current_evaluation_id == ev.evaluation_id), None)
        assert d is not None
        # materiality should not be none for failing controls that have a pack value
        if ev.control_id == "CHG-TICKET-PROD":
            assert d.materiality == "urgent"


def test_outbound_actions_emitted():
    state = run_pipeline()
    emitted = [a for a in state.actions if a.status == "emitted"]
    # At least the known failure should produce an emitted agentbridge_event
    assert any(a.action_type == "agentbridge_event" and a.status == "emitted" for a in state.actions)
    assert state.metrics.get("emitted_actions", 0) >= 1
