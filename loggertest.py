import os
import logging

from logging.config import dictConfig

from app.config import Config


class CustomFilter(logging.Filter):
    def filter(self, record):
        record.appName = "eKYC_API"
        return True


logging_configuration = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {"format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"}
    },
    # 'filters': {
    #     'additional': {
    #         '()': CustomFilter
    #     }
    # },
    "handlers": {
        "file_handler": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "DEBUG",
            "formatter": "default",
            "filename": Config.LOG_FILEPATH,
            "when": "midnight",
            "backupCount": 30,
        },
        "stream_handler": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "default",
            "stream": "ext://sys.stdout",
        },
    },
    "root": {"level": "DEBUG", "handlers": ["file_handler", "stream_handler"]},
}


def setup_logging():
    # Create logs folder if does not exist.
    if not os.path.exists(Config.LOG_FOLDER):
        os.makedirs(Config.LOG_FOLDER)

    dictConfig(logging_configuration)

    # # Disable flask internal logger.
    # logging.getLogger('werkzeug').disabled = True
