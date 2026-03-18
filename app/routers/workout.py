from datetime import date, timedelta

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.schemas.workout import WorkoutCreate, WorkoutResponse, WorkoutUpdate
from app.services import workout_service

router = APIRouter(prefix="/workouts", tags=["workouts"])


@router.get("", response_model=list[WorkoutResponse])
async def list_workouts(
    date_from: date | None = None,
    date_to: date | None = None,
    limit: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
) -> list[WorkoutResponse]:
    return await workout_service.get_workouts(db, date_from, date_to, limit=limit)


@router.get("/streak")
async def get_streak(db: AsyncSession = Depends(get_db)) -> dict:
    return await workout_service.get_streak(db)


@router.get("/missing")
async def get_missing_dates(
    date_from: date = Query(...),
    date_to: date = Query(...),
    db: AsyncSession = Depends(get_db),
) -> dict:
    dates = await workout_service.get_missing_dates(db, date_from, date_to)
    return {"dates": dates}


@router.get("/report/weekly")
async def get_weekly_report(
    week_start: date | None = None,
    db: AsyncSession = Depends(get_db),
) -> dict:
    if week_start is None:
        today = date.today()
        week_start = today - timedelta(days=today.weekday())
    return await workout_service.get_weekly_report(db, week_start)


@router.get("/check/{date}")
async def check_workout(
    date: date,
    db: AsyncSession = Depends(get_db),
) -> dict:
    workouts = await workout_service.get_workout_by_date(db, date)
    return {"exists": len(workouts) > 0, "count": len(workouts)}


@router.get("/{workout_id}", response_model=WorkoutResponse)
async def get_workout(
    workout_id: int,
    db: AsyncSession = Depends(get_db),
) -> WorkoutResponse:
    workout = await workout_service.get_workout(db, workout_id)
    if workout is None:
        raise HTTPException(status_code=404, detail="Workout not found")
    return workout


@router.post("", response_model=WorkoutResponse, status_code=201)
async def create_workout(
    data: WorkoutCreate,
    db: AsyncSession = Depends(get_db),
) -> WorkoutResponse:
    return await workout_service.create_workout(db, data)


@router.patch("/{workout_id}", response_model=WorkoutResponse)
async def update_workout(
    workout_id: int,
    data: WorkoutUpdate,
    db: AsyncSession = Depends(get_db),
) -> WorkoutResponse:
    return await workout_service.update_workout(db, workout_id, data)


@router.delete("/{workout_id}", status_code=204)
async def delete_workout(
    workout_id: int,
    db: AsyncSession = Depends(get_db),
) -> None:
    await workout_service.delete_workout(db, workout_id)
