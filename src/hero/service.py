from fastapi import BackgroundTasks, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import NoResultFound

from src.hero.models import Hero
from src.hero.schemas import UpdateHeroSchema
from src.utils import update_photo
from src.exceptions import NO_DATA_FOUND, NO_RECORD, SERVER_ERROR


async def get_hero_record(session: AsyncSession) -> Hero:
    try:
        record = await session.get(Hero, 1)
        if not record:
            raise NoResultFound
        return record
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NO_DATA_FOUND)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=SERVER_ERROR
        )


async def update_hero_record(
    schema: UpdateHeroSchema,
    session: AsyncSession,
    background_tasks: BackgroundTasks,
) -> Hero:
    record = await session.get(Hero, 1)
    if not record:
        raise NoResultFound

    schema_output = schema.model_dump()
    media_field_name = Hero.media_path.name
    media_path = schema_output.get(media_field_name, None)
    if media_path:
        schema_output[media_field_name] = await update_photo(
            file=media_path,
            record=record,
            field_name=media_field_name,
            background_tasks=background_tasks,
        )
    else:
        del schema_output[media_field_name]

    try:
        for field, value in schema_output.items():
            setattr(record, field, value)
        await session.commit()
        return record
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NO_RECORD)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=SERVER_ERROR
        )
