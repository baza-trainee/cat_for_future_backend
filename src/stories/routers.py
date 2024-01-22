from typing import Annotated, List
from fastapi import APIRouter, Depends, File, UploadFile

# from fastapi_pagination import Page, paginate
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.auth_config import CURRENT_SUPERUSER
from src.database.database import get_async_session
from .models import Story
from .schemas import GetStorySchema, CreateStorySchema, UpdateStorySchema
from .service import (
    get_all_stories,
    create_story,
    update_story,
    delete_story_by_id,
)

stories_router = APIRouter(prefix="/stories", tags=["Stories"])


@stories_router.get("", response_model=List[GetStorySchema])
async def get_stories_list(
    session: AsyncSession = Depends(get_async_session),
):
    result = await get_all_stories(Story, session)
    return result


@stories_router.post("")
async def post_story(
    story_data: CreateStorySchema = Depends(CreateStorySchema.as_form),
    session: AsyncSession = Depends(get_async_session),
    user: Story = Depends(CURRENT_SUPERUSER),
):
    # await invalidate_cache("get_news_list")
    return await create_story(story_data, Story, session)


@stories_router.patch("/{story_id}")
async def partial_update_news(
    story_id: int,
    story_data: UpdateStorySchema = Depends(UpdateStorySchema.as_form),
    session: AsyncSession = Depends(get_async_session),
    user: Story = Depends(CURRENT_SUPERUSER),
):
    # await invalidate_cache("get_news", story_id)
    # await invalidate_cache("get_news_list")
    return await update_story(story_data, Story, session, story_id)


@stories_router.delete("/{story_id}")
async def delete_news(
    story_id: int,
    session: AsyncSession = Depends(get_async_session),
    user: Story = Depends(CURRENT_SUPERUSER),
):
    # await invalidate_cache("get_news_list")
    # await invalidate_cache("get_news", story_id)
    return await delete_story_by_id(story_id, Story, session)
