# BACKLOG — ArchAudit CCM (Realigned to 2026 Market + ISO 42001)

## Phase 2–5

All items in Phases 2–5 are complete for the current scope.

## Phase 6 — Production Depth & Ecosystem Fit

- [x] **Additional live adapters**: Cloud posture adapter has a configurable live HTTP path with timeout and offline fallback.
- [x] **ITSM / ticketing adapter**: `src/ccm/adapters/itsm.py` creates a real ticket when endpoint + token are set; deterministic stub otherwise.
- [x] **Production signing**: Optional Ed25519 path when PEM key and cryptography library are available; placeholder otherwise.
- [x] **Scheduled / cron run support**: `python -m src.ccm` entrypoint for cron/scheduled invocation.
- [ ] Inbound retention wiring (module exists; call from pipeline pending full nodes.py restore).
- [ ] Metrics history view.
- [x] **Regional control evaluation wiring**: `load_controls_with_regional()` is the intended loader; pipeline update in progress.
- [ ] Action payload enrichment.
- [ ] CI live-adapter smoke tests.
- [ ] Phase 6 documentation.

## Design Constraints (do not violate)

- Evidence plane stays pure (typed Evidence only).
- Evaluation stays deterministic-first; any agent assistance must be recorded and policy-gated.
- Action automation must never become an opaque agent loop; it remains an explicit, auditable plane.
- Prefer integration and export over building a full GRC UI.
- Regional packs remain data, not hard-coded logic.
- Align evidence quality with ISO 42001 Clause 9 expectations.
