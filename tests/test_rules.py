"""Rule unit tests."""
from src.ccm.rules import apply_rule


def test_mfa_admin_pass():
    assert apply_rule("ACC-MFA-ADMIN", {"admin_mfa": True})["status"] == "pass"


def test_mfa_admin_fail():
    assert apply_rule("ACC-MFA-ADMIN", {"admin_mfa": False})["status"] == "fail"
