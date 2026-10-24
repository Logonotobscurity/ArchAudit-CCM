# ArchAudit CCM — DEVELOPMENT.md

## Principles
1. Evidence is the source of truth (adapters return typed Evidence only).
2. Deterministic rules first; agent assistance is policy-gated.
3. Contracts (Pydantic v2) over frameworks.
4. Skip re-eval on content hash match.
5. Sample packs must be fully replayable offline.

## Layout
```
apps/api/          FastAPI surface
docs/adr/          ADRs
policies/          controls.yaml + schemas
samples/           audit_pack + evidence
src/               pipeline, rules, models
tests/
```

## DoD (v3 slice)
- [x] Typed Evidence / Evaluation / Drift
- [x] Pipeline: ingest → collect → skip → evaluate → drift → report
- [x] Sample audit pack generated
- [x] Control pack YAML (Access, Change, Logging)
