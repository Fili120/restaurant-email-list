from __future__ import annotations

from pathlib import Path
from typing import Set

def load_states(path: str) -> Set[str]:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"states list not found at {path}")
    codes: Set[str] = set()
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip().upper()
        if not line or line.startswith("#"):
            continue
        if len(line) == 2:
            codes.add(line)
    return codes