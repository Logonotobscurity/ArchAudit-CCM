"""Adapters for live evidence collection.

Each adapter returns a typed EvidenceRecord and degrades gracefully to an offline stub when credentials are absent.
"""
from .github_branch import collect_branch_protection
from .poll import poll_identity_mfa

__all__ = ["collect_branch_protection", "poll_identity_mfa"]
