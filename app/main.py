from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.routers import coffee, health, workout


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    yield


def create_app() -> FastAPI:
    app = FastAPI(title="life-log", version="0.1.0", lifespan=lifespan)
    app.include_router(health.router)
    app.include_router(workout.router, prefix="/api")
    app.include_router(coffee.router, prefix="/api")
    return app


app = create_app()
