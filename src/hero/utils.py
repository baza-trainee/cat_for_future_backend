from sqlalchemy.ext.asyncio import AsyncSession

from .exceptions import AFTER_HERO_CREATE
from .models import Hero


async def create_hero(hero_data: dict, session: AsyncSession):
    try:
        instance = Hero(**hero_data)
        session.add(instance)
        print(AFTER_HERO_CREATE)
    except Exception as exc:
        raise exc
