from fastapi import Request
from pathlib import Path
import gettext



class TranslationManager:
    """
    A class that manages translations and handles the installation of the
    correct language translation at runtime.
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.setup_translation()
        return cls._instance

    def setup_translation(self):
        """ Set up translations with a default language (English). """
        lang = "en"  # Default language is English
        locales_dir = Path(__file__).parent / "locales"
        self.translations = gettext.translation(
            "messages", localedir=locales_dir, languages=[lang], fallback=True
        )
        self.translations.install()

    def translate(self, text: str) -> str:
        """ Return the translated string for the given message. """
        return self.translations.gettext(text)

async def set_language(request: Request):
    """ Middleware function to set language based on the Accept-Language header. """
    translator = TranslationManager()
    lang = request.headers.get("Accept-Language", "en")
    locales_dir = Path(__file__).parent / "locales"
    translator.translations = gettext.translation(
        "messages", localedir=locales_dir, languages=[lang], fallback=True
    )
    translator.translations.install()

def _(text: str) -> str:
    """ Shortcut function to access translation for a given string. """
    translator = TranslationManager()
    return translator.translate(text)