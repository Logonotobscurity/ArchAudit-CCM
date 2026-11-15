"""Optional detached signature over the evidence chain root.

Uses a local private key if ARCHAUDIT_SIGNING_KEY is set to a PEM path.
Falls back to a deterministic placeholder when no key or library is available.
Verifiable offline.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any


def sign_chain_root(chain_root: str, output_path: Path) -> dict[str, Any]:
    """Produce a detached signature file next to the audit pack."""
    key_path = os.environ.get("ARCHAUDIT_SIGNING_KEY")
    method = "deterministic-placeholder"
    sig = hashlib.sha256(f"unsigned:{chain_root}".encode()).hexdigest()

    if key_path and Path(key_path).exists():
        try:
            # Optional real signing when cryptography is installed
            from cryptography.hazmat.primitives import serialization
            from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

            pem = Path(key_path).read_bytes()
            key = serialization.load_pem_private_key(pem, password=None)
            if isinstance(key, Ed25519PrivateKey):
                sig_bytes = key.sign(chain_root.encode())
                sig = sig_bytes.hex()
                method = "ed25519"
        except Exception:
            # Fall through to placeholder
            sig = hashlib.sha256(f"signed-placeholder:{chain_root}".encode()).hexdigest()
            method = "placeholder-hmac"

    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "chain_root": chain_root,
        "signature": sig,
        "method": method,
    }
    output_path.write_text(json.dumps(payload, indent=2))
    return payload
