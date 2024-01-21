from pydantic import BaseModel

from src.exceptions import SUCCESS_DELETE
from .models import Hero

TITLE_LEN = Hero.title.type.length
SUB_TITLE = Hero.sub_title.type.length
MEDIA_PATH_LEN = Hero.media_path.type.length
LEFT_TEXT = Hero.left_text.type.length
RIGHTH_TEXT = Hero.righth_text.type.length


class DeleteResponseSchema(BaseModel):
    message: str = SUCCESS_DELETE
