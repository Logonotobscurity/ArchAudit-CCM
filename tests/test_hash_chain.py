"""Evidence hash-chain integrity tests."""
from src.ccm.nodes import run_pipeline


def test_chain_root_present_and_stable():
    s1 = run_pipeline()
    s2 = run_pipeline()

    assert "evidence_chain_root" in s1.metrics
    assert len(s1.metrics["evidence_chain_root"]) == 64  # sha256 hex
    # Same evidence set → same root
    assert s1.metrics["evidence_chain_root"] == s2.metrics["evidence_chain_root"]
