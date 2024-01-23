from sqladmin import ModelView

from src.stories.models import Story


class StoryAdmin(ModelView, model=Story):
    column_list = [
        Story.media_path,
        Story.title,
        Story.text,
    ]
    can_export = False
