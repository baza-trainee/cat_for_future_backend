import os
import shutil

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from .exceptions import AFTER_HERO_CREATE, HERO_ALREADY_EXISTS
from .models import Hero


async def create_hero(hero_data, session: AsyncSession):
    try:
        hero_count = await session.scalar(select(func.count()).select_from(Hero))
        if hero_count == 0:
            folder_path = os.path.join("static", "media", Hero.__tablename__)
            if os.path.exists(folder_path):
                shutil.rmtree(folder_path)
            instance = Hero(**hero_data)
            session.add(instance)
            await session.commit()
            print(AFTER_HERO_CREATE)
        else:
            print(HERO_ALREADY_EXISTS)
    except Exception as exc:
        raise exc
