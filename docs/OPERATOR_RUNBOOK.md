# ArchAudit CCM — Operator Runbook

## Trigger a run

```bash
python -m src.ccm run
# or
uvicorn src.ccm.api:app --reload
curl -H "X-API-Key: $CCM_API_KEY" -X POST http://localhost:8000/runs
```

Output: `samples/audit_pack/` (metrics.json, summary.md, assessment-results.oscal.json, metrics.html).

## Ingest evidence

```bash
curl -H "X-API-Key: $CCM_API_KEY" -X POST http://localhost:8000/webhooks/evidence \
  -H "Content-Type: application/json" \
  -d '{"control_id":"ACC-MFA-ADMIN","source":"okta","payload":{"admin_mfa":true}}'
```

Files land in `samples/inbound/` and merge on the next run.

## Enable regional controls

```bash
export ARCHAUDIT_REGION=NG,ZA
python -m src.ccm run
```

## Verify offline replay

```bash
python -m src.ccm verify-replay
```

## Clean inbound evidence

Retention runs automatically at the start of each pipeline execution.  
Override with `ARCHAUDIT_INBOUND_MAX_AGE_DAYS` or `ARCHAUDIT_INBOUND_MAX_FILES`.

## Sign the audit pack

```bash
export ARCHAUDIT_SIGNING_KEY=/path/to/ed25519.pem
python -m src.ccm run
```

## Live adapters

Set credentials to enable live paths:
- `GITHUB_TOKEN` — branch protection
- `IDENTITY_TOKEN` + `IDENTITY_ENDPOINT` — MFA poll
- `CLOUD_POSTURE_ENDPOINT` + token — cloud posture
- `ITSM_ENDPOINT` + `ITSM_TOKEN` — ticket creation

All adapters fall back to deterministic stubs when credentials are absent or calls fail.

## Journey status

| Status | Meaning |
|--------|---------|
| all_controls_passing | No failures |
| actions_emitted_awaiting_verification | Actions sent; waiting for next run |
| pending_actions_need_emission | Failures exist; actions not yet emitted |
| failures_suppressed_by_exception | All failures covered by valid exceptions |
| failures_open | Failures remain |
