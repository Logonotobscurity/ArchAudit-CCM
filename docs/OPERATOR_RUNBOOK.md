# ArchAudit CCM — Operator Runbook

Short guide for running, feeding, and interpreting the continuous control monitoring pipeline.

## 1. Trigger a run

```bash
make run-sample
# or
uvicorn src.ccm.api:app --reload
curl -u ccm:changeme -X POST http://localhost:8000/runs
# or with API key (when CCM_API_KEY is set)
curl -H "X-API-Key: $CCM_API_KEY" -X POST http://localhost:8000/runs
```

Output lands in `samples/audit_pack/`:
- `metrics.json` — coverage, TTE, drift, journey_status, chain root, action counters
- `summary.md` — human-readable pack
- `assessment-results.oscal.json` — OSCAL Assessment Results
- `metrics.html` — static operator surface

## 2. Ingest evidence via webhook

```bash
curl -H "X-API-Key: $CCM_API_KEY" -X POST http://localhost:8000/webhooks/evidence \
  -H "Content-Type: application/json" \
  -d '{"control_id":"ACC-MFA-ADMIN","source":"okta","payload":{"admin_mfa":true}}'
```

Files are written to `samples/inbound/` and automatically merged on the next run (deduped by content hash).

## 3. Interpret journey status

| Status | Meaning |
|--------|---------|
| `all_controls_passing` | No failures |
| `actions_emitted_awaiting_verification` | Remediation actions sent; waiting for next run |
| `pending_actions_need_emission` | Failures exist but actions not yet emitted |
| `failures_suppressed_by_exception` | All failures covered by valid dual-control exceptions |
| `failures_open` | Failures remain |

## 4. Add a regional pack

Drop a YAML file in `policies/regional/` (see `ng.yaml`, `ke.yaml`, `za.yaml`, `gh.yaml`).  
Pure data only — no code changes required. Controls are loaded when the pack is referenced.

## 5. Add or test an adapter

Adapters live in `src/ccm/adapters/`. Each returns a typed `EvidenceRecord` and falls back to a deterministic stub when credentials are absent.

```bash
export GITHUB_TOKEN=...
export IDENTITY_TOKEN=...
export AWS_ACCESS_KEY_ID=...
python -c "from src.ccm.adapters import collect_branch_protection; print(collect_branch_protection())"
```

## 6. Verify offline replay

```bash
python -c "
from src.ccm.nodes import run_pipeline
s1 = run_pipeline()
s2 = run_pipeline()
assert s1.metrics['evidence_chain_root'] == s2.metrics['evidence_chain_root']
print('Replay stable')
"
```

CI already runs this assertion.

## 7. Secrets

- `CCM_API_KEY` — enables API-key auth on `/runs` and `/webhooks/evidence`
- `GITHUB_TOKEN`, `IDENTITY_TOKEN`, `AWS_*` — enable live adapter paths

Never commit secrets. Use environment variables or a secret manager.
