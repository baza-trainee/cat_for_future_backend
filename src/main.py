from fastapi import FastAPI
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
from src.hero.routers import hero_router
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
]

[app.include_router(router, prefix=API_PREFIX) for router in api_routers]
app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=ALLOW_METHODS,
    allow_headers=ALLOW_HEADERS,
)
