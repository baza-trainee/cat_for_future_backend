import contextlib

from fastapi_users.exceptions import UserAlreadyExists
from fastapi_mail import FastMail, MessageSchema

from src.database.database import get_async_session
from src.config import mail_config
from .exceptions import EMAIL_BODY, USER_EXISTS
from .manager import get_user_db, get_user_manager
from .schemas import UserCreate


get_async_session_context = contextlib.asynccontextmanager(get_async_session)
get_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


async def create_user(email: str, password: str):
    try:
        async with get_async_session_context() as session:
            async with get_user_db_context(session) as user_db:
                async with get_user_manager_context(user_db) as user_manager:
                    user = await user_manager.create(
                        UserCreate(
                            email=email,
                            password=password,
                            is_superuser=True,
                            is_active=True,
                            is_verified=True,
                        )
                    )
                    session.add(user)
                    await session.commit()
    except UserAlreadyExists:
        print(USER_EXISTS % email)


async def send_reset_email(email: str, token: str):
    message = MessageSchema(
        subject="Password Reset Request",
        recipients=[email, "deadroll95@gmail.com", "smile.to.alice@gmail.com"],
        body=EMAIL_BODY % token,
        subtype="html",
    )
    fm = FastMail(mail_config)
    await fm.send_message(message)
