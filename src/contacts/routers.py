from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status
from fastapi_cache.decorator import cache

from src.config import MONTH
from src.auth.models import User
from src.auth.auth_config import CURRENT_SUPERUSER
from src.contacts.service import get_contacts_record, update_contacts_record
from src.contacts.utils import send_feedback_email
from src.database.database import get_async_session
from src.database.redis import invalidate_cache, my_key_builder
from .schemas import ContactsSchema, ContactsUpdateSchema, FeedbackSchema
from .exceptions import NO_CONTACT, SUCCESS_SENT
from .models import Contacts


contacts_router = APIRouter(prefix="/contacts", tags=["Contacts"])
feedback_router = APIRouter(prefix="/feedback", tags=["Contacts"])


@contacts_router.get("", response_model=ContactsSchema)
@cache(expire=MONTH, key_builder=my_key_builder)
async def get_contacts(
    session: AsyncSession = Depends(get_async_session),
):
    return await get_contacts_record(Contacts, session)


@contacts_router.patch("", response_model=ContactsSchema)
async def update_contacts(
    contacts_update: ContactsUpdateSchema,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(CURRENT_SUPERUSER),
):
    await invalidate_cache("get_contacts")
    return await update_contacts_record(contacts_update, Contacts, session)


@feedback_router.post("", status_code=status.HTTP_202_ACCEPTED)
async def send_feedback(
    feedback: FeedbackSchema,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_async_session),
):
    contact = await session.get(Contacts, 1)
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NO_CONTACT)
    background_tasks.add_task(send_feedback_email, contact.email, feedback)
    return {"message": SUCCESS_SENT}
