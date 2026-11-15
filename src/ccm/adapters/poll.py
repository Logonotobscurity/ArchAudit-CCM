"""Minimal poll adapter stub.

Demonstrates the pull side of event-driven collection.
In production this would poll an identity provider, cloud API, or webhook log
and emit typed EvidenceRecords. Offline-safe: returns deterministic sample
payload when no live credentials are present.
"""
from __future__ import annotations

import hashlib
import json
import os
from typing import Any

from src.ccm.state import EvidenceRecord


def _content_hash(payload: dict[str, Any]) -> str:
    raw = json.dumps(payload, sort_keys=True, default=str).encode()
    return hashlib.sha256(raw).hexdigest()


def poll_identity_mfa(source: str = "okta-stub") -> EvidenceRecord:
    """Poll-style collection for an identity MFA control.

    Live path would call the identity provider API.
    Stub returns a deterministic payload so the pipeline stays offline-replayable.
    """
    token = os.environ.get("IDENTITY_TOKEN")
    if token:
        payload: dict[str, Any] = {
            "admin_mfa": True,
            "operator_mfa": True,
            "source": "identity-api",
            "note": "live poll (token present)",
        }
    else:
        payload = {
            "admin_mfa": True,
            "operator_mfa": False,
            "source": source,
            "note": "offline stub; set IDENTITY_TOKEN for live poll",
        }
    return EvidenceRecord(
        control_id="ACC-MFA-ADMIN",
        source=payload["source"],
        content_hash=_content_hash(payload),
        payload=payload,
    )
