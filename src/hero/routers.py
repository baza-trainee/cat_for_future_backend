from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_cache.decorator import cache

from src.auth.models import User
from src.auth.auth_config import CURRENT_SUPERUSER
from src.database.database import get_async_session
from .service import get_hero_record, update_hero_record
from .schemas import GetHeroSchema, UpdateHeroSchema
from src.config import MONTH
from src.database.redis import invalidate_cache, my_key_builder

hero_router = APIRouter(prefix="/hero", tags=["Hero"])


@hero_router.get("", response_model=GetHeroSchema)
@cache(expire=MONTH, key_builder=my_key_builder)
async def get_hero(
    session: AsyncSession = Depends(get_async_session),
):
    record = await get_hero_record(session=session)
    return record


@hero_router.patch("", response_model=GetHeroSchema)
async def patch_hero(
    background_tasks: BackgroundTasks,
    schema: UpdateHeroSchema = Depends(UpdateHeroSchema.as_form),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(CURRENT_SUPERUSER),
):
    record = await update_hero_record(
        schema=schema, session=session, background_tasks=background_tasks
    )
    await invalidate_cache("get_hero")
    return record
