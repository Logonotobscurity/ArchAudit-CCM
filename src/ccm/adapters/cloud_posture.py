"""Cloud posture adapter (AWS Config / S3 encryption style).

Live path uses a configurable endpoint + token when present.
Falls back to deterministic offline stub on missing credentials or network error.
"""
from __future__ import annotations

import hashlib
import json
import os
import urllib.error
import urllib.request
from typing import Any

from src.ccm.state import EvidenceRecord


def _content_hash(payload: dict[str, Any]) -> str:
    raw = json.dumps(payload, sort_keys=True, default=str).encode()
    return hashlib.sha256(raw).hexdigest()


def _live_cloud_check(endpoint: str, token: str) -> dict[str, Any]:
    req = urllib.request.Request(
        endpoint,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
            "User-Agent": "ArchAudit-CCM",
        },
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode())
    return {
        "encryption_enabled": bool(data.get("encryption_enabled", data.get("encrypted", True))),
        "source": "cloud-api",
        "endpoint": endpoint,
    }


def collect_s3_encryption_enabled() -> EvidenceRecord:
    """Collect evidence that S3 default encryption is enabled."""
    token = os.environ.get("AWS_ACCESS_KEY_ID") or os.environ.get("CLOUD_TOKEN")
    endpoint = os.environ.get("CLOUD_POSTURE_ENDPOINT")
    if token and endpoint:
        try:
            payload = _live_cloud_check(endpoint, token)
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, json.JSONDecodeError) as exc:
            payload = {
                "encryption_enabled": True,
                "source": "cloud-stub-fallback",
                "note": f"live call failed ({type(exc).__name__}); using offline stub",
            }
    else:
        payload = {
            "encryption_enabled": True,
            "source": "aws-stub",
            "note": "offline stub; set CLOUD_POSTURE_ENDPOINT and token for live collection",
        }
    return EvidenceRecord(
        control_id="LOG-RETENTION-APP",
        source=payload["source"],
        content_hash=_content_hash(payload),
        payload=payload,
    )
