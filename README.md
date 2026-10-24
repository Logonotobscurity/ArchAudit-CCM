# ArchAudit CCM

[![Python](https://img.shields.io/badge/Python-3.11+-blue)]()
[![Pydantic](https://img.shields.io/badge/Pydantic-v2-green)]()
[![Status](https://img.shields.io/badge/Status-evidence--native%20CCM-brightgreen)]()

**Evidence-native, deterministic-first Continuous Control Monitor for African operating environments.**

Typed evidence contracts, policy-as-code control packs, and a fully replayable audit pipeline. Agents assist only under policy gates; collection stays pure.

---

## What problem does this solve?

Control evidence goes stale. Teams cannot produce a measurable audit pack (Coverage % + Time-to-Evidence) without manual screenshot hunts. ArchAudit turns evidence collection into a deterministic, hash-aware, offline-replayable loop.

## What is implemented

- Six-layer pipeline: Intake → Collection → Skip → Evaluation → Drift → Reporting
- Pydantic v2 contracts for Evidence, Evaluation, Drift
- YAML control pack (Access, Change, Logging families)
- Content-hash skip gate
- Sample audit pack with metrics
- ADR trail (v2 → v3) and technical specification

## Architecture / stack

Python 3.11+ · Pydantic v2 · PyYAML · pytest  
Optional LangGraph-shaped orchestration. MCP-shaped tool envelopes.

```
ingest_run → collect → maybe_skip → evaluate → drift → report
```

## What a reviewer can run

```bash
pip install -r requirements.txt
make test
make run-sample
```

## Portfolio value

Demonstrates evidence-first design, deterministic rules over agent judgments, and machine-readable control packs suitable for African GRC and security engineering contexts.

## Limitations

Governance plane (exceptions, dual control) is Phase 2. Regional packs and OSCAL export are phased.

## Companion repositories

- [AgentBridge-Africa](https://github.com/Logonotobscurity/AgentBridge-Africa)
- [GigPilot](https://github.com/Logonotobscurity/GigPilot)
