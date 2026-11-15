# BACKLOG — ArchAudit CCM (Realigned to 2026 Market + ISO 42001)

## Phase 2–5

All items in Phases 2–5 are complete for the current scope. See prior commits.

## Phase 6 — Production Depth & Ecosystem Fit

- [x] **Additional live adapters**: Cloud posture adapter now has a configurable live HTTP path with timeout and offline fallback (in addition to existing GitHub and identity adapters).
- [x] **ITSM / ticketing adapter**: `src/ccm/adapters/itsm.py` creates a real ticket when `ITSM_ENDPOINT` + `ITSM_TOKEN` are set; otherwise returns a deterministic stub ticket ID.
- [x] **Production signing**: `src/ccm/signing.py` supports optional Ed25519 signing when a PEM key and the cryptography library are available; deterministic placeholder otherwise.
- [ ] Scheduled / cron run support.
- [ ] Inbound retention wiring.
- [ ] Metrics history view.
- [ ] Regional control evaluation wiring.
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
