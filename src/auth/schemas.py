from fastapi import Body
from fastapi_users import schemas

from src.auth.exceptions import PASSWORD_DESC
from src.auth.models import User


class UserCreate(schemas.BaseUserCreate):
    pass


class UserRead(schemas.BaseUser[int]):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    pass
