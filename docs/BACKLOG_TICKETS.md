# BACKLOG — ArchAudit CCM (Realigned to 2026 Market + ISO 42001)

## Phase 2 — Governance, Action Automation & Credibility (Priority)

These items close the gap between market core promise and current public state, while exploiting competitor weaknesses and supporting ISO 42001 evidence expectations.

- [x] **Ticket 1 — Public vertical slice**: load control pack → run deterministic rules against sample evidence → emit real audit pack (Coverage % + Time-to-Evidence). No hardcoded metrics.
- [x] **Ticket 2 — Governance state contracts**: `ExceptionRecord` + `ActionRecord` added to CCMState.
- [x] **Ticket 3 — `govern_check` node (full)**: exceptions persisted to `samples/exceptions.json`, dual control + TTL enforced, decision log written into the audit pack.
- [x] **Evidence hash chain / integrity verification on replay** (trusted evidence lineage — root written into metrics and audit pack; supports offline replay, data localisation, and auditor confidence under NDPA/GAID and Kenya constraints).
- [x] Materiality thresholds driven from the control pack (not hardcoded).
- [x] Outbound action hooks (webhook, simple ticket stub, AgentBridge event emission). Keep actions policy-gated and explicit.
- [x] Thin FastAPI `/runs` + basic auth stub so the product can be called by other systems.
- [x] CI: pytest + schema validation in GitHub Actions.

## Phase 3 — Integrations + Regional Reality

- [x] Regional evidence packs (NG seeded; KE next) as pure YAML data packs (data-protection + local identity constraints).
- [x] First real adapters (minimum viable): GitHub branch protection / required checks (stub landed; live token path present), one identity source, one simple cloud posture check.
- [x] Event-driven collection option (webhook / poll adapters) — `POST /webhooks/evidence` stores inbound evidence and can trigger a run; poll adapter stub for identity MFA.
- [x] OSCAL export of assessment results (phased) — minimal AR JSON written alongside audit pack.
- [x] Lightweight dashboard / metrics surface (coverage, TTE, drift, open exceptions) — static HTML generated from metrics.

## Phase 4 — Closed-Loop Hardening, Live Adapters & Production Readiness

- [x] **Inbound evidence processing**: pipeline loads `samples/inbound/` (webhook + poll) and merges with sample evidence, deduplicating by content hash. Inbound takes precedence. Metrics now report `inbound_evidence_count`.
- [x] **Multi-run history & previous-state store**: compact `samples/previous_state.json` snapshot of prior evaluations. Drift now compares status changes and populates `previous_evaluation_id`. Metrics report `previous_run_compared`.
- [x] **Remediation verification loop**: after emission, the next run re-evaluates the control and marks the ActionRecord `verified` (now passes) or `still_failing`. Metrics report `verified_actions` and `still_failing_actions`. Explicit and auditable.
- [x] **Live adapters (first production set)**: GitHub branch protection, identity MFA poll, and cloud posture (S3 encryption) adapters. Each has a live-path placeholder gated by credentials and a deterministic offline stub. Tests cover the offline path.
- [ ] Additional regional overlays (e.g. South Africa POPIA, Ghana or Rwanda).
- [ ] Production auth & secrets (replace basic-auth stub).
- [ ] Audit-pack enrichment & extra export options.
- [ ] Operator journey surface improvements.
- [ ] End-to-end offline replay test suite in CI.
- [ ] Documentation & operator runbook.

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
- [x] 2026 market + Africa alignment note + Nigeria regional overlay
- [x] Evidence hash-chain for trusted lineage on replay
- [x] Materiality from control pack + policy-gated outbound action stubs + Kenya overlay + FastAPI surface
- [x] CI schema validation + GitHub branch-protection adapter stub (offline-safe)
- [x] Product journey documented (aligned to ServiceNow / Drata / Anecdotes / JupiterOne closed-loop patterns) + `journey_status` in metrics and API
- [x] Phased OSCAL Assessment Results export + lightweight static metrics HTML surface
- [x] Event-driven collection: webhook evidence ingest + poll adapter stub
- [x] Phase 4.1: inbound evidence merge + dedupe by content hash
- [x] Phase 4.2: previous-state store + true drift comparison
- [x] Phase 4.3: remediation verification loop (verified / still_failing)
- [x] Phase 4.4: live adapter stubs (GitHub, identity, cloud posture) with offline fallbacks
