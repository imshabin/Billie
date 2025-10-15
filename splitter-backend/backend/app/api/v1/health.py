from fastapi import APIRouter
from backend.app.core.db import ping_db
from backend.app.core.redis import ping_redis

router = APIRouter()

@router.get("/healthz")
async def healthz():
    return {"status": "ok"}

@router.get("/readyz")
async def readyz():
    db_ok = await ping_db()
    redis_ok = ping_redis()
    return {"db": db_ok, "redis": redis_ok, "ready": db_ok and redis_ok}
