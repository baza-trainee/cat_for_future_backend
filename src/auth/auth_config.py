from fastapi import Depends
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import AuthenticationBackend, BearerTransport
from fastapi_users.authentication.strategy.db import (
    AccessTokenDatabase,
    DatabaseStrategy,
)

from .manager import get_user_manager
from .models import AccessToken, User, get_access_token_db


lifetime = 60 * 60 * 24 * 15  # 30 days

bearer_transport = BearerTransport(tokenUrl="api/v1/auth/login")


def get_database_strategy(
    access_token_db: AccessTokenDatabase[AccessToken] = Depends(get_access_token_db),
) -> DatabaseStrategy:
    return DatabaseStrategy(access_token_db, lifetime_seconds=lifetime)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_database_strategy,
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()

CURRENT_SUPERUSER = fastapi_users.current_user(
    active=True, verified=True, superuser=True
)
CURRENT_USER = fastapi_users.current_user(active=True)
