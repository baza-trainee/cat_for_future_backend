from typing import Union
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from src.config import CACHE_PREFIX, REDIS_URL

redis = aioredis.from_url(REDIS_URL, encoding="utf8", decode_responses=True)
cache_key = lambda func, arg: f"{CACHE_PREFIX}:{func}{f':{arg}' if arg else ''}"


async def init_redis() -> None:
    FastAPICache.init(RedisBackend(redis), prefix=CACHE_PREFIX)


async def invalidate_cache(func: str, id_or_mail: Union[int, str] = None):
    key = cache_key(func, id_or_mail)
    await redis.delete(key)


def my_key_builder(func, *args, **kwargs):
    id = kwargs.get("kwargs").get("id")
    return cache_key(func.__name__, id)


def my_key_builder(func, *args, **kwargs):
    user = kwargs.get("kwargs").get("user")
    id = kwargs.get("kwargs").get("id")
    if user:
        return cache_key(func.__name__, user.email)
    else:
        return cache_key(func.__name__, id)
