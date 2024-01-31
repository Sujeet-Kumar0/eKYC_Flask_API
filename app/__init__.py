import os

from flask import Flask

from .blueprints import register_blueprints
from .cors import setup_cors


def create_app() -> Flask:
    app = Flask(__name__)
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    setup_cors(app)

    register_blueprints(app)

    return app


app = create_app()
