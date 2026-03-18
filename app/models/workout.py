from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import (
    ARRAY,
    TIMESTAMP,
    Boolean,
    CheckConstraint,
    Date,
    Integer,
    Numeric,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class WorkoutLog(Base):
    __tablename__ = "workout_logs"
    __table_args__ = (
        CheckConstraint("calories >= 0", name="workout_logs_calories_positive"),
        CheckConstraint(
            "avg_hr >= 0 AND avg_hr <= 250", name="workout_logs_avg_hr_range"
        ),
        CheckConstraint(
            "max_hr >= 0 AND max_hr <= 250", name="workout_logs_max_hr_range"
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    workout_type: Mapped[list[str]] = mapped_column(ARRAY(Text), nullable=False)
    wod_program: Mapped[str | None] = mapped_column(Text, nullable=True)
    main_record: Mapped[str | None] = mapped_column(Text, nullable=True)
    duration_min: Mapped[int | None] = mapped_column(Integer, nullable=True)
    calories: Mapped[int | None] = mapped_column(Integer, nullable=True)
    avg_hr: Mapped[int | None] = mapped_column(Integer, nullable=True)
    max_hr: Mapped[int | None] = mapped_column(Integer, nullable=True)
    distance_km: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True)
    pre_meal: Mapped[str | None] = mapped_column(Text, nullable=True)
    memo: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_rest_day: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    extra: Mapped[dict | None] = mapped_column(JSONB, nullable=True, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
