from typing import Annotated, List
from fastapi import APIRouter, BackgroundTasks, Depends, File, HTTPException, UploadFile

# from fastapi_pagination import Page, paginate
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.auth_config import CURRENT_USER
from src.database.database import get_async_session
from .models import Cat, CatPhotos
from .schemas import GetCatSchema, CreateCatSchema
from .service import (
    cancel_reserve,
    get_all_cats,
    create_cat,
    get_cat_by_id,
    delete_cat_by_id,
    reserve,
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


@cats_router.post("")
async def post_cat(
    cat_data: CreateCatSchema = Depends(CreateCatSchema.as_form),
    session: AsyncSession = Depends(get_async_session),
    user: Cat = Depends(CURRENT_USER),
):
    # await invalidate_cache("get_news_list")
    return await create_cat(cat_data, Cat, session)


# @cats_router.patch("/{cat_id}")
# async def partial_update_cat(
#     cat_id: int,
#     cat_data: UpdateCatSchema = Depends(UpdateCatSchema.as_form),
#     session: AsyncSession = Depends(get_async_session),
#     user: Cat = Depends(CURRENT_USER),
# ):
#     # await invalidate_cache("get_news", cat_id)
#     # await invalidate_cache("get_news_list")
#     return await update_cat(cat_data, Cat, session, cat_id)


@cats_router.delete("/{cat_id}")
async def delete_cat(
    cat_id: int,
    session: AsyncSession = Depends(get_async_session),
    user: Cat = Depends(CURRENT_USER),
):
    # await invalidate_cache("get_news_list")
    # await invalidate_cache("get_news", cat_id)
    return await delete_cat_by_id(cat_id, Cat, session)


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
