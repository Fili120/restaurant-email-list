from __future__ import annotations

from typing import Dict, Iterable, List, Tuple

def dedupe_records(records: Iterable[Dict[str, str]]) -> List[Dict[str, str]]:
    """
    Remove duplicates using (email) primary key, then (name, phone) fallback.
    """
    seen_email: set[str] = set()
    seen_pair: set[Tuple[str, str]] = set()
    unique: List[Dict[str, str]] = []

    for rec in records:
        email = rec.get("email", "").lower().strip()
        pair = (rec.get("restaurant_name", "").strip().lower(), rec.get("phone", "").strip())
        if email and email in seen_email:
            continue
        if not email and pair in seen_pair:
            continue

        if email:
            seen_email.add(email)
        else:
            seen_pair.add(pair)
        unique.append(rec)

    return unique