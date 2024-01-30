from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import BackgroundTasks, HTTPException, status, Response
from sqlalchemy import select, update, desc
from sqlalchemy.orm.exc import NoResultFound

from src.stories.models import Story
from src.database.database import Base
from src.stories.schemas import UpdateStorySchema
from src.utils import update_photo
from .exceptions import (
    NO_DATA_FOUND,
    SERVER_ERROR,
    NO_RECORD,
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


async def update_story(
    story_data: UpdateStorySchema,
    model: Type[Base],
    session: AsyncSession,
    background_tasks: BackgroundTasks,
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
        update_data[media_field_name] = await update_photo(
            story_data.media_path,
            record,
            media_field_name,
            background_tasks,
        )
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
