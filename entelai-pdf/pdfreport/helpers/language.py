import logging
import gettext
import os

# Use logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def set_language(language):
    try:
        locale_path = os.path.join(os.path.dirname(__file__), "../../locale")
        os.environ['LANGUAGE'] = language
        lang = gettext.translation('messages', localedir=locale_path, languages=[language])
        lang.install()
        _ = lang.gettext

    except OSError as err:
        logger.info("Traduccion no disponible - OS error: %s", err)
        _ = gettext.gettext
