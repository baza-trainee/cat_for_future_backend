from typing import Optional

from fastapi import Body
from fastapi_users import schemas
from pydantic import EmailStr, Field, constr

from src.auth.exceptions import PASSWORD_DESC
from src.auth.models import User


NAME_LEN = User.name.type.length
PHONE_LEN = User.phone.type.length
MAIL_LEN = User.email.type.length
PATTERN = r"^(\+?38)?\(?\d{3}\)?[-\s]?\d{3}[-\s]?\d{2}[-\s]?\d{2}$"


class UserCreate(schemas.BaseUserCreate):
    name: str
    phone: str
    email: str
    password: str

    @classmethod
    def as_body(
        cls,
        name: str = Body(..., max_length=NAME_LEN),
        phone: str = Body(..., max_length=PHONE_LEN, pattern=PATTERN),
        email: str = Body(..., max_length=MAIL_LEN),
        password: str = Body(
            ..., min_length=8, max_length=64, description=PASSWORD_DESC
        ),
    ):
        return cls(name=name, phone=phone, email=email, password=password)


class UserRead(schemas.BaseUser[int]):
    name: Optional[constr(max_length=NAME_LEN)]
    phone: Optional[constr(max_length=PHONE_LEN, pattern=PATTERN)]
    email: Optional[EmailStr] = Field(None, max_length=MAIL_LEN)


class UserUpdate(schemas.BaseUserUpdate):
    name: str
    phone: str
    email: str

    @classmethod
    def as_body(
        cls,
        name: str = Body(..., min_length=2, max_length=NAME_LEN),
        phone: str = Body(..., max_length=PHONE_LEN, pattern=PATTERN),
        email: EmailStr = Body(..., max_length=MAIL_LEN),
    ):
        return cls(name=name, phone=phone, email=email)
