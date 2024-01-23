from typing import List, Type

from fastapi import BackgroundTasks, HTTPException, Response, status
from psycopg2 import IntegrityError
from pydantic import BaseModel
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import NoResultFound

from .exceptions import DOCS_EXISTS, NO_DOC_FOUND
from .models import Document
from src.utils import update_photo
from src.exceptions import NO_DATA_FOUND, NO_RECORD, SERVER_ERROR
from src.database.database import Base


async def get_documents_record(session: AsyncSession) -> List[Document]:
    try:
        query = select(Document)
        result = await session.execute(query)
        records = result.scalars().all()
        if not records:
            raise NoResultFound
        return records
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NO_DATA_FOUND)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=SERVER_ERROR
        )


async def get_document_by_id(model: Type[Base], session: AsyncSession, id: int):
    query = select(model).where(model.id == id)
    result = await session.execute(query)
    response = result.scalars().first()
    if not response:
        raise HTTPException(status_code=404, detail=NO_DOC_FOUND % id)
    return response


async def update_documents_record(
    id: int,
    schema: BaseModel,
    model: Type[Base],
    session: AsyncSession,
    background_tasks: BackgroundTasks,
):
    query = select(model).where(model.id == id)
    result = await session.execute(query)
    record = result.scalars().first()
    if not record:
        raise HTTPException(status_code=404, detail=NO_DOC_FOUND)
    update_data = schema.model_dump(exclude_none=True)
    if not update_data:
        return Response(status_code=204)
    for key, data in update_data.items():
        if key == "media_path":
            media = await update_photo(
                file=data,
                record=record,
                field_name=key,
                background_tasks=background_tasks,
                is_file=True,
            )
            update_data[key] = media
    try:
        query = (
            update(model).where(model.id == id).values(**update_data).returning(model)
        )
        result = await session.execute(query)
        await session.commit()
        return result.scalars().first()
    except IntegrityError as e:
        await session.rollback()
        if "unique constraint" in str(e.orig):
            raise HTTPException(
                status_code=400, detail=DOCS_EXISTS % update_data.get("name")
            )
        else:
            raise HTTPException(status_code=500, detail=SERVER_ERROR)
