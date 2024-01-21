from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import NoResultFound

from .models import Instruction
from .schemas import UpdateInstructionSchema
from src.exceptions import NO_DATA_FOUND, NO_RECORD, SERVER_ERROR


async def get_instructions_from_db(session: AsyncSession) -> list[Instruction]:
    try:
        query = select(Instruction)
        result = await session.execute(query)
        response = result.scalars().all()
        if not response:
            raise NoResultFound
        return response
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NO_DATA_FOUND)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=SERVER_ERROR
        )


async def get_instruction_by_id_from_db(session: AsyncSession, id: int) -> Instruction:
    try:
        record = await session.get(Instruction, id)
        if not record:
            raise NoResultFound
        return record
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NO_DATA_FOUND)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=SERVER_ERROR
        )


async def update_instruction_by_id_from_db(
    schema: UpdateInstructionSchema,
    session: AsyncSession,
    id: int,
) -> Instruction:
    try:
        record = await session.get(Instruction, id)
        if not record:
            raise NoResultFound
        schema_output = schema.model_dump()
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
