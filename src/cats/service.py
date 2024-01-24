from typing import Type

from fastapi import HTTPException, status, BackgroundTasks
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, insert, select, update, desc, func
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import selectinload

from .models import CatPhotos
from src.auth.models import User
from src.config import settings
from src.cats.utils import send_notification_email
from src.contacts.models import Contacts
from src.database.database import Base
from src.cats.schemas import CreateCatSchema, UpdateCatSchema
from src.utils import save_photo, delete_photo
from .exceptions import (
    CANCEL_ERROR,
    CANCELED,
    NO_DATA_FOUND,
    RESERVED,
    RESERVED_ERROR,
    SERVER_ERROR,
    CAT_EXISTS,
    NO_RECORD,
    SUCCESS_DELETE,
)


async def get_all_cats(
    model: Type[Base],
    session: AsyncSession,
):
    try:
        query = (
            select(model).order_by(desc(model.id)).options(selectinload(model.photos))
        )
        cat = await session.execute(query)
        response = cat.scalars().all()
        if not response:
            raise NoResultFound
        return response
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NO_DATA_FOUND)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=SERVER_ERROR
        )


async def get_cat_by_id(
    model: Type[Base],
    session: AsyncSession,
    cat_id: int,
):
    query = select(model).options(selectinload(model.photos)).where(model.id == cat_id)
    result = await session.execute(query)
    cat_instance = result.scalar()
    if cat_instance is None:
        raise HTTPException(status_code=404, detail=NO_DATA_FOUND)
    return cat_instance


async def create_cat(
    cat_data: CreateCatSchema,
    model: Type[Base],
    session: AsyncSession,
    photos: [],
):
    query = select(model).where(func.lower(model.name) == cat_data.name.lower())
    result = await session.execute(query)
    instance = result.scalars().first()
    if instance:
        raise HTTPException(
            status_code=400,
            detail=CAT_EXISTS % cat_data.name,
        )

    saved_photos = []
    try:
        cat_instance = model(
            name=cat_data.name,
            is_male=cat_data.is_male,
            description=cat_data.description,
            date_of_birth=cat_data.date_of_birth,
        )
        session.add(cat_instance)
        await session.flush()

        for photo_data in photos:
            media_path = await save_photo(photo_data, model)
            photo_instance = CatPhotos(cat_id=cat_instance.id, media_path=media_path)
            saved_photos.append(photo_instance)
            session.add(photo_instance)

        await session.commit()
        
        cat_data_response = {
            "id": cat_instance.id,
            "name": cat_instance.name,
            "is_male": cat_instance.is_male,
            "is_reserved": cat_instance.is_reserved,
            "description": cat_instance.description,
            "date_of_birth": cat_instance.date_of_birth,
            "photos": [
                {"id": photo.id, "media_path": photo.media_path}
                for photo in saved_photos
            ],
        }
        
        return cat_data_response
    except IntegrityError as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


async def update_cat(
    cat_data: UpdateCatSchema,
    model: Type[Base],
    session: AsyncSession,
    cat_id: int,
    photos: [],
):
    try:
        query = (
            select(model).where(model.id == cat_id).options(selectinload(model.photos))
        )
        cat = await session.execute(query)
        cat_instance = cat.scalars().first()

        if not cat_instance:
            raise HTTPException(status_code=404, detail=NO_RECORD)

        if cat_data.name:
            cat_instance.name = cat_data.name
        if cat_data.is_male is not None:
            cat_instance.is_male = cat_data.is_male
        if cat_data.description:
            cat_instance.description = cat_data.description
        if cat_data.date_of_birth:
            cat_instance.date_of_birth = cat_data.date_of_birth

        saved_photos = []
        i = -1
        for photo_data in photos:
            i += 1
            if photo_data == None:
                continue
            else:
                await delete_photo(cat_instance.photos[i].media_path)

                media_path = await save_photo(photo_data, model)

                update_statement = (
                    update(CatPhotos)
                    .where(CatPhotos.media_path == cat_instance.photos[i].media_path)
                    .values(media_path=media_path)
                )

                await session.execute(update_statement)

        await session.commit()

        await session.refresh(cat_instance)

        return cat_instance

    except NoResultFound:
        raise HTTPException(status_code=404, detail=NO_RECORD)
    except IntegrityError as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


async def delete_cat_by_id(cat_id: int, model: Type[Base], session: AsyncSession):
    try:
        query = (
            select(model).where(model.id == cat_id).options(selectinload(model.photos))
        )
        cat = await session.execute(query)
        cat_instance = cat.scalars().first()

        if not cat_instance:
            raise HTTPException(status_code=404, detail=NO_RECORD)

        for photo in cat_instance.photos:
            await delete_photo(photo.media_path)

        await session.delete(cat_instance)
        await session.commit()

        return {"message": SUCCESS_DELETE % cat_id}

    except HTTPException:
        raise HTTPException(status_code=404, detail=NO_RECORD)

    except Exception as e:
        raise HTTPException(status_code=500, detail=SERVER_ERROR)


async def reserve(
    cat_id: int, user: int, model: Type[Base], session: AsyncSession, background_tasks
):
    cat: model = await session.get(model, cat_id)
    if cat is None:
        raise HTTPException(status_code=404, detail=NO_RECORD)
    if cat.is_reserved:
        raise HTTPException(status_code=400, detail=RESERVED_ERROR)
    cat.is_reserved = True
    cat.user = user
    await session.commit()
    user: User = await session.get(User, user.id)
    contact = await session.get(Contacts, 1)
    if all([user, contact]):
        background_tasks.add_task(
            send_notification_email, cat.name, contact.email, user
        )
    return {"message": RESERVED}


async def cancel_reserve(
    cat_id: int, user: int, model: Type[Base], session: AsyncSession
):
    cat = await session.get(model, cat_id)
    if cat is None:
        raise HTTPException(status_code=404, detail=NO_RECORD)

    if not cat.is_reserved or cat.user_id != user.id:
        raise HTTPException(status_code=400, detail=CANCEL_ERROR)
    cat.is_reserved = False
    cat.user = None
    await session.commit()
    return {"message": CANCELED}
