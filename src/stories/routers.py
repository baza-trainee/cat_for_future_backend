from typing import List

from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.auth_config import CURRENT_SUPERUSER
from src.database.database import get_async_session
from .models import Story
from .schemas import GetStorySchema, UpdateStorySchema
from .service import get_all_stories, update_story

stories_router = APIRouter(prefix="/stories", tags=["Stories"])


@stories_router.get("", response_model=List[GetStorySchema])
async def get_stories_list(
    session: AsyncSession = Depends(get_async_session),
):
    result = await get_all_stories(Story, session)
    return result


@stories_router.patch("/{story_id}", response_model=GetStorySchema)
async def partial_update_stories(
    story_id: int,
    background_tasks: BackgroundTasks,
    story_data: UpdateStorySchema = Depends(UpdateStorySchema.as_form),
    session: AsyncSession = Depends(get_async_session),
    user: Story = Depends(CURRENT_SUPERUSER),
):
    return await update_story(story_data, Story, session, background_tasks, story_id)
