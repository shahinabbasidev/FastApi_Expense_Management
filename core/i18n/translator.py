from fastapi import Request
from pathlib import Path
import gettext
from contextvars import ContextVar

LOCALES_DIR = Path(__file__).parent / "locales"
DOMAIN = "messages"
DEFAULT_LANG = "en"
SUPPORTED_LANGUAGES = {"fr", "fa", "de"}

_current_translator: ContextVar[gettext.NullTranslations] = ContextVar(
    "current_translator"
)

_default_translator = gettext.translation(
    DOMAIN,
    localedir=LOCALES_DIR,
    languages=[DEFAULT_LANG],
    fallback=True,
)


def get_translator(lang: str):
    return gettext.translation(
        DOMAIN,
        localedir=LOCALES_DIR,
        languages=[lang],
        fallback=True,
    )


def extract_language(header: str | None) -> str:
    if not header:
        return DEFAULT_LANG

    lang = header.split(",")[0].split("-")[0].lower()

    if lang not in SUPPORTED_LANGUAGES:
        return DEFAULT_LANG

    return lang


def set_language(request: Request):
    lang_header = request.headers.get("accept-language")
    lang = extract_language(lang_header)
    print(f"🔍 Header: {lang_header} -> Extracted lang: {lang}") 
    translator = get_translator(lang)
    _current_translator.set(translator)


def _(text: str) -> str:
    translator = _current_translator.get(_default_translator)
    return translator.gettext(text)