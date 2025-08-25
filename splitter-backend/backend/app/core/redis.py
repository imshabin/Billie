# backend/app/core/redis.py
import redis
from app.core.config import settings

# 1) Create a single process-wide Redis client
# decode_responses=True gives you str instead of bytes
r = redis.Redis(
    host=settings.redis_host,
    port=settings.redis_port,
    socket_connect_timeout=1.5,  # fail fast on health checks
    socket_timeout=1.5,
    decode_responses=True,
)

def ping_redis() -> bool:
    """
    Returns True if Redis responds to PING.
    Used by /readyz.
    """
    try:
        return bool(r.ping())
    except Exception:
        return False
