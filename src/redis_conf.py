from collections.abc import AsyncIterator

import aioredis
from aioredis import Redis

from src.config import settings

redis = aioredis.from_url(
    settings.redis_url,
    encoding='utf-8',
    decode_responses=True,
    password=settings.REDIS_PASS,
)


async def get_redis_connection() -> AsyncIterator[Redis]:
    yield redis
