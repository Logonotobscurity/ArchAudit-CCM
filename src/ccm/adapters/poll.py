"""Identity MFA poll adapter.

Live path uses IDENTITY_TOKEN + IDENTITY_ENDPOINT (optional).
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


def _live_identity_poll(endpoint: str, token: str) -> dict[str, Any]:
    """Minimal live poll. Expects JSON with admin_mfa / operator_mfa keys."""
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
        "admin_mfa": bool(data.get("admin_mfa", data.get("mfa_enabled", True))),
        "operator_mfa": bool(data.get("operator_mfa", True)),
        "source": "identity-api",
        "endpoint": endpoint,
    }


def poll_identity_mfa(source: str = "okta-stub") -> EvidenceRecord:
    """Poll-style collection for an identity MFA control."""
    token = os.environ.get("IDENTITY_TOKEN")
    endpoint = os.environ.get("IDENTITY_ENDPOINT")
    if token and endpoint:
        try:
            payload = _live_identity_poll(endpoint, token)
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, json.JSONDecodeError) as exc:
            payload = {
                "admin_mfa": True,
                "operator_mfa": False,
                "source": "identity-stub-fallback",
                "note": f"live poll failed ({type(exc).__name__}); using offline stub",
            }
    elif token:
        # Token present but no endpoint — still treat as live-intent stub
        payload = {
            "admin_mfa": True,
            "operator_mfa": True,
            "source": "identity-api-intent",
            "note": "token present; set IDENTITY_ENDPOINT for live poll",
        }
    else:
        payload = {
            "admin_mfa": True,
            "operator_mfa": False,
            "source": source,
            "note": "offline stub; set IDENTITY_TOKEN and IDENTITY_ENDPOINT for live poll",
        }
    return EvidenceRecord(
        control_id="ACC-MFA-ADMIN",
        source=payload["source"],
        content_hash=_content_hash(payload),
        payload=payload,
    )
