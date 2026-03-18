from __future__ import annotations

import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class CoffeeCreate(BaseModel):
    date: datetime.date | None = None
    bean_name: str
    bean_origin: str | None = None
    roast_level: str | None = None
    grind_setting: str | None = None
    dose_g: Decimal | None = None
    water_g: Decimal | None = None
    water_temp: int | None = Field(None, ge=0, le=100)
    brew_time_sec: int | None = Field(None, ge=0)
    brew_method: str | None = None
    taste_rating: int | None = Field(None, ge=1, le=5)
    taste_notes: str | None = None
    bed_photo_path: str | None = None
    extra: dict | None = None


class CoffeeResponse(CoffeeCreate):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    model_config = {"from_attributes": True}


class CoffeeUpdate(BaseModel):
    bean_name: str | None = None
    bean_origin: str | None = None
    roast_level: str | None = None
    grind_setting: str | None = None
    dose_g: Decimal | None = None
    water_g: Decimal | None = None
    water_temp: int | None = None
    brew_time_sec: int | None = None
    brew_method: str | None = None
    taste_rating: int | None = None
    taste_notes: str | None = None
    bed_photo_path: str | None = None
    extra: dict | None = None
