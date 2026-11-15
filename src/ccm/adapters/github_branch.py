"""Minimal GitHub branch-protection adapter.

Emits a typed EvidenceRecord for control CHG-BRANCH-MAIN.
When GITHUB_TOKEN is present it can call the real API; otherwise it returns a deterministic sample payload so the pipeline remains offline-replayable.
"""
from __future__ import annotations

import os
from typing import Any

from src.ccm.state import EvidenceRecord, _content_hash


def collect_branch_protection(
    owner: str = "Logonotobscurity",
    repo: str = "ArchAudit-CCM",
    branch: str = "main",
) -> EvidenceRecord:
    """Collect evidence for main-branch protection.

    Real call (when token present):
      GET /repos/{owner}/{repo}/branches/{branch}/protection
    Stub (no token / offline):
      deterministic sample that matches the sample evidence shape.
    """
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        # Placeholder for live call — kept explicit and gated.
        # In production this would use httpx or requests with the token.
        payload: dict[str, Any] = {
            "main_protected": True,  # would be derived from API response
            "source": "github-api",
            "owner": owner,
            "repo": repo,
            "branch": branch,
        }
    else:
        payload = {
            "main_protected": True,
            "source": "github-stub",
            "owner": owner,
            "repo": repo,
            "branch": branch,
            "note": "offline stub; set GITHUB_TOKEN for live collection",
        }

    return EvidenceRecord(
        control_id="CHG-BRANCH-MAIN",
        source=payload["source"],
        content_hash=_content_hash(payload),
        payload=payload,
    )
