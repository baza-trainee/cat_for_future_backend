import os
import shutil

from sqlalchemy.ext.asyncio import AsyncSession

from .exceptions import AFTER_DOCUMENTS_CREATE
from .models import Document


async def create_documents(documents_data: list[dict], session: AsyncSession) -> None:
    try:
        folder_path = os.path.join("static", "media", Document.__tablename__)
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
        result = []
        for data in documents_data:
            result.append(Document(**data))
        session.add_all(result)
        print(AFTER_DOCUMENTS_CREATE)
    except Exception as exc:
        raise exc
