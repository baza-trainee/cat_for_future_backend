from typing import Type
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, Request, Response, status
from fastapi_users import exceptions, models, schemas
from fastapi_users.manager import BaseUserManager
from fastapi_users.router.common import ErrorCode
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import selectinload

from src.database.database import Base
from src.auth.exceptions import DB_ERROR, UNIQUE_ERROR
from src.auth.models import User
from src.exceptions import NO_DATA_FOUND, SERVER_ERROR
from .schemas import UserCreate, UserRead, UserUpdate
from .exceptions import DUPLICATE_MESSAGE


async def process_register(
    request: Request,
    user_create: UserCreate,
    user_manager: BaseUserManager[models.UP, models.ID],
):
    try:
        created_user = await user_manager.create(
            user_create, safe=True, request=request
        )
    except IntegrityError as e:
        if DUPLICATE_MESSAGE in str(e):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=UNIQUE_ERROR
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=DB_ERROR
            )
    except exceptions.UserAlreadyExists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.REGISTER_USER_ALREADY_EXISTS,
        )
    except exceptions.InvalidPasswordException as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "code": ErrorCode.REGISTER_INVALID_PASSWORD,
                "reason": e.reason,
            },
        )
    return schemas.model_validate(UserRead, created_user)


async def process_update(
    request: Request,
    user: User,
    user_update: UserUpdate,
    user_manager: BaseUserManager[models.UP, models.ID],
):
    update_data = user_update.model_dump(exclude_unset=True, exclude_none=True)
    if not update_data:
        return Response(status_code=204)
    try:
        user = await user_manager.update(user_update, user, safe=True, request=request)
        return schemas.model_validate(UserRead, user)
    except exceptions.InvalidPasswordException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": ErrorCode.UPDATE_USER_INVALID_PASSWORD,
                "reason": e.reason,
            },
        )
    except IntegrityError as e:
        if DUPLICATE_MESSAGE in str(e):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=UNIQUE_ERROR
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=DB_ERROR
            )
    except exceptions.UserAlreadyExists:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.UPDATE_USER_EMAIL_ALREADY_EXISTS,
        )


async def get_cats(
    session: AsyncSession,
    user: User,
    model: Type[Base],
):
    try:
        query = (
            select(model).filter_by(user_id=user.id).options(selectinload(model.photos))
        )
        cats = await session.execute(query)
        response = cats.scalars().all()
        if not response:
            raise NoResultFound
        return response
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NO_DATA_FOUND)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=SERVER_ERROR
        )
