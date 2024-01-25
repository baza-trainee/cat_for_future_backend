from typing import List, Optional

from fastapi import Form
from pydantic import (
    AnyHttpUrl,
    Field,
    BaseModel,
    constr,
    validator,
    PastDate,
)

from src.config import settings
from .models import Cat, CatPhotos


NAME_LEN = Cat.name.type.length
DESCRIPTION_LEN = Cat.description.type.length
MEDIA_PATH_LEN = CatPhotos.media_path.type.length


class GetCatPhotoSchema(BaseModel):
    id: int
    media_path: AnyHttpUrl = Field(max_length=MEDIA_PATH_LEN)

    @validator("media_path", pre=True)
    def add_base_url(cls, v, values):
        return f"{settings.BASE_URL}/{v}"


class GetCatSchema(BaseModel):
    id: int
    name: constr(max_length=NAME_LEN)
    is_male: bool
    is_reserved: bool
    description: constr(max_length=DESCRIPTION_LEN)
    date_of_birth: PastDate
    photos: List[GetCatPhotoSchema] = []

    class Config:
        from_attributes = True


class CreateCatSchema(BaseModel):
    name: constr(max_length=NAME_LEN)
    is_male: bool
    description: constr(max_length=DESCRIPTION_LEN)
    date_of_birth: PastDate

    @classmethod
    def as_form(
        cls,
        name: str = Form(max_length=NAME_LEN),
        is_male: bool = Form(...),
        description: str = Form(max_length=DESCRIPTION_LEN),
        date_of_birth: PastDate = Form(
            ...,
            json_schema_extra={
                "type": "string",
                "format": "date",
                "pattern": "YYYY-MM-DD",
            },
        ),
    ):
        return cls(
            name=name,
            is_male=is_male,
            description=description,
            date_of_birth=date_of_birth,
        )

    class Config:
        from_attributes = True


class UpdateCatSchema(BaseModel):
    name: Optional[constr(max_length=NAME_LEN)]
    is_male: Optional[bool]
    description: Optional[constr(max_length=DESCRIPTION_LEN)]
    date_of_birth: Optional[PastDate]

    @classmethod
    def as_form(
        cls,
        name: str = Form(None),
        is_male: bool = Form(None),
        description: str = Form(None),
        date_of_birth: PastDate = Form(
            None,
            json_schema_extra={
                "type": "string",
                "format": "date",
                "pattern": "YYYY-MM-DD",
            },
        ),
    ):
        return cls(
            name=name,
            is_male=is_male,
            description=description,
            date_of_birth=date_of_birth,
        )

    class Config:
        from_attributes = True
