from fastapi import BackgroundTasks, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.hero.models import Hero
from src.hero.schemas import UpdateHeroSchema
from src.utils import update_photo
from src.exceptions import (
    NO_DATA_FOUND,
    NO_RECORD,
    SERVER_ERROR,
)


async def get_hero_record(session: AsyncSession):
    record = await session.get(Hero, 1)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NO_DATA_FOUND)
    return record


async def update_hero_record(
    schema: UpdateHeroSchema,
    session: AsyncSession,
    background_tasks: BackgroundTasks,
):
    record = await session.get(Hero, 1)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NO_RECORD)

    schema_output = schema.model_dump()
    media_path = schema_output.get("media_path", None)
    if media_path:
        schema_output["media_path"] = await update_photo(
            file=media_path,
            record=record,
            field_name="media_path",
            background_tasks=background_tasks,
        )
    else:
        del schema_output["media_path"]

    try:
        for field, value in schema_output.items():
            setattr(record, field, value)
        await session.commit()
        return record
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=SERVER_ERROR
        )
