from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from src.database import get_async_session
from src.config import settings
from src.main import app

pytest_plugins = [
    'tests.fixtures.fixture_database',
    'tests.fixtures.fixture_data'
]

engine_test = create_async_engine(settings.DB_TEST_URL, poolclass=NullPool)
async_test_session_maker = sessionmaker(
    bind=engine_test,
    expire_on_commit=False,
    class_=AsyncSession,
)


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_test_session_maker() as session:
        yield session

app.dependency_overrides[get_async_session] = override_get_async_session
