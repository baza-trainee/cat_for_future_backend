from typing import Annotated, Tuple

from pydantic import EmailStr
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import BackgroundTasks, Form, HTTPException, Request, status
from fastapi_users.authentication import Authenticator, Strategy
from fastapi_users import InvalidPasswordException, exceptions, models, schemas
from fastapi_users.password import PasswordHelper
from fastapi_users.manager import BaseUserManager
from fastapi_users.router.common import ErrorCode

from src.auth.exceptions import DB_ERROR, UNIQUE_ERROR
from .schemas import UserCreate, UserRead



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
        if "duplicate key value violates unique constraint" in str(e):
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
