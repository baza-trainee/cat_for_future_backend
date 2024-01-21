from fastapi import Body
from fastapi_users import schemas

from .exceptions import PASSWORD_DESC
from .models import User


NAME_LEN = User.name.type.length
PHONE_LEN = User.phone.type.length
CITY_LEN = User.city.type.length
MAIL_LEN = User.email.type.length


class UserRead(schemas.BaseUser[int]):
    pass


class UserCreate(schemas.BaseUserCreate):
    name: str
    phone: str
    city: str
    email: str
    password: str

    @classmethod
    def as_body(
        cls,
        name: str = Body(..., max_length=NAME_LEN),
        phone: str = Body(
            ...,
            max_length=PHONE_LEN,
            pattern=r"^(\+?38)?\(?\d{3}\)?[-\s]?\d{3}[-\s]?\d{2}[-\s]?\d{2}$",
        ),
        city: str = Body(..., max_length=CITY_LEN),
        email: str = Body(..., max_length=MAIL_LEN),
        password: str = Body(
            ..., min_length=8, max_length=64, description=PASSWORD_DESC
        ),
    ):
        return cls(name=name, phone=phone, city=city, email=email, password=password)


class UserUpdate(schemas.BaseUserUpdate):
    pass
