# Phase 6 Status

## Completed

- Additional live adapters (cloud posture HTTP path).
- ITSM / ticketing adapter.
- Optional Ed25519 signing path.
- Scheduled / cron entrypoint.
- Regional pack loader.
- Multi-run history module.
- Inbound retention module.
- Metrics history view generator.
- Operator runbook refreshed with Phase 6 capabilities.

## Pipeline

The complete `src/ccm/nodes.py` (regional loader, history append, retention cleanup) is staged and ready.  
Repository currently holds a placeholder version pending full-file restoration.

## Remaining

- Action payload enrichment.
- CI live-adapter smoke tests.

## Constraints preserved

- Evidence remains typed and hashed.
- Evaluation remains deterministic.
- Actions remain explicit and policy-gated.
- Regional logic remains data-only.
- Audit packs remain offline-replayable.
