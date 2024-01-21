import os
import shutil

from sqlalchemy.ext.asyncio import AsyncSession

from .exceptions import AFTER_HERO_CREATE
from .models import Hero


async def create_hero(hero_data: dict, session: AsyncSession):
    try:
        folder_path = os.path.join("static", "media", Hero.__tablename__)
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
        instance = Hero(**hero_data)
        session.add(instance)
        print(AFTER_HERO_CREATE)
    except Exception as exc:
        raise exc
