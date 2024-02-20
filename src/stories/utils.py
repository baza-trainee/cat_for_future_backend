from sqlalchemy.ext.asyncio import AsyncSession
from src.stories.models import Story
from .exceptions import AFTER_STORY_CREATE


async def create_fake_story(story_data_list: list[dict], session: AsyncSession):
    try:
        for story_data in story_data_list:
            instance = Story(**story_data)
            session.add(instance)
        print(AFTER_STORY_CREATE)
    except Exception as exc:
        raise exc
