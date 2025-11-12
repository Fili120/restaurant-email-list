from __future__ import annotations

from typing import Dict, Set

def validate_input(payload: Dict) -> None:
    if not isinstance(payload, dict):
        raise ValueError("input must be a JSON object")
    if "state" not in payload:
        raise ValueError("missing required field 'state'")
    state = payload["state"]
    if not isinstance(state, str) or len(state.strip()) < 2:
        raise ValueError("'state' must be a 2-letter code")

def validate_state_code(state: str, allowed: Set[str]) -> str:
    code = state.strip().upper()[:2]
    if code not in allowed:
        raise ValueError(f"Unsupported state code '{code}'")
    return code