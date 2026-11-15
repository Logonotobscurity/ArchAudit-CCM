"""Adapters for live evidence collection.

Each adapter returns a typed EvidenceRecord and degrades gracefully to an offline stub when credentials are absent.
"""
from .github_branch import collect_branch_protection

__all__ = ["collect_branch_protection"]
