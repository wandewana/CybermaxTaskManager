import asyncio
import pytest
from typing import AsyncGenerator

from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

from app.main import app
from app.api.deps import get_db
from app.models.base import Base
from app.schemas.user import UserCreate
from app.db import crud

# --- Test Database Setup ---
MAINTENANCE_DB_URL = "postgresql+asyncpg://user:password@localhost:5434/postgres"
TEST_DB_NAME = "test_taskdb"
TEST_DATABASE_URL = f"postgresql+asyncpg://user:password@localhost:5434/{TEST_DB_NAME}"

engine = create_async_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

# --- Fixtures ---

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session", autouse=True)
async def setup_database():
    """Create and drop the entire test database for the test session."""
    maintenance_engine = create_async_engine(MAINTENANCE_DB_URL, isolation_level="AUTOCOMMIT")
    async with maintenance_engine.connect() as conn:
        await conn.execute(text(f"DROP DATABASE IF EXISTS {TEST_DB_NAME} WITH (FORCE)"))
        await conn.execute(text(f"CREATE DATABASE {TEST_DB_NAME}"))
    await maintenance_engine.dispose()

    # Now, connect to the new test database and create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield # Run the tests
    
    # After tests, drop the test database
    maintenance_engine = create_async_engine(MAINTENANCE_DB_URL, isolation_level="AUTOCOMMIT")
    async with maintenance_engine.connect() as conn:
        await conn.execute(text(f"DROP DATABASE {TEST_DB_NAME} WITH (FORCE)"))
    await maintenance_engine.dispose()

@pytest.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Provide a transactional scope around a test function."""
    async with TestingSessionLocal() as session:
        yield session

@pytest.fixture(scope="function")
async def async_client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Fixture for an async client that uses the test database."""
    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
    del app.dependency_overrides[get_db]


@pytest.fixture(scope="function")
async def test_user(db_session: AsyncSession):
    """Create a test user in the database."""
    user_in = UserCreate(email="testuser@example.com", password="password")
    user = await crud.create_user(db=db_session, user_in=user_in)
    return user

@pytest.fixture(scope="function")
async def auth_token(async_client: AsyncClient, test_user):
    """Get an auth token for the test user."""
    login_data = {
        "username": test_user.email,
        "password": "password"
    }
    response = await async_client.post("/auth/login", data=login_data)
    return response.json()["access_token"]
