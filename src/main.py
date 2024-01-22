import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.config import (
    ALLOW_HEADERS,
    ALLOW_METHODS,
    ORIGINS,
    PROJECT_NAME,
    SWAGGER_PARAMETERS,
    API_PREFIX,
)
from src.auth.routers import auth_router
from src.user.routers import user_router
from src.hero.routers import hero_router
from src.stories.routers import stories_router
from src.instructions.routers import instructions_router
from src.accountability.routers import accountability_router
from src.contacts.routers import contacts_router, feedback_router
from src.donate.routers import donate_router
from src.utils import lifespan


app = FastAPI(
    swagger_ui_parameters=SWAGGER_PARAMETERS,
    title=PROJECT_NAME,
    lifespan=lifespan,
)

app.mount("/static", StaticFiles(directory="static"), name="static")
api_routers = [
    auth_router,
    hero_router,
    user_router,
    stories_router,
    instructions_router,
    accountability_router,
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