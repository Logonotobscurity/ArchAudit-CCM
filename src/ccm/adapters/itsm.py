"""ITSM / ticketing adapter.

Emits an ActionRecord-compatible payload and, when configured, creates a real ticket.
Offline path returns a deterministic stub ticket ID so the pipeline stays replayable.
"""
from __future__ import annotations

import hashlib
import json
import os
import urllib.error
import urllib.request
from typing import Any


def _stub_ticket_id(control_id: str) -> str:
    return "TICKET-" + hashlib.sha256(control_id.encode()).hexdigest()[:8].upper()


def create_ticket(control_id: str, detail: str, action_id: str) -> dict[str, Any]:
    """Create a ticket in the configured ITSM or return a deterministic stub."""
    endpoint = os.environ.get("ITSM_ENDPOINT")
    token = os.environ.get("ITSM_TOKEN")
    if endpoint and token:
        try:
            body = json.dumps({
                "summary": f"CCM failure: {control_id}",
                "description": detail,
                "external_id": action_id,
            }).encode()
            req = urllib.request.Request(
                endpoint,
                data=body,
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json",
                    "User-Agent": "ArchAudit-CCM",
                },
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode())
            return {
                "ticket_id": data.get("id") or data.get("key") or _stub_ticket_id(control_id),
                "source": "itsm-api",
                "status": "created",
            }
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, json.JSONDecodeError):
            pass
    # Offline / fallback
    return {
        "ticket_id": _stub_ticket_id(control_id),
        "source": "itsm-stub",
        "status": "stub",
    }
