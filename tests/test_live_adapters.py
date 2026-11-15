"""Tests for Phase 4.4 live adapter stubs."""
from src.ccm.adapters import (
    collect_branch_protection,
    poll_identity_mfa,
    collect_s3_encryption_enabled,
)


def test_github_adapter_offline():
    ev = collect_branch_protection()
    assert ev.control_id == "CHG-BRANCH-MAIN"
    assert ev.source == "github-stub"
    assert ev.payload.get("main_protected") is True
    assert len(ev.content_hash) == 64


def test_identity_poll_offline():
    ev = poll_identity_mfa()
    assert ev.control_id == "ACC-MFA-ADMIN"
    assert "admin_mfa" in ev.payload
    assert ev.content_hash


def test_cloud_posture_offline():
    ev = collect_s3_encryption_enabled()
    assert ev.source == "aws-stub"
    assert ev.payload.get("encryption_enabled") is True
    assert ev.content_hash
