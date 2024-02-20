from typing import Optional

from fastapi import Form, UploadFile
from pydantic import AnyHttpUrl, Field, BaseModel, ValidationInfo, field_validator

from src.config import settings
from .models import Document


MEDIA_PATH_LEN = Document.media_path.type.length
MEDIA_NAME_LEN = Document.name.type.length


class GetDocumentsSchema(BaseModel):
    id: int
    name: str = Field(max_length=MEDIA_NAME_LEN)
    media_path: AnyHttpUrl = Field(max_length=MEDIA_PATH_LEN)

    @field_validator("media_path", mode="before")
    @classmethod
    def add_base_url(cls, value: str, info: ValidationInfo) -> str:
        return f"{settings.BASE_URL}/{value}"


class UpdateDocumentsSchema(BaseModel):
    name: Optional[str] = None
    media_path: Optional[UploadFile] = None

    @classmethod
    def as_form(
        cls,
        name: str = Form(None, max_length=MEDIA_NAME_LEN),
        media_path: UploadFile = None,
    ):
        return cls(media_path=media_path, name=name)
