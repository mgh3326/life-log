from __future__ import annotations

import datetime

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health(client: AsyncClient):
    resp = await client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok", "service": "life-log"}


@pytest.mark.asyncio
async def test_create_workout(client: AsyncClient):
    payload = {
        "date": "2026-03-18",
        "workout_type": ["crossfit", "force"],
        "calories": 350,
        "duration_min": 60,
    }
    resp = await client.post("/api/workouts", json=payload)
    assert resp.status_code == 201
    data = resp.json()
    assert data["date"] == "2026-03-18"
    assert data["workout_type"] == ["crossfit", "force"]
    assert data["calories"] == 350
    assert data["id"] is not None


@pytest.mark.asyncio
async def test_list_workouts(client: AsyncClient):
    for i in range(2):
        await client.post(
            "/api/workouts",
            json={"date": f"2026-03-1{i + 1}", "workout_type": ["running"]},
        )
    resp = await client.get("/api/workouts")
    assert resp.status_code == 200
    assert len(resp.json()) == 2


@pytest.mark.asyncio
async def test_get_workout(client: AsyncClient):
    create = await client.post(
        "/api/workouts",
        json={"date": "2026-03-18", "workout_type": ["crossfit"]},
    )
    wid = create.json()["id"]
    resp = await client.get(f"/api/workouts/{wid}")
    assert resp.status_code == 200
    assert resp.json()["id"] == wid


@pytest.mark.asyncio
async def test_update_workout(client: AsyncClient):
    create = await client.post(
        "/api/workouts",
        json={"date": "2026-03-18", "workout_type": ["crossfit"]},
    )
    wid = create.json()["id"]
    resp = await client.patch(f"/api/workouts/{wid}", json={"memo": "great session"})
    assert resp.status_code == 200
    assert resp.json()["memo"] == "great session"


@pytest.mark.asyncio
async def test_delete_workout(client: AsyncClient):
    create = await client.post(
        "/api/workouts",
        json={"date": "2026-03-18", "workout_type": ["crossfit"]},
    )
    wid = create.json()["id"]
    resp = await client.delete(f"/api/workouts/{wid}")
    assert resp.status_code == 204
    get_resp = await client.get(f"/api/workouts/{wid}")
    assert get_resp.status_code == 404


@pytest.mark.asyncio
async def test_workout_not_found(client: AsyncClient):
    resp = await client.get("/api/workouts/999")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_check_workout_exists(client: AsyncClient):
    await client.post(
        "/api/workouts",
        json={"date": "2026-03-18", "workout_type": ["crossfit"]},
    )
    resp = await client.get("/api/workouts/check/2026-03-18")
    assert resp.status_code == 200
    data = resp.json()
    assert data["exists"] is True
    assert data["count"] >= 1


@pytest.mark.asyncio
async def test_check_workout_not_exists(client: AsyncClient):
    resp = await client.get("/api/workouts/check/2020-01-01")
    assert resp.status_code == 200
    data = resp.json()
    assert data["exists"] is False
    assert data["count"] == 0


@pytest.mark.asyncio
async def test_streak(client: AsyncClient):
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    for d in [yesterday, today]:
        await client.post(
            "/api/workouts",
            json={"date": d.isoformat(), "workout_type": ["crossfit"]},
        )
    resp = await client.get("/api/workouts/streak")
    assert resp.status_code == 200
    data = resp.json()
    assert data["current_streak"] == 2
    assert data["longest_streak"] == 2
