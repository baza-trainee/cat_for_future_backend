import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqladmin import Admin

from src.config import (
    ALLOW_HEADERS,
    ALLOW_METHODS,
    ORIGINS,
    PROJECT_NAME,
    SWAGGER_PARAMETERS,
    API_PREFIX,
)
from src.admin import __all__ as views
from src.auth.routers import auth_router
from src.user.routers import user_router
from src.hero.routers import hero_router
from src.stories.routers import stories_router
from src.cats.routers import cats_router
from src.instructions.routers import instructions_router
from src.documents.routers import documents_router
from src.contacts.routers import contacts_router, feedback_router
from src.donate.routers import donate_router
from src.utils import lifespan
from src.database.database import engine
from src.admin.auth import authentication_backend

app = FastAPI(
    swagger_ui_parameters=SWAGGER_PARAMETERS,
    title=PROJECT_NAME,
    lifespan=lifespan,
)

admin = Admin(app, engine, authentication_backend=authentication_backend)
[admin.add_view(view) for view in views]

app.mount("/static", StaticFiles(directory="static"), name="static")
api_routers = [
    auth_router,
    hero_router,
    user_router,
    stories_router,
    cats_router,
    instructions_router,
    documents_router,
    contacts_router,
    feedback_router,
    donate_router,
]

[app.include_router(router, prefix=API_PREFIX) for router in api_routers]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=ALLOW_METHODS,
    allow_headers=ALLOW_HEADERS,
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    response.headers["X-Process-Time"] = f"{round(process_time)} ms"
    return response
