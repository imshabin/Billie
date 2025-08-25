import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_healthz():
    # New way: use ASGITransport with your FastAPI app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        r = await ac.get("/v1/healthz")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"
