"""Tests for Phase 4.1 inbound evidence processing."""
import json
from pathlib import Path

from src.ccm.nodes import run_pipeline, INBOUND_DIR, EVIDENCE_DIR


def test_inbound_evidence_merged():
    # Write a temporary inbound file that should override or supplement sample
    INBOUND_DIR.mkdir(parents=True, exist_ok=True)
    test_payload = {
        "control_id": "ACC-MFA-ADMIN",
        "source": "webhook-test",
        "content_hash": "deadbeef1234567890abcdef",
        "payload": {"admin_mfa": False, "operator_mfa": True},
    }
    test_path = INBOUND_DIR / "test_ACC-MFA-ADMIN.json"
    test_path.write_text(json.dumps(test_payload))

    try:
        state = run_pipeline()
        # Should have evidence for the control
        mfa_ev = next((e for e in state.evidence if e.control_id == "ACC-MFA-ADMIN"), None)
        assert mfa_ev is not None
        # Source should prefer inbound when present
        assert mfa_ev.source == "webhook-test"
        assert mfa_ev.payload.get("admin_mfa") is False
        assert state.metrics.get("inbound_evidence_count", 0) >= 1
    finally:
        if test_path.exists():
            test_path.unlink()
