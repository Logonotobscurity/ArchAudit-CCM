# Restore Complete Pipeline

The complete `src/ccm/nodes.py` is staged locally.

## Upload command

```bash
python3 << 'PY'
import json
from pathlib import Path

content = Path("/tmp/nodes_final.py").read_text()
payload = {
    "owner": "Logonotobscurity",
    "repo": "ArchAudit-CCM",
    "path": "src/ccm/nodes.py",
    "message": "Restore complete CCM pipeline with regional, history, and retention",
    "branch": "main",
    "sha": "6633dd59ae0109e7c9ad76fdfa4d57a3e2ec5979",
    "content": content,
}
Path("/tmp/restore_payload.json").write_text(json.dumps(payload))
print("Payload ready:", len(content), "chars")
PY
```

## Verification

```bash
python -m src.ccm verify-replay
```

Expected: exit code 0, "Offline replay stable".
