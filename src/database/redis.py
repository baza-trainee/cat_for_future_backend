# from fastapi_cache import FastAPICache
# from fastapi_cache.backends.redis import RedisBackend
# from redis import asyncio as aioredis

# from src.config import CACHE_PREFIX, REDIS_URL

# redis = aioredis.from_url(REDIS_URL, encoding="utf8", decode_responses=True)
# cache_key = lambda func, id: f"{CACHE_PREFIX}:{func}{f':{int(id)}' if id else ''}"

# async def init_redis() -> None:
#     FastAPICache.init(RedisBackend(redis), prefix=CACHE_PREFIX)

# async def invalidate_cache(func: str, id: int = None):
#     key = cache_key(func, id)
#     await redis.delete(key)

# def my_key_builder(func, *args, **kwargs):
#     id = kwargs.get("kwargs").get("id")
#     return cache_key(func.__name__, id)
