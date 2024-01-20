from pydantic import EmailStr
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import (
    APIRouter,
    BackgroundTasks,
    Body,
    Depends,
    Form,
    HTTPException,
    Request,
    status,
)
from fastapi_users import InvalidPasswordException, exceptions, models
from fastapi_users.password import PasswordHelper
from fastapi_users.manager import BaseUserManager
from fastapi_users.router.common import ErrorCode
from fastapi_users.router.reset import RESET_PASSWORD_RESPONSES

from src.auth.auth_config import CURRENT_SUPERUSER, fastapi_users, auth_backend
from src.database.database import get_async_session
from .exceptions import (
    OLD_PASS_INCORRECT,
    PASSWORD_CHANGE_SUCCESS,
    PASSWORD_NOT_MATCH,
)
from src.auth.models import User
from src.database.database import get_async_session
from .manager import get_user_manager


auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("/change-password")
async def change_password(
    old_password: str = Form(...),
    new_password: str = Form(...),
    new_password_confirm: str = Form(...),
    user: User = Depends(CURRENT_SUPERUSER),
    session: AsyncSession = Depends(get_async_session),
    user_manager=Depends(get_user_manager),
):
    try:
        await user_manager.validate_password(password=new_password_confirm, user=user)
    except InvalidPasswordException as ex:
        raise HTTPException(status_code=422, detail=ex.reason)
    password_helper = PasswordHelper()
    if new_password != new_password_confirm:
        raise HTTPException(status_code=422, detail=PASSWORD_NOT_MATCH)
    verified, updated = password_helper.verify_and_update(
        old_password, user.hashed_password
    )
    if not verified:
        raise HTTPException(status_code=422, detail=OLD_PASS_INCORRECT)
    query = (
        update(User)
        .where(User.id == user.id)
        .values(hashed_password=password_helper.hash(new_password))
    )
    await session.execute(query)
    await session.commit()
    return {"detail": PASSWORD_CHANGE_SUCCESS}


@auth_router.post(
    "/forgot-password",
    status_code=status.HTTP_202_ACCEPTED,
    name="reset:forgot_password",
)
async def forgot_password(
    request: Request,
    background_tasks: BackgroundTasks,
    email: EmailStr = Body(..., embed=True),
    user_manager: BaseUserManager[models.UP, models.ID] = Depends(get_user_manager),
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


@auth_router.post(
    "/reset-password",
    name="reset:reset_password",
    responses=RESET_PASSWORD_RESPONSES,
)
async def reset_password(
    request: Request,
    token: str = Body(...),
    password: str = Body(...),
    user_manager: BaseUserManager[models.UP, models.ID] = Depends(get_user_manager),
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


auth_router.include_router(
    fastapi_users.get_auth_router(auth_backend, requires_verification=True)
)
