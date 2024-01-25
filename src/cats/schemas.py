from typing import List, Optional, Union
from datetime import date, datetime

from pydantic import AnyHttpUrl, Field, BaseModel, constr, validator
from fastapi import Form, UploadFile, File, Body

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
    date_of_birth: Optional[date]
    photos: List[GetCatPhotoSchema] = []

    class Config:
        from_attributes = True


class CreateCatSchema(BaseModel):
    name: constr(max_length=NAME_LEN)
    is_male: bool
    description: constr(max_length=DESCRIPTION_LEN)
    date_of_birth: date = Form(...)

    @validator("date_of_birth", pre=True)
    def string_to_date(cls, v: object) -> object:
        if isinstance(v, str):
            return datetime.strptime(v, "%d-%m-%Y").date()
        return v

    @classmethod
    def as_form(
        cls,
        name: str = Form(max_length=NAME_LEN),
        is_male: bool = Form(...),
        description: str = Form(max_length=DESCRIPTION_LEN),
        date_of_birth: str = Form(...),
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
    date_of_birth: Optional[date]

    @validator("date_of_birth", pre=True)
    def string_to_date(cls, v: object) -> object:
        if isinstance(v, str):
            return datetime.strptime(v, "%d-%m-%Y").date()
        return v

    @classmethod
    def as_form(
        cls,
        name: Optional[str] = Form(None),
        is_male: bool = Form(None),
        description: Optional[str] = Form(None),
        date_of_birth: Optional[str] = Form(None),
    ):
        return cls(
            name=name,
            is_male=is_male,
            description=description,
            date_of_birth=date_of_birth,
        )

    class Config:
        from_attributes = True
