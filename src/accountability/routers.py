from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User
from src.auth.auth_config import CURRENT_SUPERUSER
from src.database.database import get_async_session
from .service import get_accountability_record, update_accountability_record
from .schemas import GetAccountabilitySchema, UpdateAccountabilitySchema

accountability_router = APIRouter(prefix="/accountability", tags=["Accountability"])


@accountability_router.get("", response_model=GetAccountabilitySchema)
async def get_accountability(
    session: AsyncSession = Depends(get_async_session),
):
    record = await get_accountability_record(session=session)
    return record


@accountability_router.put("")
async def put_accountability(
    background_tasks: BackgroundTasks,
    schema: UpdateAccountabilitySchema = Depends(UpdateAccountabilitySchema.as_form),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(CURRENT_SUPERUSER),
):
    record = await update_accountability_record(
        schema=schema, session=session, background_tasks=background_tasks
    )
    return record
