from __future__ import annotations

import json
import os
import random
from typing import Dict, Iterable, List

from .normalizers import (
    normalize_address,
    normalize_category,
    normalize_city,
    normalize_email,
    normalize_name,
    normalize_phone,
    normalize_state,
    normalize_zip,
)

NAMES = [
    "Golden Slice Pizza",
    "Example Cafe",
    "Sunset BBQ",
    "Riverside Diner",
    "Maple & Main Bistro",
    "Harbor View Seafood",
    "Fiesta Taqueria",
    "Lotus Garden",
    "Olive Branch Mediterranean",
    "Morning Brew Coffee"
]

CITIES = [
    "San Francisco", "Los Angeles", "San Diego", "Sacramento", "San Jose",
    "Fresno", "Oakland", "Bakersfield", "Long Beach", "Irvine"
]

STREET_NAMES = [
    "Main St", "Market St", "Broadway", "Pine Ave", "Elm St",
    "Sunset Blvd", "Maple Rd", "2nd Ave", "Harbor Dr", "Mission St"
]

CATEGORIES = ["Pizza", "Cafe", "BBQ", "Seafood", "Mexican", "Chinese", "Mediterranean", "Coffee", "Diner", "Bistro"]

def _fake_zip(state: str) -> str:
    # simple state-based seed to create repeatable zip ranges
    base = (ord(state[0]) + ord(state[1])) % 80 + 10
    return f"{base}{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}"

def _fake_phone() -> str:
    # NANP-like: (NXX) NXX-XXXX
    nxx = lambda: f"{random.randint(2,9)}{random.randint(0,9)}{random.randint(0,9)}"
    xxxx = f"{random.randint(0,9)}{random.randint(0,9)}{random.randint(0,9)}{random.randint(0,9)}"
    return f"({nxx()}) {nxx()}-{xxxx}"

def _fake_email(name: str) -> str:
    base = (
        name.lower()
        .replace("&", "and")
        .replace(" ", "")
        .replace("'", "")
        .replace(".", "")
    )
    domains = ["example.com", "gmail.com", "outlook.com", "yahoo.com"]
    return f"hello@{base}.{random.choice(domains).split('.',1)[-1]}" if "." not in base else f"hello@{base}.com"

def collect_restaurants(state: str, limit: int = 100) -> List[Dict[str, str]]:
    """
    Generates deterministic but realistic restaurant records for the given state.
    This is a stand-in for a real scraper/collector module.
    """
    state = normalize_state(state)
    records: List[Dict[str, str]] = []

    for i in range(limit):
        name = normalize_name(NAMES[i % len(NAMES)])
        city = normalize_city(CITIES[(i * 3) % len(CITIES)])
        address = normalize_address(f"{random.randint(10, 9999)} {STREET_NAMES[(i * 7) % len(STREET_NAMES)]}")
        zipcode = normalize_zip(_fake_zip(state))
        phone = normalize_phone(_fake_phone())
        email = normalize_email(_fake_email(name))
        category = normalize_category(CATEGORIES[i % len(CATEGORIES)])

        records.append(
            {
                "restaurant_name": name,
                "address": address,
                "city": city,
                "state": state,
                "zipcode": zipcode,
                "phone": phone,
                "email": email,
                "category": category,
            }
        )

    return records