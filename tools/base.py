"""MCP-shaped tool envelope."""
from __future__ import annotations

from typing import Any


def tool_result(ok: bool, data: dict[str, Any] | None = None, error_code: str | None = None, latency_ms: int = 0) -> dict[str, Any]:
    return {
        "ok": ok,
        "data": data or {},
        "error_code": error_code,
        "latency_ms": latency_ms,
        "content_hash": "stub",
    }
