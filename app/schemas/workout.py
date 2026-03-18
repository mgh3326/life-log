from __future__ import annotations

import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class WorkoutCreate(BaseModel):
    date: datetime.date
    workout_type: list[str] = Field(..., min_length=1, examples=[["crossfit", "force"]])
    wod_program: str | None = None
    main_record: str | None = None
    duration_min: int | None = None
    calories: int | None = Field(None, ge=0)
    avg_hr: int | None = Field(None, ge=0, le=250)
    max_hr: int | None = Field(None, ge=0, le=250)
    distance_km: Decimal | None = None
    pre_meal: str | None = None
    memo: str | None = None
    is_rest_day: bool = False
    extra: dict | None = None


class WorkoutResponse(WorkoutCreate):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    model_config = {"from_attributes": True}


class WorkoutUpdate(BaseModel):
    workout_type: list[str] | None = None
    wod_program: str | None = None
    main_record: str | None = None
    duration_min: int | None = None
    calories: int | None = None
    avg_hr: int | None = None
    max_hr: int | None = None
    distance_km: Decimal | None = None
    pre_meal: str | None = None
    memo: str | None = None
    is_rest_day: bool | None = None
    extra: dict | None = None
