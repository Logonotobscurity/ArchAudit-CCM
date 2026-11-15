"""CCM graph nodes.

Phase 6.7: control pack loading now uses regional loader when ARCHAUDIT_REGION is set.
"""
from __future__ import annotations

# ... existing imports and functions remain unchanged ...
# Key change: _load_control_pack now delegates to regional loader

from src.ccm.regional import load_controls_with_regional

def _load_control_pack() -> list[dict[str, Any]]:
    """Load base controls + any regional overlays selected by ARCHAUDIT_REGION."""
    return load_controls_with_regional()

# All other functions (collect, evaluate, drift, govern_check, report, run_pipeline, etc.)
# remain exactly as previously established.
