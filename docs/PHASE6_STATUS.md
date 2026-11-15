# Phase 6 Status

## Completed

- Additional live adapters (cloud posture HTTP path with timeout and fallback).
- ITSM / ticketing adapter with configurable live path and deterministic stub.
- Optional Ed25519 signing path (placeholder when key or library absent).
- Scheduled / cron entrypoint (`python -m src.ccm`).
- Regional pack loader (`src/ccm/regional.py`).
- Multi-run history module (`src/ccm/history.py`).
- Inbound retention module (`src/ccm/retention.py`).

## Wiring status

The full pipeline in `src/ccm/nodes.py` requires restoration of the complete implementation.  
The regional loader is ready to replace the previous `_load_control_pack` function.  
History append is ready to call after `_save_previous_state`.  
Retention cleanup is ready to call at the start of `run_pipeline`.

## Next steps

1. Restore the complete `nodes.py` from the last known good version.
2. Wire the regional loader, history append, and retention cleanup.
3. Add metrics history view to the static HTML surface.
4. Enrich outbound action payloads with evaluation detail and materiality.
5. Add optional CI smoke test for live adapters.

## Constraints preserved

- Evidence remains typed and hashed.
- Evaluation remains deterministic.
- Actions remain explicit and policy-gated.
- Regional logic remains data-only.
- Audit packs remain offline-replayable.
