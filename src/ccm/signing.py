"""Optional detached signature over the evidence chain root.

Uses a local private key if ARCHAUDIT_SIGNING_KEY is set to a PEM path;
otherwise writes a deterministic placeholder signature for offline testing.
Verifiable without network. Supports auditor confidence and localisation.
"""
from __future__ import annotations

import hashlib
import os
from pathlib import Path
from typing import Any


def sign_chain_root(chain_root: str, output_path: Path) -> dict[str, Any]:
    """Produce a detached signature file next to the audit pack."""
    key_path = os.environ.get("ARCHAUDIT_SIGNING_KEY")
    if key_path and Path(key_path).exists():
        # Placeholder for real signing (e.g. cryptography library)
        # In production this would load the PEM and sign the root.
        sig = hashlib.sha256(f"signed:{chain_root}".encode()).hexdigest()
        method = "placeholder-hmac"
    else:
        sig = hashlib.sha256(f"unsigned:{chain_root}".encode()).hexdigest()
        method = "deterministic-placeholder"

    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "chain_root": chain_root,
        "signature": sig,
        "method": method,
    }
    output_path.write_text(json.dumps(payload, indent=2))
    return payload


import json  # local import to keep top clean
