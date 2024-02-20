from fastapi_mail import FastMail, MessageSchema
from sqlalchemy.ext.asyncio import AsyncSession

from src.contacts.schemas import FeedbackSchema

from .exceptions import AFTER_CONTACTS_CREATE
from .models import Contacts
from src.config import mail_config


async def create_contacts(contacts_data: dict, session: AsyncSession):
    try:
        instance = Contacts(**contacts_data)
        session.add(instance)
        print(AFTER_CONTACTS_CREATE)
    except Exception as exc:
        raise exc


async def send_feedback_email(contact_email: str, feedback: FeedbackSchema):
    message = MessageSchema(
        subject="New Feedback Received",
        recipients=[contact_email],
        body=f"Name: {feedback.name or 'Не вказано'}\nEmail: {feedback.email}\n\nMessage: {feedback.message}",
        subtype="plain",
    )
    fm = FastMail(mail_config)
    await fm.send_message(message)
