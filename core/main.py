from fastapi import FastAPI
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from expenses.routes import router as expenses_routes
from users.routes import router as users_routes
from fastapi.middleware.cors import CORSMiddleware
from i18n.middleware import LanguageMiddleware
from openapi import add_language_header
from core.config import settings
from collections.abc import AsyncIterator
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from redis import asyncio as aioredis
import sentry_sdk

# initialize Sentry only when a DSN is configured (e.g. in staging/production)

sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    # Add data like request headers and IP for users,
    # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
    send_default_pii=True,
)



tags_metadata = [
    {
        "name": "expenses",
        "description": "API for managing expenses with FastAPI",
        "externalDocs": {
            "description": "My GitHub",
            "url": "https://github.com/shahinabbasidev",
        },
    }
]


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url(
        settings.REDIS_URL,
        encoding="utf-8",
        decode_responses=True
    )
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    
    yield
    
    await redis.close()

app = FastAPI(
    title="Expenses management application",
    description="This is a section of description",
    version="0.0.1",
    contact={
        "name": "Shahin Abbasi",
        "url": "https://github.com/shahinabbasidev",
        "email": "shahin.abbasi.dev@gmail.com",
    },
    license_info={"name": "MIT"},
    lifespan=lifespan,
    openapi_tags=tags_metadata,
)

@cache()
async def get_cache():
    return 1

app.include_router(expenses_routes)
app.include_router(users_routes, prefix="/users")

origins = ["http://127.0.0.1:5500"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

add_language_header(app)
app.add_middleware(LanguageMiddleware)

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle all unhandled exceptions and return 500 status code."""
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

@app.get("/is-ready",status_code=200)
async def readiness():
    return JSONResponse(content="ready")

@app.get("/sentry-debug")
async def trigger_error():
    1 / 0