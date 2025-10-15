# backend/app/core/db.py
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)
from sqlalchemy import text
from backend.app.core.config import settings

# 1) Build the async Postgres URL (asyncpg driver)

from sqlalchemy.orm import declarative_base

Base = declarative_base()


DATABASE_URL = (
    f"postgresql+asyncpg://{settings.db_user}:{settings.db_password}"
    f"@{settings.db_host}:{settings.db_port}/{settings.db_name}"
)


# 2) Create a single process-wide async engine (connection pool inside)
engine = create_async_engine(
    DATABASE_URL,
    pool_pre_ping=True,          # auto-detect dead connections
    pool_size=5,                 # sensible default for dev
    max_overflow=5,              # allow short bursts
)

# 3) Session factory for request-scoped DB sessions (you’ll use this later)
SessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

# 4) Lightweight health check
async def ping_db() -> bool:
    """
    Returns True if the DB responds to a trivial SELECT 1.
    Used by /readyz.
    """
    try:
        async with engine.connect() as conn:
            val = await conn.scalar(text("SELECT 1"))
            return val == 1
    except Exception:
        return False
