"""Test the GitHub branch-protection adapter stub."""
from src.ccm.adapters.github_branch import collect_branch_protection


def test_github_branch_adapter_offline_stub():
    ev = collect_branch_protection()
    assert ev.control_id == "CHG-BRANCH-MAIN"
    assert ev.source == "github-stub"
    assert ev.payload.get("main_protected") is True
    assert ev.content_hash
    assert len(ev.content_hash) == 64
