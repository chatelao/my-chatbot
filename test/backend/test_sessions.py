import pytest
import httpx
from fastapi.testclient import TestClient
from httpx import AsyncClient
from src.backend.main import app
from src.backend.database import init_db
import os

@pytest.fixture
def api_key():
    return os.getenv("APP_API_KEY", "dev-key")

@pytest.mark.asyncio
async def test_session_lifecycle(api_key):
    await init_db()
    async with AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
        # 1. Create a session
        response = await ac.post(
            "/api/sessions",
            headers={"X-App-Api-Key": api_key}
        )
        assert response.status_code == 200
        session_data = response.json()
        session_id = session_data["id"]
        assert "id" in session_data
        assert session_data["messages"] == []

        # 2. Get the session
        response = await ac.get(
            f"/api/sessions/{session_id}",
            headers={"X-App-Api-Key": api_key}
        )
        assert response.status_code == 200
        assert response.json()["id"] == session_id

        # 3. List sessions
        response = await ac.get(
            "/api/sessions",
            headers={"X-App-Api-Key": api_key}
        )
        assert response.status_code == 200
        sessions = response.json()
        assert any(s["id"] == session_id for s in sessions)

@pytest.mark.asyncio
async def test_get_nonexistent_session(api_key):
    await init_db()
    async with AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get(
            "/api/sessions/nonexistent",
            headers={"X-App-Api-Key": api_key}
        )
        assert response.status_code == 404
