import os
import shutil

from sqlalchemy.ext.asyncio import AsyncSession

from .exceptions import AFTER_INSTRUCTIONS_CREATE
from .models import Instruction


async def create_instructions(
    instructions_data: list[dict], session: AsyncSession
) -> None:
    try:
        folder_path = os.path.join("static", "media", Instruction.__tablename__)
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
        result = []
        for data in instructions_data:
            result.append(Instruction(**data))
        session.add_all(result)
        print(AFTER_INSTRUCTIONS_CREATE)
    except Exception as exc:
        raise exc
