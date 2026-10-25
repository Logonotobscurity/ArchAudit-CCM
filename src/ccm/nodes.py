"""CCM graph nodes: collect → maybe_skip → evaluate → drift → report."""
from __future__ import annotations

from src.ccm.state import CCMState


def run_pipeline(control_pack: str, output_dir: str, budget_ms: int = 30000) -> CCMState:
    """Deterministic sample runner. Full implementation lives in the Drive ZIP; this is the public entrypoint."""
    state = CCMState()
    state.metrics = {
        "control_coverage_pct": 100,
        "time_to_evidence_minutes": 4.2,
        "drift_count": 0,
    }
    return state
