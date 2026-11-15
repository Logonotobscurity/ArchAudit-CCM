# MILESTONES — ArchAudit CCM (Realigned)

## M0 — Contracts (done)
Evidence, Evaluation, Drift, Exception/Action schemas; control pack YAML.

## M1 — Pipeline slice (done as skeleton)
ingest → collect → skip → evaluate → drift → report. Sample pack structure exists.  
**Next:** make the public runner execute real deterministic evaluation end-to-end.

## M2 — Governance + Action Automation (current focus)
- `govern_check` node with exceptions, dual control, TTL, owner
- Materiality from control pack
- Evidence integrity (hash chain)
- Explicit outbound actions (webhook / ticket / AgentBridge)
- FastAPI surface + solid CI

This milestone delivers the market core promise (continuous proof + ability to act) while keeping determinism and auditability.

## M3 — Integrations + Regional packs
Real adapters, NG/KE packs as data, event-driven option, OSCAL path.

## M4 — Operational surface
Lightweight metrics / dashboard and production hardening.

---

**Guiding principle:** Ship the smallest complete vertical slice that a reviewer can run and trust, then expand the action and integration planes. Do not compete on integration count; compete on evidence quality, determinism, and operating-context fit.
