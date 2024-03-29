import os
import shutil
from typing import Type
from uuid import uuid4

from fastapi import BackgroundTasks, FastAPI, HTTPException, UploadFile
from sqlalchemy import func, select
import aiofiles

from src.documents.utils import create_documents
from src.auth.models import User
from src.auth.utils import create_user
from src.database.database import Base, get_async_session
from src.config import FILE_FORMATS, MAX_FILE_SIZE_MB, PHOTO_FORMATS, settings
from src.database.fake_data import (
    HERO_DATA,
    INSTRUCTIONS_DATA,
    DOCUMENTS_DATA,
    CONTACTS_DATA,
    CAT_DATA,
    STORY_DATA,
)
from src.exceptions import INVALID_FILE, INVALID_PHOTO, OVERSIZE_FILE
from src.hero.utils import create_hero
from src.instructions.utils import create_instructions
from src.contacts.utils import create_contacts
from src.cats.utils import create_fake_cat
from src.stories.utils import create_fake_story
from src.database.redis import init_redis, redis


lock = redis.lock("my_lock")


async def lifespan(app: FastAPI):
    await init_redis()
    await lock.acquire(blocking=True)
    async for s in get_async_session():
        async with s.begin():
            user_count = await s.scalar(select(func.count()).select_from(User))
            if user_count == 0:
                clear_media_path()
                await create_user(settings.ADMIN_USERNAME, settings.ADMIN_PASSWORD)
                await create_hero(HERO_DATA, s)
                await create_instructions(INSTRUCTIONS_DATA, s)
                await create_documents(DOCUMENTS_DATA, s)
                await create_contacts(CONTACTS_DATA, s)
                await create_fake_cat(CAT_DATA, s)
                await create_fake_story(STORY_DATA, s)

    await lock.release()
    yield


def clear_media_path():
    folder_path = os.path.join("static", "media")
    if os.path.exists(folder_path):
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            if os.path.isfile(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)


async def save_photo(
    file: UploadFile,
    model: Type[Base],
    background_tasks: BackgroundTasks,
    is_file=False,
) -> str:
    if not is_file and not file.content_type in PHOTO_FORMATS:
        raise HTTPException(
            status_code=415, detail=INVALID_PHOTO % (file.content_type, PHOTO_FORMATS)
        )
    if file.size > MAX_FILE_SIZE_MB * 1024 * 1024:
        raise HTTPException(status_code=413, detail=OVERSIZE_FILE)
    if is_file and not file.content_type in FILE_FORMATS:
        raise HTTPException(
            status_code=415, detail=INVALID_FILE % (file.content_type, FILE_FORMATS)
        )

    folder_path = os.path.join(
        "static", "media", model.__tablename__.lower().replace(" ", "_")
    )
    file_name = f'{uuid4().hex}.{file.filename.split(".")[-1]}'
    file_path = os.path.join(folder_path, file_name)

    async def _save_photo(file_path: str):
        os.makedirs(folder_path, exist_ok=True)
        chunk_size = 256
        async with aiofiles.open(file_path, "wb") as buffer:
            while chunk := await file.read(chunk_size):
                await buffer.write(chunk)

    background_tasks.add_task(_save_photo, file_path)
    return file_path


async def delete_photo(path: str, background_tasks: BackgroundTasks) -> None:
    if "media" in path:
        path_exists = os.path.exists(path)
        if path_exists:
            background_tasks.add_task(os.remove, path)


async def update_photo(
    file: UploadFile,
    record: Type[Base],
    field_name: str,
    background_tasks: BackgroundTasks,
    is_file=False,
) -> str:
    old_photo_path = getattr(record, field_name, None)
    new_photo = await save_photo(file, record, background_tasks, is_file)
    if old_photo_path:
        await delete_photo(old_photo_path, background_tasks)
    return new_photo
