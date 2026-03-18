from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.schemas.coffee import CoffeeCreate, CoffeeResponse, CoffeeUpdate
from app.services import coffee_service

router = APIRouter(prefix="/coffee", tags=["coffee"])


@router.get("", response_model=list[CoffeeResponse])
async def list_coffees(
    date_from: date | None = None,
    date_to: date | None = None,
    limit: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
) -> list[CoffeeResponse]:
    return await coffee_service.get_coffees(db, date_from, date_to, limit=limit)


@router.get("/stats")
async def get_coffee_stats(
    date_from: date = Query(...),
    date_to: date = Query(...),
    db: AsyncSession = Depends(get_db),
) -> dict:
    return await coffee_service.get_coffee_stats(db, date_from, date_to)


@router.get("/{coffee_id}", response_model=CoffeeResponse)
async def get_coffee(
    coffee_id: int,
    db: AsyncSession = Depends(get_db),
) -> CoffeeResponse:
    coffee = await coffee_service.get_coffee(db, coffee_id)
    if coffee is None:
        raise HTTPException(status_code=404, detail="Coffee not found")
    return coffee


@router.post("", response_model=CoffeeResponse, status_code=201)
async def create_coffee(
    data: CoffeeCreate,
    db: AsyncSession = Depends(get_db),
) -> CoffeeResponse:
    return await coffee_service.create_coffee(db, data)


@router.patch("/{coffee_id}", response_model=CoffeeResponse)
async def update_coffee(
    coffee_id: int,
    data: CoffeeUpdate,
    db: AsyncSession = Depends(get_db),
) -> CoffeeResponse:
    return await coffee_service.update_coffee(db, coffee_id, data)


@router.delete("/{coffee_id}", status_code=204)
async def delete_coffee(
    coffee_id: int,
    db: AsyncSession = Depends(get_db),
) -> None:
    await coffee_service.delete_coffee(db, coffee_id)
