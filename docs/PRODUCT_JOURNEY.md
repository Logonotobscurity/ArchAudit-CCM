# ArchAudit CCM — Product Journey Flow

Last updated: 15 November 2026. Research-aligned to current market practice.

## Market patterns (what others do)

| Platform | Typical journey | Closed-loop elements |
| --- | --- | --- |
| ServiceNow IRM (agentic CCM, Nov 2026) | Detect drift/failure across 100+ systems → agent interprets with context → flag → open ticket → optional policy-gated remediation → verify → close | Explicit closed loop; IDC-noted differentiator vs dashboards |
| Drata | Monitoring page shows test history → investigate findings → remediate (notes/tasks/tickets) → re-run test → readiness updates | Workflows on readiness change; mean-time-to-remediation metric |
| Anecdotes Agentic CCM | Gap detected → tailored notification (owner/risk/tech) → managed remediation (Jira/PagerDuty/API) → continuous re-verification | Three pillars: Intelligent Notification, Managed Remediation, Continuous Reassurance |
| JupiterOne CCM | Graph query tests → drift alert to Slack/Jira → OU ownership → lifecycle (open → awaiting verification → fixed) | Daily digests, framework scorecards, drill-down to tests |

Common realistic journey: **Collect evidence → Evaluate → Detect gap/drift → Govern (exception or escalate) → Emit action (ticket/webhook/notify) → Verify on next run → Report**. Ownership and materiality drive prioritization. Evidence stays provenance-backed.

## ArchAudit journey (deterministic, evidence-native)

1. **Collect** — Typed `EvidenceRecord` from samples or adapters (GitHub branch protection stub today; others next). Content-hashed for offline replay.
2. **Evaluate** — Deterministic rule evaluation against evidence payload. Status: pass / fail / unknown. Decision basis recorded.
3. **Drift** — Materiality pulled from control pack (not hardcoded). Failing controls inherit pack materiality (informational/material/urgent).
4. **Govern** — Load persisted exceptions. Dual-control + TTL check. Valid exception → suppress action. No exception → create explicit pending `ActionRecord` (agentbridge_event / webhook / ticket).
5. **Emit** — Policy-gated stubs written to `samples/outbound/`. Status moves pending → emitted. Fully auditable, no opaque loop.
6. **Report** — Metrics (coverage, TTE, drift count, open exceptions, pending/emitted/suppressed actions) + decision log + evidence chain root written to audit pack. Ready for auditor or next system.

## Usage flow for operators

- Run pipeline (CLI or `POST /runs` with basic auth).
- Review `samples/audit_pack/summary.md` or API response for failures and emitted actions.
- For emitted actions: human or external system consumes the stub (ticket creation, webhook receiver, AgentBridge).
- On next run, new evidence can close the loop (re-evaluate after remediation).
- Exceptions (dual-control) suppress noise for accepted risk.

## Africa / localisation fit

- Offline-replayable (hash chain + stubs) survives intermittent connectivity.
- Regional packs (NG/KE) are pure data overlays.
- Explicit dual-control matches human-oversight expectations under NDPA/GAID and Kenya DPA.
- Lightweight (no heavy GRC UI required); prefer export and integration.

This journey stays closer to the deterministic layer than pure agentic remediation, while matching the closed-loop expectation buyers now see in ServiceNow and Anecdotes.
