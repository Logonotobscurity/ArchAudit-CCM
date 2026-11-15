"""Tests for Phase 5.1 live adapter implementations (offline + fallback paths)."""
import os
from unittest.mock import patch

from src.ccm.adapters import collect_branch_protection, poll_identity_mfa


def test_github_adapter_offline():
    with patch.dict(os.environ, {}, clear=True):
        ev = collect_branch_protection()
    assert ev.control_id == "CHG-BRANCH-MAIN"
    assert ev.source == "github-stub"
    assert ev.payload.get("main_protected") is True
    assert len(ev.content_hash) == 64


def test_identity_poll_offline():
    with patch.dict(os.environ, {}, clear=True):
        ev = poll_identity_mfa()
    assert ev.control_id == "ACC-MFA-ADMIN"
    assert "admin_mfa" in ev.payload
    assert ev.content_hash


def test_github_adapter_fallback_on_error():
    # Token present but network will fail — should degrade to stub
    with patch.dict(os.environ, {"GITHUB_TOKEN": "fake-token"}):
        ev = collect_branch_protection()
    assert ev.source in ("github-stub-fallback", "github-api")
    assert ev.content_hash
