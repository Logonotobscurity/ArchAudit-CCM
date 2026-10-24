# Technical Implementation Specification

**Product:** FDE Platform — ArchAudit CCM · AgentBridge Africa · GigPilot
**Spec version:** 1.0 (aligned with ADR-001 v3)
**Date:** 2026-09-01

See full Drive document for complete module inventory, data contracts, and goals.
Core pipeline: ingest_run → collect → maybe_skip → evaluate → drift → report.
