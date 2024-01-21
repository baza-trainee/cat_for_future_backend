from datetime import datetime
from typing import Optional

from fastapi import Form, UploadFile
from pydantic import Field, FilePath, BaseModel, constr

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
    media_path: FilePath = Field(max_length=MEDIA_PATH_LEN)
    left_text: constr(max_length=LEFT_TEXT_LEN)
    right_text: constr(max_length=RIGHT_TEXT_LEN)
    created_at: datetime


class UpdateHeroSchema(BaseModel):
    title: constr(max_length=TITLE_LEN)
    sub_title: constr(max_length=SUB_TITLE_LEN)
    media_path: Optional[UploadFile]
    left_text: constr(max_length=LEFT_TEXT_LEN)
    right_text: constr(max_length=RIGHT_TEXT_LEN)

    @classmethod
    def as_form(
        cls,
        title: str = Form(max_length=TITLE_LEN),
        sub_title: str = Form(max_length=SUB_TITLE_LEN),
        media_path: UploadFile = None,
        left_text: str = Form(max_length=LEFT_TEXT_LEN),
        right_text: str = Form(max_length=RIGHT_TEXT_LEN),
    ):
        return cls(
            title=title,
            sub_title=sub_title,
            media_path=media_path,
            left_text=left_text,
            right_text=right_text,
        )
