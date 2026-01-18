# tests/api/test_chats.py
import pytest
from unittest.mock import AsyncMock
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport
from datetime import datetime, timezone

from src.domain.exceptions import ChatNotFound, ValidationError
from src.api.dependencies import get_chat_service, get_message_service


@pytest.mark.anyio
async def test_create_chat_success(app):
    mock_service = AsyncMock()
    mock_service.create_chat.return_value = {
        "id": 1,
        "title": "Test chat",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    app.dependency_overrides[get_chat_service] = lambda: mock_service

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        response = await client.post("/chats/", json={"title": "Test chat"})

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test chat"
    assert "created_at" in data
    mock_service.create_chat.assert_awaited_once()
    app.dependency_overrides.clear()


@pytest.mark.anyio
async def test_create_chat_validation_error(app):
    mock_service = AsyncMock()
    mock_service.create_chat.side_effect = ValidationError("Invalid data")

    app.dependency_overrides[get_chat_service] = lambda: mock_service

    # Передаем валидный JSON, чтобы Pydantic не кидал 422
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        response = await client.post("/chats/", json={"title": "Valid title"})

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid data"
    app.dependency_overrides.clear()


@pytest.mark.anyio
async def test_send_message_success(app):
    mock_service = AsyncMock()
    mock_service.send_message.return_value = {
        "id": 1,
        "chat_id": 1,
        "text": "Hello",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    app.dependency_overrides[get_message_service] = lambda: mock_service

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        response = await client.post("/chats/1/messages/", json={"text": "Hello"})

    assert response.status_code == 201
    data = response.json()
    assert data["text"] == "Hello"
    assert "created_at" in data
    app.dependency_overrides.clear()


@pytest.mark.anyio
async def test_send_message_chat_not_found(app):
    mock_service = AsyncMock()
    mock_service.send_message.side_effect = ChatNotFound()

    app.dependency_overrides[get_message_service] = lambda: mock_service

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        response = await client.post("/chats/999/messages/", json={"text": "Hello"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Chat not found"
    app.dependency_overrides.clear()


@pytest.mark.anyio
async def test_get_chat_success(app):
    mock_service = AsyncMock()
    mock_service.get_chat.return_value = (
        {"id": 1, "title": "Chat", "created_at": datetime.now(timezone.utc).isoformat()},
        [
            {"id": 1, "chat_id": 1, "text": "Hi", "created_at": datetime.now(timezone.utc).isoformat()}
        ],
    )

    app.dependency_overrides[get_chat_service] = lambda: mock_service

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        response = await client.get("/chats/1?limit=10")

    assert response.status_code == 200
    data = response.json()
    assert data["chat"]["id"] == 1
    assert len(data["messages"]) == 1
    assert "created_at" in data["chat"]
    assert "created_at" in data["messages"][0]
    app.dependency_overrides.clear()


@pytest.mark.anyio
async def test_get_chat_not_found(app):
    mock_service = AsyncMock()
    mock_service.get_chat.side_effect = ChatNotFound()

    app.dependency_overrides[get_chat_service] = lambda: mock_service

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        response = await client.get("/chats/999")

    assert response.status_code == 404
    app.dependency_overrides.clear()


@pytest.mark.anyio
async def test_delete_chat_success(app):
    mock_service = AsyncMock()
    mock_service.delete_chat.return_value = None

    app.dependency_overrides[get_chat_service] = lambda: mock_service

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        response = await client.delete("/chats/1")

    assert response.status_code == 204
    app.dependency_overrides.clear()


@pytest.mark.anyio
async def test_delete_chat_not_found(app):
    mock_service = AsyncMock()
    mock_service.delete_chat.side_effect = ChatNotFound()

    app.dependency_overrides[get_chat_service] = lambda: mock_service

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        response = await client.delete("/chats/999")

    assert response.status_code == 404
    app.dependency_overrides.clear()
