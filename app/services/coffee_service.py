from __future__ import annotations

from datetime import date

from fastapi import HTTPException
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.coffee import CoffeeLog
from app.schemas.coffee import CoffeeCreate, CoffeeUpdate


async def create_coffee(db: AsyncSession, data: CoffeeCreate) -> CoffeeLog:
    values = data.model_dump()
    if values.get("date") is None:
        values["date"] = date.today()
    coffee = CoffeeLog(**values)
    db.add(coffee)
    await db.commit()
    await db.refresh(coffee)
    return coffee


async def get_coffee(db: AsyncSession, coffee_id: int) -> CoffeeLog | None:
    result = await db.execute(select(CoffeeLog).where(CoffeeLog.id == coffee_id))
    return result.scalar_one_or_none()


async def get_coffees(
    db: AsyncSession,
    date_from: date | None = None,
    date_to: date | None = None,
    limit: int = 50,
) -> list[CoffeeLog]:
    stmt = select(CoffeeLog)
    if date_from is not None:
        stmt = stmt.where(CoffeeLog.date >= date_from)
    if date_to is not None:
        stmt = stmt.where(CoffeeLog.date <= date_to)
    stmt = stmt.order_by(CoffeeLog.date.desc()).limit(limit)
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def update_coffee(
    db: AsyncSession, coffee_id: int, data: CoffeeUpdate
) -> CoffeeLog:
    coffee = await get_coffee(db, coffee_id)
    if coffee is None:
        raise HTTPException(status_code=404, detail="Coffee log not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(coffee, key, value)
    await db.commit()
    await db.refresh(coffee)
    return coffee


async def delete_coffee(db: AsyncSession, coffee_id: int) -> None:
    coffee = await get_coffee(db, coffee_id)
    if coffee is None:
        raise HTTPException(status_code=404, detail="Coffee log not found")
    await db.delete(coffee)
    await db.commit()


async def get_coffee_stats(db: AsyncSession, date_from: date, date_to: date) -> dict:
    """Aggregate coffee stats for the given date range."""
    base_filter = [CoffeeLog.date >= date_from, CoffeeLog.date <= date_to]

    # total brews + avg rating + avg dose in a single query
    agg_stmt = select(
        func.count(CoffeeLog.id).label("total_brews"),
        func.avg(CoffeeLog.taste_rating).label("avg_rating"),
        func.avg(CoffeeLog.dose_g).label("avg_dose_g"),
    ).where(*base_filter)
    agg_result = await db.execute(agg_stmt)
    agg_row = agg_result.one()

    total_brews: int = agg_row.total_brews or 0
    avg_rating = round(float(agg_row.avg_rating), 2) if agg_row.avg_rating else None
    avg_dose_g = round(float(agg_row.avg_dose_g), 1) if agg_row.avg_dose_g else None

    # top beans
    beans_stmt = (
        select(
            CoffeeLog.bean_name,
            func.count(CoffeeLog.id).label("cnt"),
        )
        .where(*base_filter)
        .group_by(CoffeeLog.bean_name)
        .order_by(func.count(CoffeeLog.id).desc())
        .limit(5)
    )
    beans_result = await db.execute(beans_stmt)
    top_beans = [
        {"bean_name": row.bean_name, "count": row.cnt} for row in beans_result.all()
    ]

    return {
        "total_brews": total_brews,
        "avg_rating": avg_rating,
        "top_beans": top_beans,
        "avg_dose_g": avg_dose_g,
    }
