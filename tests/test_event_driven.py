"""Tests for event-driven collection pieces."""
from src.ccm.adapters.poll import poll_identity_mfa


def test_poll_adapter_offline_stub():
    ev = poll_identity_mfa()
    assert ev.control_id == "ACC-MFA-ADMIN"
    assert ev.source == "okta-stub"
    assert "admin_mfa" in ev.payload
    assert ev.content_hash
    assert len(ev.content_hash) == 64
