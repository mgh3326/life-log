from __future__ import annotations

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_coffee(client: AsyncClient):
    payload = {
        "bean_name": "Ethiopia Yirgacheffe",
        "dose_g": 20.0,
        "water_g": 300.0,
        "brew_method": "V60",
        "taste_rating": 4,
    }
    resp = await client.post("/api/coffee", json=payload)
    assert resp.status_code == 201
    data = resp.json()
    assert data["bean_name"] == "Ethiopia Yirgacheffe"
    assert data["brew_method"] == "V60"
    assert data["id"] is not None


@pytest.mark.asyncio
async def test_list_coffees(client: AsyncClient):
    for name in ["Ethiopia", "Colombia"]:
        await client.post("/api/coffee", json={"bean_name": name})
    resp = await client.get("/api/coffee")
    assert resp.status_code == 200
    assert len(resp.json()) == 2


@pytest.mark.asyncio
async def test_get_coffee(client: AsyncClient):
    create = await client.post("/api/coffee", json={"bean_name": "Kenya AA"})
    cid = create.json()["id"]
    resp = await client.get(f"/api/coffee/{cid}")
    assert resp.status_code == 200
    assert resp.json()["bean_name"] == "Kenya AA"


@pytest.mark.asyncio
async def test_update_coffee(client: AsyncClient):
    create = await client.post("/api/coffee", json={"bean_name": "Brazil"})
    cid = create.json()["id"]
    resp = await client.patch(f"/api/coffee/{cid}", json={"taste_rating": 5})
    assert resp.status_code == 200
    assert resp.json()["taste_rating"] == 5


@pytest.mark.asyncio
async def test_delete_coffee(client: AsyncClient):
    create = await client.post("/api/coffee", json={"bean_name": "Guatemala"})
    cid = create.json()["id"]
    resp = await client.delete(f"/api/coffee/{cid}")
    assert resp.status_code == 204
    get_resp = await client.get(f"/api/coffee/{cid}")
    assert get_resp.status_code == 404


@pytest.mark.asyncio
async def test_coffee_not_found(client: AsyncClient):
    resp = await client.get("/api/coffee/999")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_coffee_stats(client: AsyncClient):
    await client.post(
        "/api/coffee",
        json={"bean_name": "Ethiopia", "taste_rating": 4, "dose_g": 20.0},
    )
    await client.post(
        "/api/coffee",
        json={"bean_name": "Ethiopia", "taste_rating": 5, "dose_g": 18.0},
    )
    resp = await client.get("/api/coffee/stats?date_from=2026-01-01&date_to=2026-12-31")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total_brews"] == 2
    assert data["avg_rating"] == 4.5
    assert len(data["top_beans"]) >= 1
