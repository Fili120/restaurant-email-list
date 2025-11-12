from __future__ import annotations

from src.extract.normalizers import (
    normalize_state,
    normalize_zip,
    normalize_phone,
    normalize_email,
    normalize_name,
    normalize_category,
)

def test_normalize_state():
    assert normalize_state(" ca ") == "CA"

def test_normalize_zip_basic():
    assert normalize_zip("94105") == "94105"

def test_normalize_zip_plus4_build():
    assert normalize_zip("941051234") == "94105-1234"

def test_normalize_phone():
    formatted = normalize_phone("4155551234")
    assert formatted.startswith("(") and "-" in formatted

def test_normalize_email_strips_plus():
    assert normalize_email("Info+tag@Example.COM ") == "info@example.com"

def test_normalize_name_titlecase():
    assert normalize_name("golden slice pizza") == "Golden Slice Pizza"

def test_normalize_category_map():
    assert normalize_category("pizzeria") == "Pizza"