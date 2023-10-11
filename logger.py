import logging
import os
from logging.handlers import TimedRotatingFileHandler, QueueHandler, QueueListener
from queue import Queue
import threading
from flask.logging import default_handler
from flask import has_request_context, request

class RequestFormatter(logging.Formatter):
    def format(self, record):
        if has_request_context():
            record.url = request.url
            record.remote_addr = request.remote_addr
        else:
            record.url = None
            record.remote_addr = None

        return super().format(record)

# formatter = RequestFormatter(
#     '[%(asctime)s] %(remote_addr)s requested %(url)s\n'
#     '%(levelname)s in %(module)s: %(message)s'
# )

def configure_logging(app):
    log_file = app.config.get("LOG_FILEPATH")
    logger = get_logger(log_file)

    # Remove the default StreamHandler from app.logger
    app.logger.removeHandler(default_handler)

    # logger.addHandler(app.logger)

    # Add the custom logger's handlers to the Flask application's logger
    for handler in logger.handlers:
        app.logger.addHandler(handler)

    # Set the log level for the Flask application's logger
    app.logger.setLevel(logger.level)

    app.logger.propagate = False


class AppLogger:
    logger = None

    @classmethod
    def get_logger(cls, log_file):
        if cls.logger is None:
            cls.logger = cls._create_logger(log_file)
        return cls.logger

    @staticmethod
    def _create_logger(log_file):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)

        # Create a queue for logging messages
        log_queue = Queue()

        # Create a file handler for logging to a file
        file_handler = TimedRotatingFileHandler(
            log_file, when="midnight", backupCount=30
        )
        file_handler.setLevel(logging.DEBUG)

        # # Create a stream handler for logging to the console
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)

        # Create a formatter for the log messages
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        # Set the formatter for the file and stream handlers
        file_handler.setFormatter(formatter)
        stream_handler.setFormatter(formatter)

        # if not logger.hasHandlers():
        # Create a queue handler and set it as the handler for the logger
        queue_handler = QueueHandler(log_queue)
        logger.addHandler(queue_handler)

        # Add the file and stream handlers to the logger
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

        # Create a listener to handle logging in a separate thread
        queue_listener = QueueListener(
            log_queue, file_handler
        )  # , default_handler, stream_handler)
        listener_thread = threading.Thread(target=queue_listener.start)
        listener_thread.daemon = True
        listener_thread.start()

        return logger


def get_logger(log_file=None, log_folder="logs"):
    os.makedirs(log_folder, exist_ok=True)
    if not log_file:
        log_file = os.path.join(log_folder, "app.log")
    return AppLogger.get_logger(log_file)
