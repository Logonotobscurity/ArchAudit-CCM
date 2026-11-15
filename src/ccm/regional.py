"""Regional pack loader.

Loads base controls plus any regional overlays selected by ARCHAUDIT_REGION
(comma-separated jurisdiction codes, e.g. NG,ZA).
Pure data merge; no hard-coded regional logic.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
BASE_CONTROLS = ROOT / "policies" / "controls.yaml"
REGIONAL_DIR = ROOT / "policies" / "regional"


def load_controls_with_regional() -> list[dict[str, Any]]:
    """Return base controls merged with selected regional overlays."""
    with BASE_CONTROLS.open() as f:
        base = yaml.safe_load(f).get("controls", [])

    regions = os.environ.get("ARCHAUDIT_REGION", "")
    if not regions:
        return base

    codes = [c.strip().upper() for c in regions.split(",") if c.strip()]
    merged = list(base)
    for code in codes:
        path = REGIONAL_DIR / f"{code.lower()}.yaml"
        if not path.exists():
            continue
        with path.open() as f:
            overlay = yaml.safe_load(f).get("controls", [])
        # Regional controls are appended; IDs are namespaced by convention
        merged.extend(overlay)
    return merged
