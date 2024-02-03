from typing import Optional

from pydantic import (
    AnyHttpUrl,
    Field,
    BaseModel,
    ValidationInfo,
    constr,
    field_validator,
)
from fastapi import Form, UploadFile, File

from src.config import settings
from .models import Story


TITLE_LEN = Story.title.type.length
TEXT_LEN = Story.text.type.length
MEDIA_PATH_LEN = Story.media_path.type.length


class GetStorySchema(BaseModel):
    id: int
    title: constr(max_length=TITLE_LEN)
    text: constr(max_length=TEXT_LEN)
    media_path: AnyHttpUrl = Field(max_length=MEDIA_PATH_LEN)

    @field_validator("media_path", mode="before")
    @classmethod
    def add_base_url(cls, value: str, info: ValidationInfo) -> str:
        return f"{settings.BASE_URL}/{value}"


class CreateStorySchema(BaseModel):
    title: constr(max_length=TITLE_LEN)
    text: constr(max_length=TEXT_LEN)
    media_path: UploadFile

    @classmethod
    def as_form(
        cls,
        title: str = Form(max_length=TITLE_LEN),
        text: str = Form(max_length=TEXT_LEN),
        media_path: UploadFile = File(...),
    ):
        return cls(
            title=title,
            text=text,
            media_path=media_path,
        )


class UpdateStorySchema(BaseModel):
    title: Optional[str] = Field(None, max_length=TITLE_LEN)
    text: Optional[str] = Field(None, max_length=TEXT_LEN)
    media_path: Optional[UploadFile]

    @classmethod
    def as_form(
        cls,
        title: Optional[str] = Form(max_length=TITLE_LEN, default=None),
        text: Optional[str] = Form(max_length=TEXT_LEN, default=None),
        media_path: UploadFile = None,
    ):
        return cls(
            title=title,
            text=text,
            media_path=media_path,
        )
