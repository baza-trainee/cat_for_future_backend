from sqlalchemy.ext.asyncio import AsyncSession

from .exceptions import AFTER_DOCUMENTS_CREATE
from .models import Document


async def create_documents(documents_data: list[dict], session: AsyncSession) -> None:
    try:
        result = []
        for data in documents_data:
            result.append(Document(**data))
        session.add_all(result)
        print(AFTER_DOCUMENTS_CREATE)
    except Exception as exc:
        raise exc
