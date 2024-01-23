from typing import List

from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User
from src.auth.auth_config import CURRENT_SUPERUSER
from src.database.database import get_async_session
from .service import get_document_by_id, get_documents_record, update_documents_record
from .schemas import GetDocumentsSchema, UpdateDocumentsSchema
from .models import Document


documents_router = APIRouter(prefix="/documents", tags=["Documents"])


@documents_router.get("", response_model=List[GetDocumentsSchema])
async def get_documents(
    session: AsyncSession = Depends(get_async_session),
):
    records = await get_documents_record(session=session)
    return records


@documents_router.get("/{id}", response_model=GetDocumentsSchema)
async def get_document(
    id: int,
    session: AsyncSession = Depends(get_async_session),
):
    return await get_document_by_id(Document, session, id)


@documents_router.patch("/{id}")
async def put_documents(
    id: int,
    background_tasks: BackgroundTasks,
    schema: UpdateDocumentsSchema = Depends(UpdateDocumentsSchema.as_form),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(CURRENT_SUPERUSER),
):
    record = await update_documents_record(
        id, schema, Document, session, background_tasks
    )
    return record
