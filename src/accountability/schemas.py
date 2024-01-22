from typing import Optional

from fastapi import UploadFile
from pydantic import AnyHttpUrl, Field, BaseModel, validator

from src.config import settings
from .models import Accountability


MEDIA_PATH_LEN = Accountability.media_path.type.length


class GetAccountabilitySchema(BaseModel):
    id: int
    media_path: AnyHttpUrl = Field(max_length=MEDIA_PATH_LEN)

    @validator("media_path", pre=True)
    def add_base_url(cls, v, values):
        return f"{settings.BASE_URL}/{v}"


class UpdateAccountabilitySchema(BaseModel):
    media_path: Optional[UploadFile]

    @classmethod
    def as_form(cls, media_path: UploadFile = None):
        return cls(media_path=media_path)
