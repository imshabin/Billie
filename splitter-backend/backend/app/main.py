from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.health import router as health_router

app = FastAPI(title="Splitter API", version="0.1.0")
app.include_router(health_router, prefix="/v1")

@app.get("/")
def root():
    return {"service": "splitter-api", "env": settings.app_env}
