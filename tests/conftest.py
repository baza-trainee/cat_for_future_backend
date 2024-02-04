import os
import asyncio
from contextlib import asynccontextmanager
from subprocess import run as sp_run
from time import sleep
from typing import AsyncGenerator

import pytest
from fastapi_users.password import PasswordHelper
from httpx import AsyncClient
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from src.auth.models import User
from src.database.database import Base, get_async_session
from src.main import app

DATABASE_URL_TEST = f"postgresql+asyncpg://test_u:test_p@localhost:5777/test_db"
DB_CONTAINER = "postgres_tests_cats"
DB_VOLUME = f"{os.path.basename(os.getcwd())}_postgres_tests_data"


async def create_database():
    sp_run(["docker", "compose", "up", "postgres_tests", "-d"])
    while True:
        sleep(1)
        res = sp_run(
            ["docker", "inspect", "-f", "{{json .State.Health.Status}}", DB_CONTAINER],
            capture_output=True,
            text=True,
        )
        if "healthy" in res.stdout:
            break

    global engine_test
    engine_test = create_async_engine(
        DATABASE_URL_TEST,
        poolclass=NullPool,
        connect_args={
            "prepared_statement_name_func": lambda: "",
            "statement_cache_size": 0,
        },
    )
    global async_session_maker
    async_session_maker = sessionmaker(
        engine_test, class_=AsyncSession, expire_on_commit=False
    )
    Base.metadata.bind = engine_test
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_database():
    print("DROP")
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    sp_run(["docker", "stop", DB_CONTAINER])
    sp_run(["docker", "rm", "-f", DB_CONTAINER])
    sp_run(["docker", "volume", "rm", DB_VOLUME])


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


get_session_context = asynccontextmanager(override_get_async_session)


@pytest.fixture(autouse=True, scope="session")
async def prepare_database():
    await create_database()
    yield
    await drop_database()


@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def ac():
    app.dependency_overrides[get_async_session] = override_get_async_session
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
