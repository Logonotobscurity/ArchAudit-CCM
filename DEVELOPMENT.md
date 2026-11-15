# ArchAudit CCM — DEVELOPMENT.md (Realigned)

## Principles (market-aligned)

1. **Evidence is the source of truth** — adapters return typed Evidence only. Never judgments in collection.
2. **Deterministic rules first** — agent assistance is optional, policy-gated, and always recorded as `decision_basis`.
3. **Contracts over frameworks** — Pydantic v2 + YAML control packs.
4. **Skip on content hash** — measurable Time-to-Evidence and Coverage % are first-class.
5. **Action automation is explicit** — exceptions, dual control, outbound webhooks/tickets live in a dedicated governance plane, never as an opaque agent loop.
6. **Integration over ownership** — emit structured packs and events that larger GRC platforms or AgentBridge can consume. Do not build a full GRC UI.
7. **Regional packs as data** — NG/KE (and future) realities are YAML, not hard-coded adapters.
8. **Sample packs must be fully replayable offline.**

## Layout

```
apps/api/          FastAPI surface (Phase 2)
docs/adr/          ADRs
policies/          controls.yaml + schemas
samples/           audit_pack + evidence
src/               pipeline, rules, models
tests/
```

## Definition of Done (current focus)

- [ ] Public vertical slice runs end-to-end with real deterministic evaluation (no hardcoded metrics).
- [ ] `govern_check` node present with exceptions / dual-control / action hooks.
- [ ] Evidence integrity (hash chain) on replay.
- [ ] At least one outbound action path (webhook or event) that is policy-gated.
- [ ] CI green (pytest + schema validation).

## Do not

- Turn evaluation into a pure agent judgment path.
- Hide action/remediation inside an uninspectable agent runtime.
- Assume cloud-vendor ubiquity or US/EU-only identity systems.
- Compete on raw integration count; compete on evidence quality and operating-context fit.
