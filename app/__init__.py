import os

from flask import Flask, logging

from .blueprints import register_blueprints
from .cors import setup_cors


def create_app() -> Flask:
    app = Flask(__name__)
    logger = logging.create_logger(app)
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        logger.debug("Failed to create", OSError, exc_info=True)
        pass

    setup_cors(app)

    register_blueprints(app)

    return app


app = create_app()
