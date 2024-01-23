from typing import Optional

from fastapi import Form, UploadFile
from pydantic import AnyHttpUrl, Field, BaseModel, constr, validator

from src.config import settings
from .models import Hero

TITLE_LEN = Hero.title.type.length
SUB_TITLE_LEN = Hero.sub_title.type.length
MEDIA_PATH_LEN = Hero.media_path.type.length
LEFT_TEXT_LEN = Hero.left_text.type.length
RIGHT_TEXT_LEN = Hero.right_text.type.length


class GetHeroSchema(BaseModel):
    id: int
    title: constr(max_length=TITLE_LEN)
    sub_title: constr(max_length=SUB_TITLE_LEN)
    media_path: AnyHttpUrl = Field(max_length=MEDIA_PATH_LEN)
    left_text: constr(max_length=LEFT_TEXT_LEN)
    right_text: constr(max_length=RIGHT_TEXT_LEN)

    @validator("media_path", pre=True)
    def add_base_url(cls, v, values):
        return f"{settings.BASE_URL}/{v}"


class UpdateHeroSchema(BaseModel):
    title: Optional[str]
    sub_title: Optional[str]
    media_path: Optional[UploadFile]
    left_text: Optional[str]
    right_text: Optional[str]

    @classmethod
    def as_form(
        cls,
        title: str = Form(None, max_length=TITLE_LEN),
        sub_title: str = Form(None, max_length=SUB_TITLE_LEN),
        media_path: UploadFile = None,
        left_text: str = Form(None, max_length=LEFT_TEXT_LEN),
        right_text: str = Form(None, max_length=RIGHT_TEXT_LEN),
    ):
        return cls(
            title=title,
            sub_title=sub_title,
            media_path=media_path,
            left_text=left_text,
            right_text=right_text,
        )
