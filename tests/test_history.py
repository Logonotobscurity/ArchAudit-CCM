"""Tests for Phase 5.2 multi-run history."""
from src.ccm.history import append_run_snapshot, load_recent_snapshots, HISTORY_PATH
from src.ccm.state import EvaluationResult


def test_history_appends_and_trims():
    if HISTORY_PATH.exists():
        HISTORY_PATH.unlink()

    ev = EvaluationResult(control_id="TEST-1", status="pass", detail="ok")
    for i in range(12):
        append_run_snapshot([ev], run_id=f"run-{i}", keep=10)

    snaps = load_recent_snapshots(limit=20)
    assert len(snaps) == 10
    assert snaps[-1]["run_id"] == "run-11"
    assert snaps[0]["run_id"] == "run-2"
