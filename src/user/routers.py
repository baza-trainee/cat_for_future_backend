from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi_users import models, schemas, exceptions
from fastapi_users.manager import BaseUserManager
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import selectinload

from src.cats.models import Cat
from src.cats.schemas import GetCatSchema
from src.database.database import get_async_session
from src.auth.auth_config import CURRENT_USER
from src.auth.manager import get_user_manager
from .exceptions import DELETE_ERROR
from .service import get_cats, process_register, process_update
from .schemas import UserRead, UserUpdate, UserCreate


user_router = APIRouter(prefix="/user", tags=["User"])


async def get_user_or_404(
    id: str,
    user_manager: BaseUserManager[models.UP, models.ID] = Depends(get_user_manager),
) -> models.UP:
    try:
        parsed_id = user_manager.parse_id(id)
        return await user_manager.get(parsed_id)
    except (exceptions.UserNotExists, exceptions.InvalidID) as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) from e


@user_router.post("", status_code=status.HTTP_201_CREATED, response_model=UserRead)
async def register(
    request: Request,
    user_create: UserCreate = Depends(UserCreate.as_body),
    user_manager: BaseUserManager[models.UP, models.ID] = Depends(get_user_manager),
):
    return await process_register(request, user_create, user_manager)


@user_router.get("/me", response_model=UserRead)
# @cache(expire=HOUR, key_builder=my_key_builder)
async def get_me(user: models.UP = Depends(CURRENT_USER)):
    return schemas.model_validate(UserRead, user)


@user_router.put("/me", response_model=UserRead, dependencies=[Depends(CURRENT_USER)])
async def update_me(
    request: Request,
    user_update: UserUpdate = Depends(UserUpdate.as_body),
    user: models.UP = Depends(CURRENT_USER),
    user_manager: BaseUserManager[models.UP, models.ID] = Depends(get_user_manager),
):
    # await invalidate_cache("get_me", user.email)
    return await process_update(request, user, user_update, user_manager)


@user_router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_my_account(
    request: Request,
    user=Depends(CURRENT_USER),
    user_manager: BaseUserManager[models.UP, models.ID] = Depends(get_user_manager),
    session: AsyncSession = Depends(get_async_session),
):
    if user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=DELETE_ERROR)
    try:
        cats = await get_cats(session, user, Cat)
        [setattr(cat, "is_reserved", False) for cat in cats]
    except HTTPException as e:
        if e.status_code != status.HTTP_404_NOT_FOUND:
            raise
    await user_manager.delete(user, request=request)
    return None


@user_router.get("/me/cats", response_model=List[GetCatSchema])
async def get_my_cats(
    user=Depends(CURRENT_USER),
    session: AsyncSession = Depends(get_async_session),
):
    return await get_cats(session, user, Cat)
