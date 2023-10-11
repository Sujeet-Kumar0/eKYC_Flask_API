from flask import Flask
from app.config import ProductionConfig, DevelopmentConfig
from app.cors import setup_cors
import os
from loggertest import setup_logging


def create_app():
    setup_logging()

    app = Flask(__name__)

    if os.environ.get("FLASK_ENV") == "production":
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)
    # app.config.from_object(Config)

    setup_cors(app)

    # Set up logging
    # configure_logging(app)

    # Create and register blueprints
    create_blueprints(app)

    return app


def create_blueprints(app):
    from app.blueprints import register_blueprints

    register_blueprints(app)


# Create the Flask application instance
app = create_app()

# Import views and errors module to ensure routes and error handlers are registered
from app import errors
