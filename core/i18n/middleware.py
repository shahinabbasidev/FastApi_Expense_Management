from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from i18n.translator import set_language

class LanguageMiddleware(BaseHTTPMiddleware):
    """
    Middleware that checks the 'Accept-Language' header and sets the appropriate
    language for the response.
    """
    async def dispatch(self, request: Request, call_next):
        await set_language(request)
        response = await call_next(request)
        return response