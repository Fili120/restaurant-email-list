from __future__ import annotations

import re
import unicodedata
from typing import Dict

ZIP_RE = re.compile(r"\d{5}(-\d{4})?")
PHONE_RE = re.compile(r"\d")
WHITESPACE_RE = re.compile(r"\s+")

def normalize_whitespace(s: str) -> str:
    s = unicodedata.normalize("NFKC", s)
    return WHITESPACE_RE.sub(" ", s).strip()

def normalize_state(state: str) -> str:
    return normalize_whitespace(state).upper()[:2]

def normalize_zip(zipcode: str) -> str:
    digits = "".join(ch for ch in zipcode if ch.isdigit())
    if len(digits) >= 9:
        return f"{digits[:5]}-{digits[5:9]}"
    return digits[:5].zfill(5)

def normalize_phone(phone: str) -> str:
    digits = "".join(PHONE_RE.findall(phone))
    if len(digits) < 10:
        # pad with zeros to avoid validation crash; upstream should validate
        digits = digits.rjust(10, "0")
    area, central, line = digits[-10:-7], digits[-7:-4], digits[-4:]
    return f"({area}) {central}-{line}"

def normalize_email(email: str) -> str:
    email = normalize_whitespace(email).lower()
    # remove common tracking params after '+'
    if "@" in email and "+" in email.split("@", 1)[0]:
        local, domain = email.split("@", 1)
        local = local.split("+", 1)[0]
        email = f"{local}@{domain}"
    return email

def normalize_name(name: str) -> str:
    name = normalize_whitespace(name)
    # Title-case but preserve words like BBQ, USA etc.
    parts = []
    for token in name.split(" "):
        if token.isupper() and len(token) <= 4:
            parts.append(token)
        else:
            parts.append(token.title())
    return " ".join(parts)

def normalize_city(city: str) -> str:
    return normalize_name(city)

def normalize_address(address: str) -> str:
    return normalize_whitespace(address)

def normalize_category(category: str | None) -> str | None:
    if category is None:
        return None
    cat = normalize_whitespace(category).title()
    # Simple canonicalizations
    mapping: Dict[str, str] = {
        "Bbq": "BBQ",
        "Bar & Grill": "Bar & Grill",
        "Cafe": "Cafe",
        "Pizzeria": "Pizza",
        "Pizza": "Pizza",
    }
    return mapping.get(cat, cat)