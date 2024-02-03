import asyncio
import os
from typing import AsyncGenerator

import pytest
from fastapi_users.password import PasswordHelper
from httpx import AsyncClient
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from src.auth.models import User

from src.database.database import Base
from src.database.database import get_async_session
from src.main import app

os.system("docker compose up postgres_tests -d")
os.system('scripts/wait-for-it.sh localhost:5777 -- echo "TestDB is up"')

DATABASE_URL_TEST = f"postgresql+asyncpg://test_u:test_p@localhost:5777/test_db"

engine_test = create_async_engine(
    DATABASE_URL_TEST,
    poolclass=NullPool,
    connect_args={
        "prepared_statement_name_func": lambda: "",
        "statement_cache_size": 0,
    },
)
async_session_maker = sessionmaker(
    engine_test, class_=AsyncSession, expire_on_commit=False
)
Base.metadata.bind = engine_test


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


app.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture(autouse=True, scope="session")
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    os.system("docker compose stop postgres_tests")
    os.system("docker compose rm -f postgres_tests")


# SETUP
@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def ac():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session")
async def admin_data(ac: AsyncClient):
    password = "T3st12345$"
    admin_data = {
        "email": "test@test.com",
        "hashed_password": PasswordHelper().hash(password),
        "is_superuser": True,
        "is_active": True,
        "is_verified": True,
        "name": "Test",
        "phone": "+38000000000",
    }
    async with async_session_maker() as session:
        stmt = insert(User).values(**admin_data)
        await session.execute(stmt)
        await session.commit()

    admin_data["password"] = password
    return admin_data


@pytest.fixture(scope="session")
async def authorization_header(admin_data: dict, ac: AsyncClient):
    form_data = {
        "username": admin_data["email"],
        "password": admin_data["password"],
    }
    response = await ac.post("api/v1/auth/login", data=form_data)
    response_data = response.json()
    access_token = response_data["access_token"]
    token_type = response_data["token_type"]
    return {"Authorization": f"{token_type} {access_token}"}
