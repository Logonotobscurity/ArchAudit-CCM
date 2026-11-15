# BACKLOG — ArchAudit CCM (Realigned to 2026 Market + ISO 42001)

## Phase 2 — Governance, Action Automation & Credibility (Priority)

These items close the gap between market core promise and current public state, while exploiting competitor weaknesses and supporting ISO 42001 evidence expectations.

- [x] **Ticket 1 — Public vertical slice**: load control pack → run deterministic rules against sample evidence → emit real audit pack (Coverage % + Time-to-Evidence). No hardcoded metrics.
- [x] **Ticket 2 — Governance state contracts**: `ExceptionRecord` + `ActionRecord` added to CCMState.
- [x] **Ticket 3 — `govern_check` node (full)**: exceptions persisted to `samples/exceptions.json`, dual control + TTL enforced, decision log written into the audit pack.
- [ ] Materiality thresholds driven from the control pack (not hardcoded).
- [ ] Evidence hash chain / integrity verification on replay (trusted evidence lineage).
- [ ] Outbound action hooks (webhook, simple ticket stub, AgentBridge event emission). Keep actions policy-gated and explicit.
- [ ] Thin FastAPI `/runs` + basic auth stub so the product can be called by other systems.
- [ ] CI: pytest + schema validation in GitHub Actions.

## Phase 3 — Integrations + Regional Reality

- [ ] First real adapters (minimum viable): GitHub branch protection / required checks, one identity source, one simple cloud posture check.
- [ ] Regional evidence packs (NG, KE) as pure YAML data packs (data-protection + local identity constraints).
- [ ] Event-driven collection option (webhook / poll adapters).
- [ ] OSCAL export of assessment results (phased).
- [ ] Lightweight dashboard / metrics surface (coverage, TTE, drift, open exceptions).

## Design Constraints (do not violate)

- Evidence plane stays pure (typed Evidence only).
- Evaluation stays deterministic-first; any agent assistance must be recorded and policy-gated.
- Action automation must never become an opaque agent loop; it remains an explicit, auditable plane.
- Prefer integration and export over building a full GRC UI.
- Regional packs remain data, not hard-coded logic.
- Align evidence quality with ISO 42001 Clause 9 expectations.

## Done in v3.1 slice

- [x] Deterministic rules first (contracts + real evaluator)
- [x] Typed Evidence / Evaluation / Drift / Exception / Action
- [x] Skip on content hash (concept; full previous-run store still pending)
- [x] Sample audit pack output structure with real metrics
- [x] ADR + market realignment + ISO 42001 / African governance note (v3.1)
- [x] Exception persistence + dual-control governance (Ticket 3)
