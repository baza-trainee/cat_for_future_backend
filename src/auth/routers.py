from typing import Tuple

from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import (
    APIRouter,
    BackgroundTasks,
    Body,
    Depends,
    Form,
    Request,
    Response,
    status,
)
from fastapi_users.authentication import Strategy
from fastapi_users import models
from fastapi_users.manager import BaseUserManager
from fastapi_users.router.reset import RESET_PASSWORD_RESPONSES

from src.database.database import get_async_session
from .responses import login_responses, logout_responses, is_accessible_resposes
from .auth_config import CURRENT_USER, auth_backend
from .models import User
from .manager import get_user_manager
from .service import (
    process_change_password,
    process_forgot_password,
    process_login,
    process_logout,
    process_reset_password,
    get_current_user_token,
    OAuth2PasswordRequestForm,
)


auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("/login", responses=login_responses)
async def login(
    request: Request,
    credentials: OAuth2PasswordRequestForm = Depends(),
    user_manager: BaseUserManager[models.UP, models.ID] = Depends(get_user_manager),
    strategy: Strategy[models.UP, models.ID] = Depends(auth_backend.get_strategy),
):
    return await process_login(request, credentials, user_manager, strategy)


@auth_router.post("/logout", responses=logout_responses)
async def logout(
    user_token: Tuple[models.UP, str] = Depends(get_current_user_token),
    strategy: Strategy[models.UP, models.ID] = Depends(auth_backend.get_strategy),
):
    # user, _ = user_token
    # await invalidate_cache("get_me", user.email)
    return await process_logout(user_token, strategy)


@auth_router.post("/forgot-password", status_code=status.HTTP_202_ACCEPTED)
async def forgot_password(
    request: Request,
    background_tasks: BackgroundTasks,
    email: EmailStr = Body(..., embed=True),
    user_manager: BaseUserManager[models.UP, models.ID] = Depends(get_user_manager),
):
    return await process_forgot_password(request, background_tasks, email, user_manager)


@auth_router.post("/reset-password", responses=RESET_PASSWORD_RESPONSES)
async def reset_password(
    request: Request,
    token: str = Body(...),
    password: str = Body(...),
    session: AsyncSession = Depends(get_async_session),
    user_manager: BaseUserManager[models.UP, models.ID] = Depends(get_user_manager),
):
    return await process_reset_password(request, token, password, session, user_manager)


@auth_router.post("/change-password")
async def change_password(
    old_password: str = Form(...),
    new_password: str = Form(...),
    new_password_confirm: str = Form(...),
    user: User = Depends(CURRENT_USER),
    session: AsyncSession = Depends(get_async_session),
    user_manager=Depends(get_user_manager),
    user_token: Tuple[models.UP, str] = Depends(get_current_user_token),
):
    return await process_change_password(
        old_password,
        new_password,
        new_password_confirm,
        user,
        session,
        user_manager,
        user_token,
    )


@auth_router.post(
    "/is-accessible",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=is_accessible_resposes,
)
async def check(user_token: Tuple[models.UP, str] = Depends(get_current_user_token)):
    return Response(status_code=status.HTTP_204_NO_CONTENT)
