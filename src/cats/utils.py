from datetime import datetime

from fastapi_mail import FastMail, MessageSchema
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from src.auth.models import User
from src.cats.models import Cat, CatPhotos
from src.cats.exceptions import AFTER_CAT_CREATE
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


def string_to_date(v: object) -> object:
    if isinstance(v, str):
        return datetime.strptime(v, "%d-%m-%Y").date()
    return v


async def create_fake_cat(cat_data: dict, session: AsyncSession):
    try:
        cat_data["date_of_birth"] = string_to_date(cat_data["date_of_birth"])

        cat_instance = Cat(
            name=cat_data["name"],
            is_male=cat_data["is_male"],
            description=cat_data["description"],
            date_of_birth=cat_data["date_of_birth"],
        )
        session.add(cat_instance)
        await session.flush()

        for photo_data in cat_data["photos"]:
            photo_instance = CatPhotos(
                cat_id=cat_instance.id, media_path=photo_data["media_path"]
            )
            session.add(photo_instance)

        await session.commit()
        print(AFTER_CAT_CREATE)
    except IntegrityError as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
