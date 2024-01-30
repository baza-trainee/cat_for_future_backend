from typing import List
from fastapi import APIRouter, BackgroundTasks, Depends, File, UploadFile

# from fastapi_pagination import Page, paginate
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.auth_config import CURRENT_USER, CURRENT_SUPERUSER
from src.database.database import get_async_session
from .models import Cat
from .schemas import GetCatSchema, CreateCatSchema, UpdateCatSchema
from .service import (
    cancel_reserve,
    get_all_cats,
    create_cat,
    get_cat_by_id,
    delete_cat_by_id,
    reserve,
    update_cat,
)

cats_router = APIRouter(prefix="/cats", tags=["Cats"])


@cats_router.get("", response_model=List[GetCatSchema])
async def get_cats_list(
    session: AsyncSession = Depends(get_async_session),
):
    result = await get_all_cats(Cat, session)
    return result


@cats_router.get("/{cat_id}", response_model=GetCatSchema)
async def get_cat(
    cat_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    result = await get_cat_by_id(Cat, session, cat_id)
    return result


@cats_router.post("", response_model=GetCatSchema)
async def post_cat(
    background_tasks: BackgroundTasks,
    cat_data: CreateCatSchema = Depends(CreateCatSchema.as_form),
    session: AsyncSession = Depends(get_async_session),
    user: Cat = Depends(CURRENT_SUPERUSER),
    photo1: UploadFile = File(...),
    photo2: UploadFile = File(...),
    photo3: UploadFile = File(...),
    photo4: UploadFile = File(...),
):
    photos = [photo1, photo2, photo3, photo4]
    return await create_cat(cat_data, Cat, session, background_tasks, photos)


@cats_router.patch("/{cat_id}", response_model=GetCatSchema)
async def partial_update_cat(
    cat_id: int,
    background_tasks: BackgroundTasks,
    cat_data: UpdateCatSchema = Depends(UpdateCatSchema.as_form),
    photo1: UploadFile = None,
    photo2: UploadFile = None,
    photo3: UploadFile = None,
    photo4: UploadFile = None,
    session: AsyncSession = Depends(get_async_session),
    user: Cat = Depends(CURRENT_SUPERUSER),
):
    photos = [photo1, photo2, photo3, photo4]
    return await update_cat(cat_data, Cat, session, background_tasks, cat_id, photos)


@cats_router.delete("/{cat_id}")
async def delete_cat(
    cat_id: int,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_async_session),
    user: Cat = Depends(CURRENT_SUPERUSER),
):
    return await delete_cat_by_id(cat_id, background_tasks, Cat, session)


@cats_router.post("/{cat_id}/reserve")
async def reserve_cat(
    cat_id: int,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_async_session),
    user=Depends(CURRENT_USER),
):
    return await reserve(cat_id, user, Cat, session, background_tasks)


@cats_router.post("/{cat_id}/cancel-reservation")
async def cancel_reservation(
    cat_id: int,
    session: AsyncSession = Depends(get_async_session),
    user=Depends(CURRENT_USER),
):
    return await cancel_reserve(cat_id, user, Cat, session)
