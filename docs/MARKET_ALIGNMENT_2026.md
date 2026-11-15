# Market Alignment 2026 — ArchAudit CCM

Last researched: 15 November 2026.

## Global market

- ISO/IEC 42001 is the certifiable AI Management System standard. Auditors sample **runtime evidence** (agent inventory, event logs of tool calls and policy decisions per A.6.2.8, pre-release evaluations + post-deploy monitoring, change history, closed corrective actions under Clause 10). Continuous monitoring is the practical answer for Clause 9 performance evaluation.
- Agentic continuous control monitoring is moving into production. ServiceNow announced agentic CCM for IRM (expected GA Q1 2027) that turns failed controls into tickets and automated fixes. Buyers prefer agents first on measurable internal work.
- Traditional GRC platforms are under strain: high manual evidence burden, delayed control testing, and low rates of real-time monitoring. Deterministic evaluation + explicit, auditable actions remain a differentiator against opaque agent loops.

## African operating context (NG + KE priority)

- **Nigeria (NDPA 2023 + GAID 2025, effective Sep 2025)**: Continuous monitoring and evaluation required for AI/emerging technologies once deployed. DPIAs mandatory for automated decisions, new technologies, and listed sectors (including digital financial services). Safeguards must be documented for the annual compliance audit return. Human intervention rights apply to automated decisions with legal or similarly significant effects.
- **Kenya (Data Protection Act + July 2026 ODPC draft AI Guidance)**: Continuous post-deployment monitoring expected. DPIAs for high-risk AI (credit scoring, biometrics, generative platforms, etc.). Strong safeguards required for offshore AI transfers. High Court has directed government to complete a formal AI legal framework by May 2027.
- **Structural constraints that global tools ignore**:
  - Data localisation pressure (CBN January 2027 deadline for payment transaction data in Nigeria; readiness still incomplete across financial institutions).
  - Limited local data-centre capacity and power reliability.
  - Low-bandwidth / intermittent connectivity; imported frameworks assume continuous high-bandwidth sessions.
  - Compliance cost relative to local revenue; need for low-bandwidth contestability (e.g. SMS/USSD) and inference-focused audits.
  - Fragmented national laws across the continent.

## ArchAudit edge

ArchAudit is positioned as the continuous, deterministic evidence substrate that supports an ISO 42001 AIMS (inventory, risk/impact, human oversight, measurable evidence) rather than a full AIMS product.

It maps cleanly to the three gaps already identified:

1. **Production multi-agent + customer deployment reliability** → AgentBridge Africa (orchestration, eval harness, deployment playbook, local/African context).
2. **AI + GRC / compliance automation** → ArchAudit (agentic continuous control monitoring, evidence collection, audit reports, dual-control exceptions).
3. **End-to-end FDE delivery narrative + business outcomes** → GigPilot / full engagement simulation.

Differentiating design choices that match African realities:

- Offline-replayable, content-hashed evidence (survives intermittent connectivity and supports localisation).
- YAML regional packs as pure data (NG, KE) rather than hard-coded logic.
- Explicit dual-control + TTL exceptions and outbound actions (human oversight remains visible and auditable).
- Deterministic-first evaluation with any assisted path policy-gated and recorded.

These choices keep the system lightweight, auditable, and operable under the infrastructure and regulatory constraints that exist in Nigeria and Kenya today.
