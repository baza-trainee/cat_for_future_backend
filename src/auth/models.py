from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from src.database.database import Base, get_async_session
from sqlalchemy.orm import declared_attr
from fastapi_users_db_sqlalchemy.access_token import (
    SQLAlchemyAccessTokenDatabase,
    SQLAlchemyBaseAccessTokenTable,
)


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String(25))
    phone = Column(String(30), unique=True)
    email = Column(String(50), nullable=False)
    hashed_password: str = Column(String(length=1024), nullable=False)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(Boolean, default=False, nullable=False)
    is_verified: bool = Column(Boolean, default=False, nullable=False)
    cats = relationship("Cat", back_populates="user", passive_deletes=True)


class AccessToken(SQLAlchemyBaseAccessTokenTable[int], Base):
    @declared_attr
    def user_id(cls):
        return Column(
            Integer, ForeignKey("user.id", ondelete="cascade"), nullable=False
        )


async def get_access_token_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyAccessTokenDatabase(session, AccessToken)
