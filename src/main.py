from __future__ import annotations

import argparse
import json
import os
import random
import sys
from pathlib import Path
from typing import List

# Ensure 'src' directory (this file's parent) is on sys.path so namespace packages import without __init__.py
THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from ingest.state_loader import load_states
from ingest.validators import validate_input, validate_state_code
from extract.collectors import collect_restaurants
from extract.normalizers import (
    normalize_address,
    normalize_category,
    normalize_city,
    normalize_email,
    normalize_name,
    normalize_phone,
    normalize_state,
    normalize_zip,
)
from transform.dedupe import dedupe_records
from transform.enrich import enrich
from output.exporters import export_csv, export_json
from output.schema import RestaurantRecord

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Restaurant Email List Scraper (state-based)")
    parser.add_argument("--input", type=str, default="data/inputs.sample.json", help="Path to JSON input file")
    parser.add_argument("--settings", type=str, default="config/settings.example.json", help="Path to settings JSON")
    parser.add_argument("--states", type=str, default="config/states.list", help="Path to states list")
    parser.add_argument("--out", type=str, default=None, help="Output path (overrides settings)")
    parser.add_argument("--format", type=str, choices=["json", "csv"], default=None, help="Output format (overrides settings)")
    parser.add_argument("--limit", type=int, default=None, help="Record limit (overrides settings)")
    parser.add_argument("--seed", type=int, default=None, help="Random seed (overrides settings)")
    return parser.parse_args()

def load_json(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def normalize_record(rec: dict) -> dict:
    return {
        "restaurant_name": normalize_name(rec["restaurant_name"]),
        "address": normalize_address(rec["address"]),
        "city": normalize_city(rec["city"]),
        "state": normalize_state(rec["state"]),
        "zipcode": normalize_zip(rec["zipcode"]),
        "phone": normalize_phone(rec["phone"]),
        "email": normalize_email(rec["email"]),
        "category": normalize_category(rec.get("category")),
    }

def validate_with_schema(records: List[dict]) -> List[dict]:
    validated: List[dict] = []
    for r in records:
        model = RestaurantRecord.model_validate(r)
        validated.append(model.model_dump())
    return validated

def main() -> int:
    args = parse_args()

    # Load settings with sensible defaults
    settings_path = args.settings
    settings = load_json(settings_path) if Path(settings_path).exists() else {
        "output_format": "json",
        "limit": 1000,
        "seed": 42,
        "output_path": "data/sample_output.json"
    }

    output_path = args.out or settings.get("output_path", "data/sample_output.json")
    output_format = args.format or settings.get("output_format", "json")
    limit = int(args.limit or settings.get("limit", 1000))
    seed = int(args.seed or settings.get("seed", 42))

    random.seed(seed)

    # Load and validate input
    payload = load_json(args.input)
    validate_input(payload)

    allowed_states = load_states(args.states)
    state = validate_state_code(payload["state"], allowed_states)

    # Collect
    raw_records = collect_restaurants(state, limit=limit)

    # Normalize
    normalized = [normalize_record(r) for r in raw_records]

    # Dedupe
    unique = dedupe_records(normalized)

    # Enrich
    enriched = enrich(unique)

    # Schema validation
    validated = validate_with_schema(enriched)

    # Export
    if output_format == "json":
        path = export_json(validated, output_path)
    else:
        path = export_csv(validated, output_path)

    print(f"Wrote {len(validated)} records to {path}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())