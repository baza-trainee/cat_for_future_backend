from typing import List, Optional, Union
from datetime import date, datetime

from pydantic import AnyHttpUrl, Field, BaseModel, constr, validator
from datetime import date
from fastapi import Form, UploadFile, File

from src.config import settings
from .models import Cat, CatPhotos

NAME_LEN = Cat.name.type.length
DESCRIPTION_LEN = Cat.description.type.length
MEDIA_PATH_LEN = CatPhotos.media_path.type.length


class GetCatPhotoSchema(BaseModel):
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


class CreateCatPhotoSchema(BaseModel):
    cat_id: int
    media_path: Union[UploadFile, str]

    @classmethod
    def as_form(
        cls,
        cat_id: int,
        media_path: Union[UploadFile, str] = File(...),
    ):
        return cls(
            cat_id=cat_id,
            media_path=media_path,
        )


class CreateCatSchema(BaseModel):
    name: constr(max_length=NAME_LEN)
    is_male: bool
    is_reserved: bool
    description: constr(max_length=DESCRIPTION_LEN)
    date_of_birth: date = Form(...)
    photos: List[CreateCatPhotoSchema] = []

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
        is_reserved: bool = Form(...),
        description: str = Form(max_length=DESCRIPTION_LEN),
        date_of_birth: str = Form(...),
        photos: List[UploadFile] = File(...),
    ):
        photo_schemas = [
            CreateCatPhotoSchema(cat_id=i, media_path=photo)
            for i, photo in enumerate(photos)
        ]
        return cls(
            name=name,
            is_male=is_male,
            is_reserved=is_reserved,
            description=description,
            date_of_birth=date_of_birth,
            photos=photo_schemas,
        )

    class Config:
        from_attributes = True


# class UpdateCatPhotoSchema(BaseModel):
#     media_path: Union[UploadFile, str]

# class UpdateCatSchema(BaseModel):
#     name: Optional[constr(max_length=NAME_LEN)]
#     is_male: Optional[bool]
#     description: Optional[constr(max_length=DESCRIPTION_LEN)]
#     date_of_birth: Optional[date]
#     # photos: Optional[List[UpdateCatPhotoSchema]]
#     # photos: List[UpdateCatPhotoSchema] = []
#     photos: Optional[List[UpdateCatPhotoSchema]] = Form(None)


#     @validator("date_of_birth", pre=True)
#     def string_to_date(cls, v: object) -> object:
#         if isinstance(v, str):
#             return datetime.strptime(v, "%d-%m-%Y").date()
#         return v

#     @classmethod
#     def as_form(
#         cls,
#         name: Optional[str] = None,
#         is_male: bool = Form(...),
#         description: Optional[str] = None,
#         date_of_birth: Optional[str] = None,
#         # photos: List[UploadFile] = File(...),
#         # photos: Optional[List[UploadFile]] = None,
#         photos: List[UploadFile] = None,
#         # photos: Optional[List[UploadFile]] = File(None),
#     ):
#         photo_schemas = [
#             UpdateCatPhotoSchema(media_path=photo) for photo in photos
#         ]
#         return cls(
#             name=name,
#             is_male=is_male,
#             description=description,
#             date_of_birth=date_of_birth,
#             photos=photo_schemas,
#         )

#     class Config:
#         from_attributes = True
