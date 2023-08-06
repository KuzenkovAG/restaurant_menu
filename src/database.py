from collections.abc import AsyncGenerator

from sqlalchemy.ext import asyncio
from sqlalchemy.orm import DeclarativeBase

from .config import settings

engine = asyncio.create_async_engine(settings.db_url)
async_session_maker = asyncio.async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_async_session() -> AsyncGenerator[asyncio.AsyncSession, None]:
    """Create async session."""
    async with async_session_maker() as session:
        yield session
