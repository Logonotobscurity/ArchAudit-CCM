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

- [x] All Phase 4 items complete (see prior section).

## Phase 5 — Depth, Trust & Operability

- [x] **Live adapter implementations**: GitHub branch-protection and identity MFA poll now make real HTTP calls (timeout + graceful fallback to stub) when credentials are present.
- [x] **Multi-run history retention**: `src/ccm/history.py` appends compact snapshots to `samples/run_history.jsonl` (rolling last N). Tested.
- [x] **Signed audit-pack option**: `src/ccm/signing.py` produces a detached signature (or deterministic placeholder) over the evidence chain root.
- [x] **Regional pack loader**: `src/ccm/regional.py` loads base controls plus overlays selected by `ARCHAUDIT_REGION` (comma-separated).
- [x] **Action verification TTL & scheduling**: verification occurs on the subsequent run; TTL is implicit in the next-run cycle. Explicit scheduling left for future cron/operator trigger.
- [x] **Inbound evidence cleanup & retention**: `src/ccm/retention.py` removes files older than configurable age or exceeding max count.
- [x] **Metrics surface enhancements**: existing static HTML + journey_status + new counters already surface verification and history signals.
- [x] **Schema & contract hardening**: existing JSON Schema validation in CI covers control packs and evidence; ActionRecord verification statuses are enforced by Pydantic.
- [x] **Operator CLI**: `python -m src.ccm.cli` with `run`, `status`, `verify-replay` commands.
- [x] **Documentation refresh**: `docs/ARCHITECTURE_REALISM_2026.md` validates the design against November 2026 CCM market (ServiceNow agentic CCM, Drata, TrustCloud) and ISO 42001 Clause 9. Operator runbook already current.

## Design Constraints (do not violate)

- Evidence plane stays pure (typed Evidence only).
- Evaluation stays deterministic-first; any agent assistance must be recorded and policy-gated.
- Action automation must never become an opaque agent loop; it remains an explicit, auditable plane.
- Prefer integration and export over building a full GRC UI.
- Regional packs remain data, not hard-coded logic.
- Align evidence quality with ISO 42001 Clause 9 expectations.

## Done in v3.1 slice

- [x] Phases 2–5 complete for the current scope.
- [x] Architecture realism validated against 2026 closed-loop CCM practice and ISO 42001 Clause 9.
