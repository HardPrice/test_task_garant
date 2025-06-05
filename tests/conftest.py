from typing import AsyncGenerator, Generator
import pytest
import pytest_asyncio
import httpx
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import close_all_sessions
from sqlalchemy.sql import text
from app.models.models import Base
from app.database.database import get_session
from app.main import app
import asyncio
import logging

logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

TEST_DATABASE_URL = "postgresql+asyncpg://postgres:nikita22335@localhost:5432/posts_test_db"

@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()

test_engine = create_async_engine(
    TEST_DATABASE_URL,
    isolation_level="READ COMMITTED",
    echo=True,
    pool_pre_ping=True,
    pool_size=5
)

test_async_session = async_sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

@pytest_asyncio.fixture(autouse=True)
async def setup_database() -> AsyncGenerator[None, None]:
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    await test_engine.dispose()

@pytest_asyncio.fixture
async def test_session() -> AsyncGenerator[AsyncSession, None]:
    async with test_async_session() as session:
        yield session
        await session.close()

@pytest_asyncio.fixture
async def client(test_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    app.dependency_overrides[get_session] = lambda: test_session
    transport = httpx.ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
    app.dependency_overrides.clear()