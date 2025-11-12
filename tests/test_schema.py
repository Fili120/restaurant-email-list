from __future__ import annotations

from src.output.schema import RestaurantRecord

def test_restaurant_record_valid():
    rec = RestaurantRecord.model_validate(
        {
            "restaurant_name": "Example Cafe",
            "address": "123 Main St",
            "city": "San Francisco",
            "state": "CA",
            "zipcode": "94105",
            "phone": "(415) 555-1234",
            "email": "info@example.com",
            "category": "Cafe",
        }
    )
    assert rec.state == "CA"
    assert rec.zipcode.startswith("941")
    assert rec.email == "info@example.com"

def test_restaurant_record_zip_plus4():
    rec = RestaurantRecord.model_validate(
        {
            "restaurant_name": "Golden Slice Pizza",
            "address": "44 Market St",
            "city": "San Francisco",
            "state": "CA",
            "zipcode": "94105-1234",
            "phone": "(415) 555-9090",
            "email": "hello@goldenslice.com",
            "category": "Pizza",
        }
    )
    assert rec.zipcode.endswith("1234")