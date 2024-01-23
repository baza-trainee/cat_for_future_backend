from sqladmin import ModelView
from wtforms import Form, StringField, FileField

from src.hero.models import Hero


class MyForm(Form):
    title = StringField("Заголовок")
    sub_title = StringField("Підзаголовок")
    media_path = FileField("Фото")
    left_text = StringField("Текст1")
    right_text = StringField("Текст2")


class HeroAdmin(ModelView, model=Hero):
    name_plural = "Hero section"

    column_list = [
        "title",
        "sub_title",
        "media_path",
        "left_text",
        "right_text",
    ]
    column_labels = {
        "title": "Заголовок",
        "sub_title": "Підзаголовок",
        "media_path": "Фото",
        "left_text": "Текст1",
        "right_text": "Текст2",
    }
    can_create = False
    can_delete = False
    can_export = False
