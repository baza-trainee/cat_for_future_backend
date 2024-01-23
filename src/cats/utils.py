from fastapi_mail import FastMail, MessageSchema

from src.auth.models import User
from src.config import mail_config
from .exceptions import CAT_MAIL


async def send_notification_email(cat: str, contact_email: str, user: User):
    message = MessageSchema(
        subject=f"Кота {cat} заброньовано",
        recipients=[contact_email],
        body=CAT_MAIL % (cat, user.name, user.phone, user.email),
        subtype="html",
    )
    fm = FastMail(mail_config)
    await fm.send_message(message)
