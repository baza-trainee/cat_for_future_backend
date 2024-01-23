from typing import Optional

from fastapi import Body, Form, UploadFile
from pydantic import AnyHttpUrl, Field, BaseModel, validator

from src.config import settings
from .models import Document


MEDIA_PATH_LEN = Document.media_path.type.length
MEDIA_NAME_LEN = Document.name.type.length


class GetDocumentsSchema(BaseModel):
    id: int
    name: str = Field(max_length=MEDIA_NAME_LEN)
    media_path: AnyHttpUrl = Field(max_length=MEDIA_PATH_LEN)

    @validator("media_path", pre=True)
    def add_base_url(cls, v, values):
        return f"{settings.BASE_URL}/{v}"


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
