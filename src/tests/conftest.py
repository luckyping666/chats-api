from typing import AsyncGenerator
import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from src.api.routers.chats_router import router

@pytest.fixture
def app() -> FastAPI:
    app = FastAPI()
    app.include_router(router)
    return app

@pytest.fixture
async def client(app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    """
    Асинхронный fixture для HTTP-клиента.
    Возвращаем AsyncGenerator[AsyncClient, None] для корректной типизации.
    """
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
