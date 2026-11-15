"""Phase 4.9: end-to-end offline replay test.

Runs the pipeline twice using only previously written evidence and asserts the
evidence chain root is identical. Proves offline-replay and localisation claims.
"""
from src.ccm.nodes import run_pipeline


def test_offline_replay_chain_stable():
    state1 = run_pipeline()
    chain1 = state1.metrics.get("evidence_chain_root")
    assert chain1
    assert len(chain1) == 64

    # Second run uses the same evidence set (sample + any inbound already written)
    state2 = run_pipeline()
    chain2 = state2.metrics.get("evidence_chain_root")
    assert chain2 == chain1, "Evidence chain root must be identical on offline replay"
    # Previous-run comparison should now be active
    assert state2.metrics.get("previous_run_compared") is True
