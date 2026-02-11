from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from i18n.translator import set_language


class LanguageMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        set_language(request)
        response = await call_next(request)
        return response