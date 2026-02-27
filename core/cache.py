from fastapi_cache import FastAPICache

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
    # Extract user from either direct kwargs or nested kwargs structure
    user = kwargs.get("user")
    if not user:
        # If user is not available, try to extract from nested kwargs
        nested_kwargs = kwargs.get("kwargs", {})
        user = nested_kwargs.get("user")
    
    # If user is still not available, return None to disable caching
    if not user:
        return None
    
    return f"{namespace}:user:{user.id}:{request.url.path}?{request.url.query}"