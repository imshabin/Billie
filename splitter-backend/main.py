from fastapi import FastAPI
from backend.app.core.config import settings
from backend.app.api.v1.health import router as health_router
from backend.app.auth.router import router as auth_router
from backend.app.core.db import engine
from backend.app.models import user

app = FastAPI(title="Splitter API", version="0.1.0")

# ✅ Create tables asynchronously on startup
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(user.Base.metadata.create_all)

# Routers
app.include_router(health_router, prefix="/v1")
app.include_router(auth_router, prefix="/auth", tags=["authentication"])

@app.get("/")
def root():
    return {"service": "splitter-api", "env": settings.app_env}
