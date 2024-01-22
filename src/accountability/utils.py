import os
import shutil

from sqlalchemy.ext.asyncio import AsyncSession

from .exceptions import AFTER_ACCOUNTABILITY_CREATE
from .models import Accountability


async def create_accountability(
    accountability_data: list[dict], session: AsyncSession
) -> None:
    try:
        folder_path = os.path.join("static", "media", Accountability.__tablename__)
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
        instance = Accountability(**accountability_data)
        session.add(instance)
        print(AFTER_ACCOUNTABILITY_CREATE)
    except Exception as exc:
        raise exc
