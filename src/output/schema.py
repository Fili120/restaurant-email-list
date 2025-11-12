from __future__ import annotations

import re
from typing import Optional

from pydantic import BaseModel, Field, EmailStr, field_validator

ZIP_RE = re.compile(r"^\d{5}(?:-\d{4})?$")
PHONE_DIGITS_RE = re.compile(r"\d")
STATE_RE = re.compile(r"^[A-Z]{2}$")

class RestaurantRecord(BaseModel):
    restaurant_name: str = Field(min_length=1, max_length=200)
    address: str = Field(min_length=1, max_length=200)
    city: str = Field(min_length=1, max_length=120)
    state: str = Field(min_length=2, max_length=2)
    zipcode: str = Field(min_length=5, max_length=10)
    phone: str = Field(min_length=7, max_length=20)
    email: EmailStr
    category: Optional[str] = Field(default=None, max_length=120)

    @field_validator("zipcode")
    @classmethod
    def validate_zipcode(cls, v: str) -> str:
        if not ZIP_RE.match(v):
            raise ValueError("zipcode must be 5 digits or ZIP+4")
        return v

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        digits = "".join(PHONE_DIGITS_RE.findall(v))
        if len(digits) < 10:
            raise ValueError("phone must have at least 10 digits")
        return v

    @field_validator("state")
    @classmethod
    def validate_state(cls, v: str) -> str:
        if not STATE_RE.match(v):
            raise ValueError("state must be a 2-letter uppercase code")
        return v