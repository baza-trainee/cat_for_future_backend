from sqlalchemy.ext.asyncio import AsyncSession
from src.stories.models import Story
from .exceptions import AFTER_STORY_CREATE


async def create_fake_story(story_data: dict, session: AsyncSession):
    try:
        instance = Story(**story_data)
        session.add(instance)
        print(AFTER_STORY_CREATE)
    except Exception as exc:
        raise exc
