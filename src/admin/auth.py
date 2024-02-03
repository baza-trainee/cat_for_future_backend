from httpx import AsyncClient
from sqladmin.authentication import AuthenticationBackend
from fastapi import Request
from src.config import settings


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]
        async with AsyncClient() as client:
            response = await client.post(
                f"{settings.BASE_URL}/api/v1/auth/login",
                data={"username": username, "password": password},
            )
        if response.status_code == 200:
            token = response.json().get("access_token")
            request.session.update({"token": token})
            return True

    async def logout(self, request: Request) -> bool:
        token = request.session.get("token")
        async with AsyncClient() as client:
            response = await client.post(
                f"{settings.BASE_URL}/api/v1/auth/logout",
                headers={"Authorization": f"Bearer {token}"},
            )
        request.session.clear()
        return response.status_code == 204

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")
        if not token:
            return False
        return True


authentication_backend = AdminAuth(secret_key=settings.SECRET_AUTH)
