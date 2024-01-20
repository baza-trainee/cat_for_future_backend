import os
from uuid import uuid4
from fastapi import FastAPI
from sqlalchemy import func, select

from src.auth.models import User
from src.auth.utils import create_user
from src.database.database import get_async_session
from src.config import settings


async def lifespan(app: FastAPI):
    async for s in get_async_session():
        async with s.begin():
            user_count = await s.execute(select(func.count()).select_from(User))
            if user_count.scalar() == 0:
                await create_user(
                    email=settings.ADMIN_USERNAME, password=settings.ADMIN_PASSWORD
                )
    yield