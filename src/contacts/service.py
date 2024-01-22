from typing import Type

from fastapi import HTTPException, Response
from pydantic_core import Url
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.database import Base
from src.exceptions import (
    NO_RECORD,
    SERVER_ERROR,
)
from .schemas import ContactsUpdateSchema


async def get_contacts_record(model: Type[Base], session: AsyncSession):
    try:
        query = select(model)
        result = await session.execute(query)
        response = result.scalars().first()
        if not response:
            raise HTTPException(status_code=404, detail=NO_RECORD)
        return response
    except:
        raise HTTPException(status_code=500, detail=SERVER_ERROR)


async def update_contacts_record(
    data: ContactsUpdateSchema, model: Type[Base], session: AsyncSession
):
    contacts_data = data.model_dump(exclude_none=True)
    if not contacts_data:
        return Response(status_code=204)
    for key, value in contacts_data.items():
        if isinstance(value, Url):
            contacts_data[key] = str(value)
    try:
        query = (
            update(model).where(model.id == 1).values(**contacts_data).returning(model)
        )
        result = await session.execute(query)
        await session.commit()
        return result.scalars().first()
    except:
        raise HTTPException(status_code=500, detail=SERVER_ERROR)
