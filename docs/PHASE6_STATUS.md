# Phase 6 Status

## Completed

- Additional live adapters (cloud posture HTTP path with timeout and fallback).
- ITSM / ticketing adapter with configurable live path and deterministic stub.
- Optional Ed25519 signing path (placeholder when key or library absent).
- Scheduled / cron entrypoint (`python -m src.ccm`).
- Regional pack loader (`src/ccm/regional.py`).
- Multi-run history module (`src/ccm/history.py`).
- Inbound retention module (`src/ccm/retention.py`).
- Metrics history view generator (`src/ccm/metrics_history.py`).

## Pipeline wiring

The complete `src/ccm/nodes.py` includes:
- Regional loader call in `_load_control_pack`.
- History append after previous-state save.
- Retention cleanup at the start of `run_pipeline`.

## Remaining

- Action payload enrichment (include evaluation detail and materiality).
- Optional CI smoke test for live adapters.
- Final documentation refresh.

## Constraints preserved

- Evidence remains typed and hashed.
- Evaluation remains deterministic.
- Actions remain explicit and policy-gated.
- Regional logic remains data-only.
- Audit packs remain offline-replayable.
