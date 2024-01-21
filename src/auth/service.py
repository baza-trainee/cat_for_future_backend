from typing import Annotated, Tuple

from pydantic import EmailStr
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import BackgroundTasks, Form, HTTPException, Request, status
from fastapi_users.authentication import Authenticator, Strategy
from fastapi_users import InvalidPasswordException, exceptions, models, schemas
from fastapi_users.password import PasswordHelper
from fastapi_users.manager import BaseUserManager
from fastapi_users.router.common import ErrorCode

from .auth_config import auth_backend
from .models import User
from .manager import get_user_manager
from .exceptions import (
    DB_ERROR,
    OLD_PASS_INCORRECT,
    PASSWORD_CHANGE_SUCCESS,
    PASSWORD_NOT_MATCH,
    UNIQUE_ERROR,
)


class OAuth2PasswordRequestForm:
    def __init__(
        self, *, username: Annotated[str, Form()], password: Annotated[str, Form()]
    ):
        self.username = username
        self.password = password


auth = Authenticator([auth_backend], get_user_manager)
get_current_user_token = auth.current_user_token(active=True)


async def process_change_password(
    old_password: str,
    new_password: str,
    new_password_confirm: str,
    user: User,
    session: AsyncSession,
    user_manager,
):
    try:
        await user_manager.validate_password(password=new_password_confirm, user=user)
    except InvalidPasswordException as ex:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=ex.reason
        )
    password_helper = PasswordHelper()
    if new_password != new_password_confirm:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=PASSWORD_NOT_MATCH
        )
    verified, updated = password_helper.verify_and_update(
        old_password, user.hashed_password
    )
    if not verified:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=OLD_PASS_INCORRECT
        )
    query = (
        update(User)
        .where(User.id == user.id)
        .values(hashed_password=password_helper.hash(new_password))
    )
    await session.execute(query)
    await session.commit()
    return {"detail": PASSWORD_CHANGE_SUCCESS}


async def process_forgot_password(
    request: Request,
    background_tasks: BackgroundTasks,
    email: EmailStr,
    user_manager: BaseUserManager[models.UP, models.ID],
):
    try:
        user = await user_manager.get_by_email(email)
    except exceptions.UserNotExists:
        return None

    try:
        await user_manager.forgot_password(user, background_tasks, request)
    except exceptions.UserInactive:
        pass

    return None


async def process_reset_password(
    request: Request,
    token: str,
    password: str,
    user_manager: BaseUserManager[models.UP, models.ID],
):
    try:
        await user_manager.reset_password(token, password, request)
    except (
        exceptions.InvalidResetPasswordToken,
        exceptions.UserNotExists,
        exceptions.UserInactive,
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.RESET_PASSWORD_BAD_TOKEN,
        )
    except exceptions.InvalidPasswordException as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "code": ErrorCode.RESET_PASSWORD_INVALID_PASSWORD,
                "reason": e.reason,
            },
        )


async def process_login(
    request: Request,
    credentials: OAuth2PasswordRequestForm,
    user_manager: BaseUserManager[models.UP, models.ID],
    strategy: Strategy[models.UP, models.ID],
):
    user = await user_manager.authenticate(credentials)

    if user is None or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.LOGIN_BAD_CREDENTIALS,
        )
    response = await auth_backend.login(strategy, user)
    await user_manager.on_after_login(user, request, response)
    return response


async def process_logout(
    user_token: Tuple[models.UP, str],
    strategy: Strategy[models.UP, models.ID],
):
    user, token = user_token
    return await auth_backend.logout(strategy, user, token)
