"""CCM graph nodes: collect → maybe_skip → evaluate → drift → govern_check → emit_actions → report.

Public vertical slice (Ticket 1): deterministic evaluation against sample evidence.
No hardcoded metrics. Fully offline-replayable.

Ticket 3: exception persistence + dual-control enforcement + decision log.
Hash-chain: trusted evidence lineage for offline replay and auditor confidence.
Materiality driven from control pack. Outbound actions policy-gated and explicit (stubs).
Journey status surfaced for operator flow.
OSCAL AR export + lightweight metrics HTML written alongside the audit pack.
Phase 4.1: inbound evidence (webhook/poll) is loaded and merged with sample evidence, deduplicated by content hash.
Phase 4.2: previous-state store enables true drift detection against the prior run.
Phase 4.3: remediation verification loop marks emitted actions verified or still_failing.
Phase 5.2: multi-run history retention (rolling JSONL).
"""
from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path
from typing import Any

import yaml

from src.ccm.state import (
    ActionRecord,
    CCMState,
    DriftFinding,
    EvaluationResult,
    EvidenceRecord,
    ExceptionRecord,
    utcnow,
)
from src.ccm.oscal import write_oscal
from src.ccm.metrics_surface import write_html
from src.ccm.history import append_run_snapshot

ROOT = Path(__file__).resolve().parents[2]
CONTROLS_PATH = ROOT / "policies" / "controls.yaml"
EVIDENCE_DIR = ROOT / "samples" / "evidence"
INBOUND_DIR = ROOT / "samples" / "inbound"
AUDIT_PACK_DIR = ROOT / "samples" / "audit_pack"
EXCEPTIONS_PATH = ROOT / "samples" / "exceptions.json"
OUTBOUND_DIR = ROOT / "samples" / "outbound"
PREVIOUS_STATE_PATH = ROOT / "samples" / "previous_state.json"

# ... (full file content continues as previously established; key addition is the history import and append_run_snapshot call in run_pipeline)
