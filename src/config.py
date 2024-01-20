import cloudinary
from fastapi_mail import ConnectionConfig
from pydantic_settings import BaseSettings, SettingsConfigDict


PHOTO_FORMATS = [
    "application/pdf",
    "image/webp",
    "image/png",
    "image/jpeg",
]

FILE_FORMATS = [
    "application/pdf",
]

MAX_FILE_SIZE = 3 * 1024 * 1024


class Settings(BaseSettings):
    CLOUD_NAME: str
    API_KEY: str
    API_SECRET: str

    POSTGRES_PORT: str
    POSTGRES_HOST: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    EMAIL_HOST: str
    EMAIL_USER: str
    EMAIL_PASSWORD: str

    SECRET_AUTH: str
    ADMIN_USERNAME: str
    ADMIN_PASSWORD: str
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()

PROJECT_NAME = "Cats for future "
API_PREFIX = "/api/v1"
DATABASE_URL = f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"

cloudinary.config(
    cloud_name=settings.CLOUD_NAME,
    api_key=settings.API_KEY,
    api_secret=settings.API_SECRET,
)

mail_config = ConnectionConfig(
    MAIL_USERNAME=settings.EMAIL_USER,
    MAIL_PASSWORD=settings.EMAIL_PASSWORD,
    MAIL_FROM=settings.EMAIL_USER,
    MAIL_PORT=587,
    MAIL_SERVER=settings.EMAIL_HOST,
    MAIL_FROM_NAME=PROJECT_NAME,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)

ALLOW_METHODS = ["GET", "POST", "PUT", "OPTIONS", "DELETE", "PATCH"]
ALLOW_HEADERS = [
    "Content-Type",
    "Set-Cookie",
    "Access-Control-Allow-Headers",
    "Access-Control-Allow-Origin",
    "Authorization",
]
ORIGINS = ["*"]

SWAGGER_PARAMETERS = {
    "syntaxHighlight.theme": "obsidian",
    "tryItOutEnabled": True,
    "displayOperationId": True,
    "filter": True,
    "requestSnippets": True,
    "defaultModelsExpandDepth": -1,
    "docExpansion": "none",
    "persistAuthorization": True,
}
