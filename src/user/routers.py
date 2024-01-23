from typing import List

from fastapi_users.router.common import ErrorCode
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
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
from src.exceptions import NO_DATA_FOUND, SERVER_ERROR
from .exceptions import DELETE_ERROR
from .service import process_register
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
    update_data = user_update.model_dump(exclude_unset=True, exclude_none=True)
    if not update_data:
        return Response(status_code=204)
    try:
        user = await user_manager.update(user_update, user, safe=True, request=request)
        # await invalidate_cache("get_me", user.email)
        return schemas.model_validate(UserRead, user)
    except exceptions.InvalidPasswordException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": ErrorCode.UPDATE_USER_INVALID_PASSWORD,
                "reason": e.reason,
            },
        )
    except exceptions.UserAlreadyExists:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.UPDATE_USER_EMAIL_ALREADY_EXISTS,
        )


@user_router.delete(
    "/me", status_code=status.HTTP_204_NO_CONTENT, response_class=Response
)
async def delete_my_account(
    request: Request,
    user=Depends(CURRENT_USER),
    user_manager: BaseUserManager[models.UP, models.ID] = Depends(get_user_manager),
):
    if user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=DELETE_ERROR)
    # await invalidate_cache("get_me", user.email)
    await user_manager.delete(user, request=request)
    return None


@user_router.get(
    "/me/cats",
    response_model=List[GetCatSchema],
)
async def get_my_cats(
    user=Depends(CURRENT_USER),
    session: AsyncSession = Depends(get_async_session),
):
    try:
        query = select(Cat).filter_by(user_id=user.id).options(selectinload(Cat.photos))
        cats = await session.execute(query)
        response = cats.scalars().all()
        if not response:
            raise HTTPException(status_code=404, detail=NO_DATA_FOUND)
        return response
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NO_DATA_FOUND)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=SERVER_ERROR
        )
