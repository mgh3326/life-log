from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import (
    TIMESTAMP,
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


class CoffeeLog(Base):
    __tablename__ = "coffee_logs"
    __table_args__ = (
        CheckConstraint(
            "taste_rating >= 1 AND taste_rating <= 5",
            name="coffee_logs_taste_rating_range",
        ),
        CheckConstraint(
            "water_temp >= 0 AND water_temp <= 100",
            name="coffee_logs_water_temp_range",
        ),
        CheckConstraint("brew_time_sec >= 0", name="coffee_logs_brew_time_positive"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date: Mapped[date] = mapped_column(
        Date, nullable=False, index=True, default=date.today
    )
    bean_name: Mapped[str] = mapped_column(Text, nullable=False)
    bean_origin: Mapped[str | None] = mapped_column(Text, nullable=True)
    roast_level: Mapped[str | None] = mapped_column(Text, nullable=True)
    grind_setting: Mapped[str | None] = mapped_column(Text, nullable=True)
    dose_g: Mapped[Decimal | None] = mapped_column(Numeric(4, 1), nullable=True)
    water_g: Mapped[Decimal | None] = mapped_column(Numeric(5, 1), nullable=True)
    water_temp: Mapped[int | None] = mapped_column(Integer, nullable=True)
    brew_time_sec: Mapped[int | None] = mapped_column(Integer, nullable=True)
    brew_method: Mapped[str | None] = mapped_column(Text, nullable=True)
    taste_rating: Mapped[int | None] = mapped_column(Integer, nullable=True)
    taste_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    bed_photo_path: Mapped[str | None] = mapped_column(Text, nullable=True)
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
