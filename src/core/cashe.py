import json
from typing import TypeVar

from aioredis import Redis
from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from src.redis_conf import get_redis_connection

T_Schema = TypeVar('T_Schema', bound=BaseModel)


class Cache:
    """Manager of cache."""

    def __init__(self, redis: Redis = Depends(get_redis_connection)):
        self.redis = redis

    async def get(self, key: str) -> dict | list | None:
        """Get cache."""
        result = await self.redis.get(key)
        return json.loads(result) if result else None

    async def set(self, key: str, value: T_Schema | list[T_Schema]) -> None:
        """Set cache."""
        await self.redis.set(key, json.dumps(jsonable_encoder(value)))

    async def clear(self, key: str, *keys: str) -> None:
        """Delete cache."""
        await self.redis.delete(key, *keys)
