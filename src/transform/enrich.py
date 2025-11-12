from __future__ import annotations

from typing import Dict, Iterable, List

KEYWORD_TO_CATEGORY = {
    "pizza": "Pizza",
    "slice": "Pizza",
    "brew": "Coffee",
    "coffee": "Coffee",
    "cafe": "Cafe",
    "bbq": "BBQ",
    "bar": "Bar & Grill",
    "grill": "Bar & Grill",
    "seafood": "Seafood",
    "taqueria": "Mexican",
    "garden": "Chinese",
    "mediterranean": "Mediterranean",
    "diner": "Diner",
    "bistro": "Bistro",
}

def infer_category(name: str, existing: str | None) -> str | None:
    if existing:
        return existing
    lowered = name.lower()
    for kw, cat in KEYWORD_TO_CATEGORY.items():
        if kw in lowered:
            return cat
    return None

def enrich(records: Iterable[Dict[str, str]]) -> List[Dict[str, str]]:
    enriched: List[Dict[str, str]] = []
    for rec in records:
        rec = dict(rec)
        rec["category"] = infer_category(rec.get("restaurant_name", ""), rec.get("category"))
        enriched.append(rec)
    return enriched