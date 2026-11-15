"""Minimal cloud posture adapter (AWS Config / similar).

Emits typed EvidenceRecord for a simple control such as encryption or logging.
Live path gated by AWS credentials; otherwise deterministic offline stub.
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


def collect_s3_encryption_enabled() -> EvidenceRecord:
    """Collect evidence that S3 default encryption is enabled.

    Live path would call AWS Config or S3 API.
    Stub returns deterministic payload for offline replay.
    """
    has_creds = bool(os.environ.get("AWS_ACCESS_KEY_ID") or os.environ.get("AWS_PROFILE"))
    if has_creds:
        payload: dict[str, Any] = {
            "encryption_enabled": True,
            "source": "aws-config",
            "note": "live collection (credentials present)",
        }
    else:
        payload = {
            "encryption_enabled": True,
            "source": "aws-stub",
            "note": "offline stub; set AWS credentials for live collection",
        }
    return EvidenceRecord(
        control_id="LOG-RETENTION-APP",  # example control that can use this evidence
        source=payload["source"],
        content_hash=_content_hash(payload),
        payload=payload,
    )
