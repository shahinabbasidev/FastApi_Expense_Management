from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache
from fastapi_cache.backends.redis import RedisBackend

class CacheNamespace:
    USERS_LIST = "users-list"
    EXPENSES_LIST = "expenses-list"

async def clear_user_cache():
    await FastAPICache.clear(namespace=CacheNamespace.USERS_LIST)

async def clear_expenses_cache():
    await FastAPICache.clear(namespace=CacheNamespace.EXPENSES_LIST)
    

def user_expenses_cache_key_builder(
    func,
    namespace: str,
    request,
    response,
    *args,
    **kwargs,
):
    user = kwargs.get("user")
    return f"{namespace}:user:{user.id}:{request.url.path}?{request.url.query}"