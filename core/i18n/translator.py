from fastapi import Request
from pathlib import Path
import gettext
from contextvars import ContextVar


_current_translator: ContextVar[gettext.NullTranslations] = ContextVar(
    "current_translator"
)

LOCALES_DIR = Path(__file__).parent / "locales"
DOMAIN = "messages"
DEFAULT_LANG = "en"


def get_translator(lang: str):
    return gettext.translation(
        DOMAIN,
        localedir=LOCALES_DIR,
        languages=[lang],
        fallback=True,
    )


def set_language(lang: str):
    translator = get_translator(lang)
    _current_translator.set(translator)


def _(text: str) -> str:
    translator = _current_translator.get(get_translator(DEFAULT_LANG))
    return translator.gettext(text)