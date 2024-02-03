from httpx import AsyncClient
from sqlalchemy import insert
import pytest

from src.hero.models import Hero
from tests.conftest import async_session_maker


@pytest.fixture(scope="session")
async def hero_data():
    async with async_session_maker() as session:
        hero_data = {
            "title": "Подаруй дім для маленьких хвостиків",
            "sub_title": "Вони чекають на тебе",
            "media_path": "static/hero/main_photo.png",
            "left_text": "Наша місія проста, але могутня",
            "right_text": "Опікуємось котами, які поруч з нами переживають буремні часи. Прилаштовуємо у добрі руки.",
        }
        stmt = insert(Hero).values(**hero_data)
        await session.execute(stmt)
        await session.commit()
    return hero_data


async def test_get_hero(ac: AsyncClient, hero_data: dict):
    response = await ac.get("/api/v1/hero")
    assert response.status_code == 200

    result = response.json()
    assert hero_data["title"] == result["title"]


async def test_patch_hero(ac: AsyncClient, hero_data: dict, authorization_header: dict):
    update_data = {
        "title": "test string1",
        "sub_title": "test string2",
    }
    response = await ac.patch(
        "/api/v1/hero", data=update_data, headers=authorization_header
    )
    assert response.status_code == 200

    result = response.json()
    assert update_data["title"] == result["title"]
    assert update_data["sub_title"] == result["sub_title"]
