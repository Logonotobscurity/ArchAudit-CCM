# BACKLOG — ArchAudit CCM (Realigned to 2026 Market)

## Phase 2 — Governance, Action Automation & Credibility (Priority)

These items close the gap between market core promise and current public state, while exploiting competitor weaknesses.

- [ ] Complete public vertical slice: load control pack → run deterministic rules against sample evidence → emit real audit pack (Coverage % + Time-to-Evidence). Remove hardcoded metrics from the public runner.
- [ ] `govern_check` node: exceptions, dual control, TTL, owner, decision log.
- [ ] Materiality thresholds driven from the control pack (not hardcoded).
- [ ] Evidence hash chain / integrity verification on replay (trusted evidence lineage).
- [ ] Outbound action hooks (webhook, simple ticket stub, AgentBridge event emission). Keep actions policy-gated and explicit.
- [ ] Thin FastAPI `/runs` + basic auth stub so the product can be called by other systems.
- [ ] CI: pytest + schema validation in GitHub Actions.

## Phase 3 — Integrations + Regional Reality

- [ ] First real adapters (minimum viable): GitHub branch protection / required checks, one identity source, one simple cloud posture check.
- [ ] Regional evidence packs (NG, KE) as pure YAML data packs.
- [ ] Event-driven collection option (webhook / poll adapters).
- [ ] OSCAL export of assessment results (phased).
- [ ] Lightweight dashboard / metrics surface (coverage, TTE, drift, open exceptions).

## Design Constraints (do not violate)

- Evidence plane stays pure (typed Evidence only).
- Evaluation stays deterministic-first; any agent assistance must be recorded and policy-gated.
- Action automation must never become an opaque agent loop; it remains an explicit, auditable plane.
- Prefer integration and export over building a full GRC UI.
- Regional packs remain data, not hard-coded logic.

## Done in v3 slice

- [x] Deterministic rules first (contracts)
- [x] Typed Evidence / Evaluation / Drift
- [x] Skip on content hash (concept)
- [x] Sample audit pack output structure
- [x] ADR + market realignment (v3.1)
