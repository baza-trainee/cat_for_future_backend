from typing import Annotated, Tuple
from typing_extensions import Doc

# from fastapi.security import HTTPBasicCredentials, OAuth2PasswordRequestForm
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
from fastapi_users.authentication import Authenticator, Strategy
from fastapi_users import InvalidPasswordException, exceptions, models, schemas
from fastapi_users.password import PasswordHelper
from fastapi_users.manager import BaseUserManager
from fastapi_users.router.common import ErrorCode, ErrorModel
from fastapi_users.router.reset import RESET_PASSWORD_RESPONSES
from fastapi_users.openapi import OpenAPIResponseType
from sqlalchemy.exc import IntegrityError

from .responses import login_responses, logout_responses
from src.auth.auth_config import CURRENT_USER, auth_backend, fastapi_users
from src.auth.schemas import UserCreate, UserRead
from src.database.database import get_async_session
from .exceptions import (
    DB_ERROR,
    OLD_PASS_INCORRECT,
    PASSWORD_CHANGE_SUCCESS,
    PASSWORD_NOT_MATCH,
    UNIQUE_ERROR,
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
    user: User = Depends(CURRENT_USER),
    session: AsyncSession = Depends(get_async_session),
    user_manager=Depends(get_user_manager),
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


@auth_router.post("/forgot-password", status_code=status.HTTP_202_ACCEPTED)
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


@auth_router.post("/reset-password", responses=RESET_PASSWORD_RESPONSES)
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


@auth_router.post(
    "/register", status_code=status.HTTP_201_CREATED, response_model=UserRead
)
async def register(
    request: Request,
    user_create: UserCreate = Depends(UserCreate.as_body),
    user_manager: BaseUserManager[models.UP, models.ID] = Depends(get_user_manager),
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


# auth_router.include_router(
#     fastapi_users.get_auth_router(auth_backend, requires_verification=True)
# )


class OAuth2PasswordRequestForm:
    def __init__(
        self,
        *,
        username: Annotated[
            str,
            Form(),
            Doc(
                """
                `username` string. The OAuth2 spec requires the exact field name
                `username`.
                """
            ),
        ],
        password: Annotated[
            str,
            Form(),
            Doc(
                """
                `password` string. The OAuth2 spec requires the exact field name
                `password".
                """
            ),
        ],
    ):
        self.username = username
        self.password = password


@auth_router.post(
    "/login",
    name=f"auth:{auth_backend.name}.login",
    responses=login_responses,
)
async def login(
    request: Request,
    credentials: OAuth2PasswordRequestForm = Depends(),
    # credentials: HTTPBasicCredentials = Depends(),
    user_manager: BaseUserManager[models.UP, models.ID] = Depends(get_user_manager),
    strategy: Strategy[models.UP, models.ID] = Depends(auth_backend.get_strategy),
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


auth = Authenticator([auth_backend], get_user_manager)
get_current_user_token = auth.current_user_token(active=True)


@auth_router.post("/logout", responses=logout_responses)
async def logout(
    user_token: Tuple[models.UP, str] = Depends(get_current_user_token),
    strategy: Strategy[models.UP, models.ID] = Depends(auth_backend.get_strategy),
):
    user, token = user_token
    return await auth_backend.logout(strategy, user, token)
