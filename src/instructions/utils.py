from sqlalchemy.ext.asyncio import AsyncSession

from .exceptions import AFTER_INSTRUCTIONS_CREATE
from .models import Instruction


async def create_instructions(
    instructions_data: list[dict], session: AsyncSession
) -> None:
    try:
        result = []
        for data in instructions_data:
            result.append(Instruction(**data))
        session.add_all(result)
        print(AFTER_INSTRUCTIONS_CREATE)
    except Exception as exc:
        raise exc
