from collections.abc import AsyncGenerator

from sqlalchemy.ext import asyncio
from sqlalchemy.pool import NullPool

from src.config import settings
from src.database import get_async_session
from src.main import app

pytest_plugins = [
    'tests.fixtures.fixture_database',
    'tests.fixtures.fixture_data',
]

engine_test = asyncio.create_async_engine(settings.db_test_url, poolclass=NullPool)
async_test_session_maker = asyncio.async_sessionmaker(
    bind=engine_test,
    expire_on_commit=False,
    class_=asyncio.AsyncSession,
)


async def override_get_async_session() -> AsyncGenerator[asyncio.AsyncSession, None]:
    async with async_test_session_maker() as session:
        yield session


app.dependency_overrides[get_async_session] = override_get_async_session
