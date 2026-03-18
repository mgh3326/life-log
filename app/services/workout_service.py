from __future__ import annotations

from datetime import date, timedelta

from fastapi import HTTPException
from sqlalchemy import distinct, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.workout import WorkoutLog
from app.schemas.workout import WorkoutCreate, WorkoutUpdate


async def create_workout(db: AsyncSession, data: WorkoutCreate) -> WorkoutLog:
    workout = WorkoutLog(**data.model_dump())
    db.add(workout)
    await db.commit()
    await db.refresh(workout)
    return workout


async def get_workout(db: AsyncSession, workout_id: int) -> WorkoutLog | None:
    result = await db.execute(select(WorkoutLog).where(WorkoutLog.id == workout_id))
    return result.scalar_one_or_none()


async def get_workouts(
    db: AsyncSession,
    date_from: date | None = None,
    date_to: date | None = None,
    limit: int = 50,
) -> list[WorkoutLog]:
    stmt = select(WorkoutLog)
    if date_from is not None:
        stmt = stmt.where(WorkoutLog.date >= date_from)
    if date_to is not None:
        stmt = stmt.where(WorkoutLog.date <= date_to)
    stmt = stmt.order_by(WorkoutLog.date.desc()).limit(limit)
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def get_workout_by_date(db: AsyncSession, target_date: date) -> list[WorkoutLog]:
    stmt = (
        select(WorkoutLog).where(WorkoutLog.date == target_date).order_by(WorkoutLog.id)
    )
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def update_workout(
    db: AsyncSession, workout_id: int, data: WorkoutUpdate
) -> WorkoutLog:
    workout = await get_workout(db, workout_id)
    if workout is None:
        raise HTTPException(status_code=404, detail="Workout not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(workout, key, value)
    await db.commit()
    await db.refresh(workout)
    return workout


async def delete_workout(db: AsyncSession, workout_id: int) -> None:
    workout = await get_workout(db, workout_id)
    if workout is None:
        raise HTTPException(status_code=404, detail="Workout not found")
    await db.delete(workout)
    await db.commit()


async def get_streak(db: AsyncSession) -> dict:
    """Calculate current and longest consecutive workout day streaks.

    A day counts if ANY record exists for that date (including rest days).
    """
    stmt = select(distinct(WorkoutLog.date)).order_by(WorkoutLog.date.desc())
    result = await db.execute(stmt)
    logged_dates: list[date] = sorted(result.scalars().all(), reverse=True)

    if not logged_dates:
        return {"current_streak": 0, "longest_streak": 0, "last_logged": None}

    # --- current streak (count backwards from most recent logged date) ---
    current_streak = 1
    for i in range(1, len(logged_dates)):
        if logged_dates[i - 1] - logged_dates[i] == timedelta(days=1):
            current_streak += 1
        else:
            break

    # Check if the streak is still "active" (last logged is today or yesterday)
    today = date.today()
    if logged_dates[0] < today - timedelta(days=1):
        current_streak = 0

    # --- longest streak ever ---
    longest_streak = 1
    running = 1
    for i in range(1, len(logged_dates)):
        if logged_dates[i - 1] - logged_dates[i] == timedelta(days=1):
            running += 1
        else:
            running = 1
        longest_streak = max(longest_streak, running)

    return {
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "last_logged": logged_dates[0].isoformat(),
    }


async def get_missing_dates(
    db: AsyncSession, date_from: date, date_to: date
) -> list[date]:
    """Return dates in range with NO workout_logs record at all."""
    stmt = select(distinct(WorkoutLog.date)).where(
        WorkoutLog.date >= date_from, WorkoutLog.date <= date_to
    )
    result = await db.execute(stmt)
    logged: set[date] = set(result.scalars().all())

    all_dates: list[date] = []
    current = date_from
    while current <= date_to:
        all_dates.append(current)
        current += timedelta(days=1)

    return [d for d in all_dates if d not in logged]


async def get_weekly_report(db: AsyncSession, week_start: date) -> dict:
    """Generate a 7-day report starting from week_start."""
    week_end = week_start + timedelta(days=6)

    stmt = select(WorkoutLog).where(
        WorkoutLog.date >= week_start,
        WorkoutLog.date <= week_end,
    )
    result = await db.execute(stmt)
    rows: list[WorkoutLog] = list(result.scalars().all())

    logged_dates: set[date] = set()
    rest_days = 0
    workout_types: dict[str, int] = {}
    total_calories: int = 0
    total_duration: int = 0
    has_calories = False
    has_duration = False

    for row in rows:
        logged_dates.add(row.date)
        if row.is_rest_day:
            rest_days += 1
        if row.workout_type:
            for wt in row.workout_type:
                workout_types[wt] = workout_types.get(wt, 0) + 1
        if row.calories is not None:
            total_calories += row.calories
            has_calories = True
        if row.duration_min is not None:
            total_duration += row.duration_min
            has_duration = True

    return {
        "week_start": week_start.isoformat(),
        "total_days": len(logged_dates),
        "rest_days": rest_days,
        "workout_types": workout_types,
        "total_calories": total_calories if has_calories else None,
        "total_duration_min": total_duration if has_duration else None,
    }
