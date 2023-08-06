import aioredis

from src.config import settings

redis = aioredis.from_url(
    settings.redis_url,
    encoding="utf-8",
    decode_responses=True,
    password=settings.REDIS_PASS,
)


async def get_redis_connection():
    yield redis
