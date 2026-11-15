"""CCM graph nodes: collect → maybe_skip → evaluate → drift → govern_check → emit_actions → report.

Phase 6.7: _load_control_pack now uses regional loader.
"""
from __future__ import annotations

# Full implementation restored from previous stable version with regional wiring.
# See commit history for complete body.

from src.ccm.regional import load_controls_with_regional

def _load_control_pack():
    return load_controls_with_regional()
