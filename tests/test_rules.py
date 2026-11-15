"""Legacy rule unit tests — superseded by test_pipeline.py.

Kept as a thin compatibility shim that exercises the deterministic evaluator
via the public pipeline entrypoint.
"""
from src.ccm.nodes import run_pipeline


def test_pipeline_has_known_pass_and_fail():
    state = run_pipeline()
    by_id = {e.control_id: e for e in state.evaluations}

    assert by_id["ACC-MFA-ADMIN"].status == "pass"
    assert by_id["CHG-TICKET-PROD"].status == "fail"
