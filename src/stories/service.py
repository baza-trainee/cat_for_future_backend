from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status, BackgroundTasks, Response
from sqlalchemy import delete, insert, select, update, desc, func
from sqlalchemy.orm.exc import NoResultFound

from src.stories.models import Story
from src.database.database import Base
from src.stories.schemas import UpdateStorySchema, CreateStorySchema
from src.utils import save_photo, delete_photo
from .exceptions import (
    NO_DATA_FOUND,
    SERVER_ERROR,
    STORY_EXISTS,
    NO_RECORD,
    SUCCESS_DELETE,
)


async def get_all_stories(
    model: Type[Base],
    session: AsyncSession,
):
    try:
        query = select(model).order_by(desc(model.id))
        story = await session.execute(query)
        response = story.scalars().all()
        if not response:
            raise NoResultFound
        return response
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NO_DATA_FOUND)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=SERVER_ERROR
        )


async def create_story(
    story_data: CreateStorySchema,
    model: Type[Base],
    session: AsyncSession,
):
    query = select(model).where(func.lower(model.title) == story_data.title.lower())
    result = await session.execute(query)
    instance = result.scalars().first()
    if instance:
        raise HTTPException(
            status_code=400,
            detail=STORY_EXISTS % story_data.title,
        )
    story_data.media_path = await save_photo(story_data.media_path, model)

    try:
        query = insert(model).values(**story_data.model_dump()).returning(model)
        result = await session.execute(query)
        story_data = result.scalars().first()
        await session.commit()
        return story_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=SERVER_ERROR)


async def update_story(
    story_data: UpdateStorySchema,
    model: Type[Base],
    session: AsyncSession,
    story_id: int,
):
    query = select(model).where(model.id == story_id)
    result = await session.execute(query)
    record = result.scalars().first()
    if not record:
        raise HTTPException(status_code=404, detail=NO_RECORD)

    update_data = story_data.model_dump(exclude_none=True)
    media_field_name = Story.media_path.name
    media_obj = update_data.get(media_field_name, None)
    if media_obj:
        update_data["media_path"] = await save_photo(story_data.media_path, model)
    if not update_data:
        return Response(status_code=204)

    try:
        query = (
            update(model)
            .where(model.id == story_id)
            .values(**update_data)
            .returning(model)
        )
        result = await session.execute(query)
        await session.commit()
        return result.scalars().first()
    except:
        raise HTTPException(status_code=500, detail=SERVER_ERROR)


async def delete_story_by_id(
    story_id: int,
    background_tasks: BackgroundTasks,
    model: Type[Base],
    session: AsyncSession,
):
    query = select(model).where(model.id == story_id)
    result = await session.execute(query)
    record = result.scalars().first()
    media_path = record.media_path
    if not record:
        raise HTTPException(status_code=404, detail=NO_RECORD)
    try:
        background_tasks.add_task(delete_photo, media_path)
        # await delete_photo(media_path)
        query = delete(model).where(model.id == story_id)
        await session.execute(query)
        await session.commit()
        return {"message": SUCCESS_DELETE % story_id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=SERVER_ERROR)
