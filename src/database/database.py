from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import NullPool

from src.config import DATABASE_URL


Base = declarative_base()

engine = create_async_engine(
    DATABASE_URL,
    poolclass=NullPool,
    connect_args={
        "prepared_statement_name_func": lambda: "",
        "statement_cache_size": 0,
    },
)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
