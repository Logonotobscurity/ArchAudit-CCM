# ADR-001 v3.1 — Evidence-native CCM with Action Automation

## Status
Accepted (2026-09-01, realigned 2026-11-15)

## Context

The 2026 Continuous Control Monitoring market has converged on a clear core promise:

> Always-on proof that controls are operating, continuous evidence collection, and the ability to act when controls fail.

Dominant platforms (ServiceNow IRM agentic CCM, Cyber Sierra, Drata, Vanta, Scytale, Compyl, etc.) deliver this through large integration catalogs, automated tests, and increasingly agentic interpretation + remediation loops.

Their persistent weaknesses are:
- Evidence is frequently treated as “artifact present” rather than typed, lineage-backed, and fully replayable.
- Evaluation is often opaque or fully delegated to agents, introducing non-determinism that regulated environments reject.
- Action/remediation is tightly coupled to the vendor’s workflow engine (high lock-in).
- Almost no product is designed for African / emerging-market operating realities (connectivity, identity systems, regulatory nuance).
- High cost and complexity for teams that only need a trustworthy control-monitoring layer.

ArchAudit is built for Continuous Control Monitoring in agentic systems and African operating environments. It must adopt the market’s core promise while systematically exploiting the weaknesses above.

### Governance Alignment (ISO 42001 + African context)

**Primary external target: ISO/IEC 42001:2023 (AI Management System).**  
ISO 42001 is the first certifiable international standard for an AI Management System. It expects:
- AI system inventory and scope (agents are AI systems),
- AI risk assessment + AI system impact assessment,
- life-cycle controls, data controls, human oversight / accountability,
- continuous monitoring and measurable evidence (Clause 9),
- continual improvement and corrective action.

ArchAudit’s design maps cleanly to the evidence and governance expectations of an AIMS auditor:
- typed Evidence + content-hash integrity → continuous, provenance-backed proof,
- deterministic-first evaluation → reduces opacity risk,
- explicit `govern_check` (exceptions, dual control, action hooks) → human oversight + corrective action,
- replayable audit packs (Coverage % + Time-to-Evidence) → the measurable evidence Clause 9 requires.

**Complementary frameworks:** NIST AI RMF (risk language), EU AI Act (legal obligations where applicable). ArchAudit is the continuous evidence substrate, not a full AIMS product or conformity-assessment tool.

**African context (Nov 2026):** Nigeria and Kenya rank among the more mature African AI-governance environments, but almost no binding AI-specific statute yet exists. Governance still rides primarily on data-protection law + national strategies. ArchAudit therefore treats ISO 42001 as the durable technical target and keeps regional packs (NG, KE) as data so future local obligations can be mapped without redesign.

## Decision

1. **Evidence is the source of truth.**  
   Adapters return typed Evidence only. No judgments are allowed in the collection plane. Every Evidence record carries a content hash and is designed for full offline replay.

2. **Deterministic rules first.**  
   Evaluation is performed by explicit, versioned rules. Any LLM/agent assistance is policy-gated, optional, and recorded as `decision_basis`. This preserves auditability and avoids the non-determinism risk of pure agentic CCM.

3. **Contracts over frameworks.**  
   Pydantic v2 schemas for Evidence, Evaluation, Drift, Exception/Action. Control packs remain pure YAML data.

4. **Skip on content hash.**  
   Avoid re-evaluation when evidence is unchanged. Measurable Time-to-Evidence and Coverage % are first-class outputs.

5. **Governance & Action plane is explicit (Phase 2).**  
   Exceptions, dual control, TTL, owner, and outbound actions (webhook, ticket, AgentBridge event) live in a dedicated `govern_check` node. Action automation is policy-driven, not hidden inside an agent runtime. This directly attacks the “action is locked inside the vendor platform” weakness.

6. **Integration plane is first-class.**  
   ArchAudit is designed to emit structured audit packs and events that larger GRC platforms or agentic delivery systems (AgentBridge) can consume. It does not attempt to own the full risk register or remediation UI. This keeps exit cost low and enables coexistence with ServiceNow, Drata, etc.

7. **Regional packs as data.**  
   NG/KE (and future) operating realities are expressed as YAML packs, not hard-coded adapters. This is currently unique in the category.

8. **Phased OSCAL / events.**  
   Machine-readable assessment export and event-driven collection remain on the roadmap; they are not required for the core promise.

## Consequences

- ArchAudit can honestly claim the same core market promise (continuous proof + action) while remaining lighter, more auditable, and more portable than the dominant platforms.
- Deterministic-first + typed evidence gives a clear technical story for regulated and African contexts where pure agentic judgment is unacceptable.
- Explicit action plane + integration surface prevents the product from becoming another closed GRC silo.
- The public vertical slice (contracts → deterministic evaluation → replayable pack) must be complete and runnable before heavy marketing claims are made.
- Alignment with ISO 42001 strengthens the FDE / AI+GRC narrative without expanding ArchAudit into a full AIMS product.

## Alternatives considered

- Full agentic evaluation as primary path → rejected (non-determinism + auditability risk).
- Building a complete GRC suite → rejected (wrong scope; high competition; loses differentiation).
- Immediate deep integration catalog → deferred (correctness of contracts and evaluation comes first).
- Cloud-vendor-centric assumptions → rejected (incompatible with African operating context goal).
