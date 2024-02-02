from re import match
from typing import Annotated, Optional, Union

from pydantic import (
    BaseModel,
    EmailStr,
    AnyHttpUrl,
    Field,
    ValidationInfo,
    constr,
    field_validator,
)

from .exceptions import INVALID_PHONE
from .models import Contacts


PHONE_LEN = Contacts.phone_first.type.length
MAIL_LEN = Contacts.email.type.length
ADDRESS_LEN = Contacts.post_address.type.length
URL_LEN = Contacts.facebook.type.length

PATTERN = r"^(\+?38)?\(?\d{3}\)?[-\s]?\d{3}[-\s]?\d{2}[-\s]?\d{2}$|^$"


class FeedbackSchema(BaseModel):
    name: Optional[str] = None
    email: Annotated[EmailStr, Field(max_length=MAIL_LEN)]
    message: constr(min_length=2, max_length=10000)


class ContactsSchema(BaseModel):
    post_address: constr(max_length=ADDRESS_LEN)
    phone_first: constr(
        max_length=PHONE_LEN,
        pattern=PATTERN,
    )
    phone_second: constr(
        max_length=PHONE_LEN,
        pattern=PATTERN,
    )
    email: Annotated[EmailStr, Field(max_length=MAIL_LEN)]
    facebook: Union[AnyHttpUrl, str] = Field(max_length=URL_LEN)
    instagram: Union[AnyHttpUrl, str] = Field(max_length=URL_LEN)


class ContactsUpdateSchema(BaseModel):
    post_address: constr(max_length=ADDRESS_LEN) = None
    phone_first: Optional[
        constr(
            max_length=50,
            pattern=PATTERN,
        )
    ] = None
    phone_second: Optional[
        constr(
            max_length=50,
            pattern=PATTERN,
        )
    ] = None
    email: Optional[Union[EmailStr, constr(min_length=5, max_length=MAIL_LEN)]] = None
    facebook: Optional[Union[AnyHttpUrl, constr(max_length=URL_LEN, pattern=r"^$")]] = (
        None
    )
    instagram: Optional[
        Union[AnyHttpUrl, constr(max_length=URL_LEN, pattern=r"^$")]
    ] = None

    @field_validator(
        "facebook",
        "instagram",
        "email",
        "phone_first",
        "phone_second",
    )
    @classmethod
    def validate(cls, value: str, info: ValidationInfo) -> str:
        if not value:
            return ""
        else:
            if info.field_name == "email":
                return EmailStr._validate(value)
            elif info.field_name in ["phone_first", "phone_second"]:
                if not (match(PATTERN, value)):
                    raise ValueError(INVALID_PHONE)
                else:
                    return value
            else:
                return AnyHttpUrl(value)
