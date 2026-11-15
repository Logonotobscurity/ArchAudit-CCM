# Market Alignment 2026 — ArchAudit CCM

Last researched: 15 November 2026.

## Global market

- ISO/IEC 42001 is the certifiable AI Management System standard. Auditors sample **runtime evidence** (agent inventory, event logs of tool calls and policy decisions per A.6.2.8, pre-release evaluations + post-deploy monitoring, change history, closed corrective actions under Clause 10). Continuous monitoring is the practical answer for Clause 9 performance evaluation.
- Agentic continuous control monitoring is moving into production. ServiceNow announced agentic CCM for IRM (expected GA Q1 2027) that turns failed controls into tickets and automated fixes. Buyers prefer agents first on measurable internal work.
- Traditional GRC platforms are under strain: high manual evidence burden, delayed control testing, and low rates of real-time monitoring. Deterministic evaluation + explicit, auditable actions remain a differentiator against opaque agent loops.

## Outbound actions & integrations landscape (Nov 2026)

| Layer | Typical Players | Core Promise | Strength | Weakness |
| --- | --- | --- | --- | --- |
| Enterprise GRC platforms with agentic CCM | ServiceNow IRM (agentic CCM announced Nov 2026, GA Q1 2027), Cyber Sierra, MetricStream, OneTrust, LogicGate, Hyperproof | Always-on control testing + AI agents that interpret, ticket, and sometimes remediate | Breadth of integrations (100+), closed-loop remediation, multi-framework mapping | Heavy, expensive, vendor-locked, often still audit-focused rather than evidence-native; remediation is policy-gated but can become opaque |
| Compliance automation / evidence platforms | Vanta, Drata, Secureframe, Sprinto, Scytale, Anecdotes, Compyl | Automated evidence collection + continuous tests for SOC 2 / ISO / etc.; some ticket creation and webhook steps | Fast time-to-value for first audit, good integrations (Jira, Slack, ServiceNow) | Mostly “evidence exists” rather than “control is operating”; limited governance depth; actions often workflow-driven rather than explicitly auditable |
| Specialised / deterministic / agent-control layers | GATE (deterministic-agents), Kayllo Control, Vaikora-style policy gates, Panaseer (trusted evidence), emerging agent-control monitors | Deterministic enforcement, typed evidence, pre-action gating, replayable proof, require-approval | High trust, low hallucination risk, good for AI-agent environments, hash-chained audit | Narrower scope, fewer integrations, still early |

**Observed patterns for outbound actions:**
- ServiceNow IRM: failed control → flag → open ticket → optional auto-remediate within defined policies → verify. Closed loop emphasized by IDC.
- Anecdotes Agentic CCM: gap detection → tailored notification (control owner / risk / tech) → Jira/PagerDuty/Okta remediation → re-verify.
- Drata: write-access ticket creation for controls/monitoring/risks; custom workflows with “Send Webhook” steps to Zapier/Torq/ServiceNow.
- Deterministic gates (Vaikora, GATE, Kayllo): inline policy decision (allow/block/modify/require-approval) **before** action executes; deterministic, replayable, hash-chained log. No post-facto agent loop.

ArchAudit follows the deterministic layer pattern: ActionRecord is explicit, policy-gated, status tracked (pending → emitted/suppressed), stubs written for offline replay. No opaque agent remediation.

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
- Policy-gated, explicit outbound stubs (webhook/ticket/AgentBridge) written for offline replay — no opaque agent loop.

These choices keep the system lightweight, auditable, and operable under the infrastructure and regulatory constraints that exist in Nigeria and Kenya today.
