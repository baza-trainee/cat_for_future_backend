from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User
from src.auth.auth_config import CURRENT_SUPERUSER
from src.database.database import get_async_session
from .service import (
    get_instruction_by_id_from_db,
    get_instructions_from_db,
    update_instruction_by_id_from_db,
)
from .schemas import GetInstructionSchema, UpdateInstructionSchema

# from src.database.redis import invalidate_cache
# from src.config import HOUR, MONTH
# from src.database.redis import invalidate_cache, my_key_builder

instructions_router = APIRouter(prefix="/instructions", tags=["Instructions"])


@instructions_router.get("", response_model=List[GetInstructionSchema])
# @cache(expire=HOUR, key_builder=my_key_builder)
async def get_instructions(session: AsyncSession = Depends(get_async_session)):
    return await get_instructions_from_db(session=session)


@instructions_router.get("/{id}", response_model=GetInstructionSchema)
async def get_instruction_by_id(
    id: int,
    session: AsyncSession = Depends(get_async_session),
):
    return await get_instruction_by_id_from_db(id=id, session=session)


@instructions_router.patch("/{id}", response_model=GetInstructionSchema)
async def put_instruction(
    id: int,
    schema: UpdateInstructionSchema,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(CURRENT_SUPERUSER),
):
    record = await update_instruction_by_id_from_db(
        schema=schema, session=session, id=id
    )
    # await invalidate_cache("get_instructions")
    return record
