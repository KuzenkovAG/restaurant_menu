import json
from typing import Annotated, TypeVar

from aioredis import Redis
from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from src.redis_conf import get_redis_connection

T_Schema = TypeVar('T_Schema', bound=BaseModel)


class Cache:
    """Manager of cache."""

    def __init__(self, redis: Redis):
        self.redis = redis

    async def get(self, key: str) -> dict | list | None:
        """Get cache."""
        result = await self.redis.get(key)
        return json.loads(result) if result else None

    async def set(self, key: str, value: T_Schema | list[T_Schema]) -> None:
        """Set cache."""
        await self.redis.set(key, json.dumps(jsonable_encoder(value)))

    async def clear(self, key: str, *keys: str) -> None:
        """Clear cache for key/keys."""
        await self.redis.delete(key, *keys)

    async def clear_by_mask(self, key_mask: str) -> None:
        """Clear cache for all keys what contain mask."""
        keys = await self.redis.keys(f'{key_mask}*')
        if keys:
            await self.clear(*keys)


def get_cache(redis: Annotated[Redis, Depends(get_redis_connection)]):
    return Cache(redis=redis)
