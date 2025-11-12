from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Iterable, List, Dict

def export_json(records: Iterable[Dict[str, str]], path: str) -> str:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    data = list(records)
    out.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return str(out)

def export_csv(records: Iterable[Dict[str, str]], path: str) -> str:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    rows = list(records)
    if not rows:
        out.write_text("", encoding="utf-8")
        return str(out)

    fieldnames = list(rows[0].keys())
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)
    return str(out)