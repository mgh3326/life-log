from __future__ import annotations

from datetime import date as date_module
from datetime import timedelta
from decimal import Decimal

from fastmcp import FastMCP

from app.core.db import AsyncSessionLocal
from app.schemas.coffee import CoffeeCreate
from app.schemas.workout import WorkoutCreate
from app.services import coffee_service, workout_service


def _workout_to_dict(w) -> dict:
    return {
        "id": w.id,
        "date": str(w.date),
        "workout_type": w.workout_type,
        "wod_program": w.wod_program,
        "main_record": w.main_record,
        "duration_min": w.duration_min,
        "calories": w.calories,
        "avg_hr": w.avg_hr,
        "max_hr": w.max_hr,
        "distance_km": float(w.distance_km) if w.distance_km is not None else None,
        "pre_meal": w.pre_meal,
        "memo": w.memo,
        "is_rest_day": w.is_rest_day,
    }


def _coffee_to_dict(c) -> dict:
    return {
        "id": c.id,
        "date": str(c.date),
        "bean_name": c.bean_name,
        "bean_origin": c.bean_origin,
        "roast_level": c.roast_level,
        "grind_setting": c.grind_setting,
        "dose_g": float(c.dose_g) if c.dose_g is not None else None,
        "water_g": float(c.water_g) if c.water_g is not None else None,
        "water_temp": c.water_temp,
        "brew_time_sec": c.brew_time_sec,
        "brew_method": c.brew_method,
        "taste_rating": c.taste_rating,
        "taste_notes": c.taste_notes,
    }


def register_all_tools(mcp: FastMCP) -> None:
    @mcp.tool()
    async def save_workout(
        date: str,
        workout_type: list[str],
        wod_program: str | None = None,
        main_record: str | None = None,
        duration_min: int | None = None,
        calories: int | None = None,
        avg_hr: int | None = None,
        max_hr: int | None = None,
        distance_km: float | None = None,
        pre_meal: str | None = None,
        memo: str | None = None,
        is_rest_day: bool = False,
    ) -> dict:
        """Save a workout log entry. For rest days, set workout_type=['rest'] and is_rest_day=True."""
        try:
            parsed_date = date_module.fromisoformat(date)
            data = WorkoutCreate(
                date=parsed_date,
                workout_type=workout_type,
                wod_program=wod_program,
                main_record=main_record,
                duration_min=duration_min,
                calories=calories,
                avg_hr=avg_hr,
                max_hr=max_hr,
                distance_km=Decimal(str(distance_km))
                if distance_km is not None
                else None,
                pre_meal=pre_meal,
                memo=memo,
                is_rest_day=is_rest_day,
            )
            async with AsyncSessionLocal() as db:
                result = await workout_service.create_workout(db, data)
                return {"status": "saved", "id": result.id, "date": str(result.date)}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @mcp.tool()
    async def save_coffee(
        bean_name: str,
        date: str | None = None,
        bean_origin: str | None = None,
        roast_level: str | None = None,
        grind_setting: str | None = None,
        dose_g: float | None = None,
        water_g: float | None = None,
        water_temp: int | None = None,
        brew_time_sec: int | None = None,
        brew_method: str | None = None,
        taste_rating: int | None = None,
        taste_notes: str | None = None,
    ) -> dict:
        """Save a coffee brew log entry."""
        try:
            parsed_date = date_module.fromisoformat(date) if date else None
            data = CoffeeCreate(
                date=parsed_date,
                bean_name=bean_name,
                bean_origin=bean_origin,
                roast_level=roast_level,
                grind_setting=grind_setting,
                dose_g=Decimal(str(dose_g)) if dose_g is not None else None,
                water_g=Decimal(str(water_g)) if water_g is not None else None,
                water_temp=water_temp,
                brew_time_sec=brew_time_sec,
                brew_method=brew_method,
                taste_rating=taste_rating,
                taste_notes=taste_notes,
            )
            async with AsyncSessionLocal() as db:
                result = await coffee_service.create_coffee(db, data)
                return {"status": "saved", "id": result.id, "date": str(result.date)}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @mcp.tool()
    async def get_logs(
        category: str,
        date_from: str | None = None,
        date_to: str | None = None,
    ) -> dict:
        """Get workout or coffee logs. category: 'workout' or 'coffee'."""
        try:
            parsed_from = date_module.fromisoformat(date_from) if date_from else None
            parsed_to = date_module.fromisoformat(date_to) if date_to else None

            async with AsyncSessionLocal() as db:
                if category == "workout":
                    rows = await workout_service.get_workouts(
                        db, parsed_from, parsed_to
                    )
                    return {
                        "logs": [_workout_to_dict(r) for r in rows],
                        "count": len(rows),
                    }
                elif category == "coffee":
                    rows = await coffee_service.get_coffees(db, parsed_from, parsed_to)
                    return {
                        "logs": [_coffee_to_dict(r) for r in rows],
                        "count": len(rows),
                    }
                else:
                    return {
                        "status": "error",
                        "message": f"Unknown category: {category}. Use 'workout' or 'coffee'.",
                    }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @mcp.tool()
    async def get_streak() -> dict:
        """Get workout streak info: current consecutive days, longest streak, last logged date."""
        try:
            async with AsyncSessionLocal() as db:
                return await workout_service.get_streak(db)
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @mcp.tool()
    async def get_weekly_report(week_start: str | None = None) -> dict:
        """Get weekly workout report. Defaults to current week."""
        try:
            if week_start:
                parsed_start = date_module.fromisoformat(week_start)
            else:
                today = date_module.today()
                parsed_start = today - timedelta(days=today.weekday())
            async with AsyncSessionLocal() as db:
                return await workout_service.get_weekly_report(db, parsed_start)
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @mcp.tool()
    async def get_missing_dates(days: int = 7) -> dict:
        """Get dates with no workout log in the last N days. Used for nudge reminders."""
        try:
            today = date_module.today()
            date_from = today - timedelta(days=days)
            date_to = today
            async with AsyncSessionLocal() as db:
                dates = await workout_service.get_missing_dates(db, date_from, date_to)
                return {"missing_dates": [str(d) for d in dates], "count": len(dates)}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @mcp.tool()
    async def save_rest_day(
        date: str | None = None,
        memo: str | None = None,
    ) -> dict:
        """Quick save a rest day. Shortcut for saving workout with is_rest_day=True."""
        try:
            parsed_date = (
                date_module.fromisoformat(date) if date else date_module.today()
            )
            data = WorkoutCreate(
                date=parsed_date,
                workout_type=["rest"],
                is_rest_day=True,
                memo=memo,
            )
            async with AsyncSessionLocal() as db:
                result = await workout_service.create_workout(db, data)
                return {"status": "saved", "id": result.id, "date": str(result.date)}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @mcp.tool()
    async def get_coffee_stats(days: int = 30) -> dict:
        """Get coffee brewing statistics for the last N days."""
        try:
            today = date_module.today()
            date_from = today - timedelta(days=days)
            date_to = today
            async with AsyncSessionLocal() as db:
                return await coffee_service.get_coffee_stats(db, date_from, date_to)
        except Exception as e:
            return {"status": "error", "message": str(e)}
