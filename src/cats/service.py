from typing import Type

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status, BackgroundTasks, Response
from sqlalchemy import delete, insert, select, update, desc, func
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import selectinload
from .models import CatPhotos

from src.database.database import Base
from src.cats.schemas import CreateCatSchema
from src.utils import save_photo, delete_photo
from .exceptions import (
    NO_DATA_FOUND,
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
            raise HTTPException(status_code=404, detail=NO_DATA_FOUND)
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

        for photo_data in cat_data.photos:
            media_path = await save_photo(photo_data.media_path, model)
            photo_instance = CatPhotos(cat_id=cat_instance.id, media_path=media_path)
            saved_photos.append(photo_instance)
            session.add(photo_instance)

        await session.commit()

        return {
            "cat_instance": cat_instance,
            "photo_paths": [photo.media_path for photo in saved_photos],
        }
    except IntegrityError as e:
        await session.rollback()
        print(f"Error during cat creation: {e}")

        raise HTTPException(status_code=500, detail=str(e))


# async def update_cat(
#     cat_data: UpdateCatSchema,
#     model: Type[Base],
#     session: AsyncSession,
#     cat_id: int,
# ):
#     query = select(model).where(model.id == cat_id)
#     result = await session.execute(query)
#     record = result.scalars().first()
#     if not record:
#         raise HTTPException(status_code=404, detail=NO_DATA_FOUND)
#     update_data = cat_data.model_dump(exclude_none=True)
#     # if photo:
#     #     update_data["photo"] = await save_photo(photo, model)
#     # if not update_data:
#     #     return Response(status_code=204)
#     # try:
#     #     query = (
#     #         update(model)
#     #         .where(model.id == cat_id)
#     #         .values(**update_data)
#     #         .returning(model)
#     #     )
#     #     result = await session.execute(query)
#     #     await session.commit()
#     #     return result.scalars().first()
#     # except:
#     #     raise HTTPException(status_code=500, detail=SERVER_ERROR)

# async def update_cat(
#     cat_data: UpdateCatSchema,
#     model: Type[Base],
#     session: AsyncSession,
#     cat_id: int,
# ):
#     try:
#         # Загрузка кота и связанных с ним фотографий
#         query = select(model).where(model.id == cat_id).options(selectinload(model.photos))
#         cat = await session.execute(query)
#         cat_record = cat.scalars().first()

#         if not cat_record:
#             raise HTTPException(status_code=404, detail=NO_RECORD)

#         # Обновление данных кота
#         if cat_data.name:
#             cat_record.name = cat_data.name
#         if cat_data.is_male is not None:
#             cat_record.is_male = cat_data.is_male
#         if cat_data.description:
#             cat_record.description = cat_data.description
#         if cat_data.date_of_birth:
#             cat_record.date_of_birth = cat_data.date_of_birth

#         # Проверка наличия новых фотографий
#         if cat_data.photos:
#             # Удаление старых фотографий
#             for old_photo in cat_record.photos:
#                 await delete_photo(old_photo.media_path)

#             # Добавление новых фотографий
#             cat_record.photos = []
#             for photo_data in cat_data.photos:
#                 media_path = await save_photo(photo_data.media_path, model)
#                 photo_instance = CatPhotos(cat_id=cat_record.id, media_path=media_path)
#                 session.add(photo_instance)

#         await session.commit()
        
#     except IntegrityError as e:
#         await session.rollback()
#         raise HTTPException(status_code=500, detail=str(e))

    
async def delete_cat_by_id(cat_id: int, model: Type[Base], session: AsyncSession):
    try:
        query = select(model).where(model.id == cat_id).options(selectinload(model.photos))
        cat = await session.execute(query)
        cat_record = cat.scalars().first()

        if not cat_record:
            raise HTTPException(status_code=404, detail=NO_RECORD)

        for photo in cat_record.photos:
            await delete_photo(photo.media_path)

        await session.delete(cat_record)
        await session.commit()

        return {"message": SUCCESS_DELETE % cat_id}

    except HTTPException:
        raise HTTPException(status_code=404, detail=NO_RECORD)

    except Exception as e:
        print({e})
        raise HTTPException(status_code=500, detail=SERVER_ERROR)