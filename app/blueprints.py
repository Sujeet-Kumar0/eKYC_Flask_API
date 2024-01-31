from . import endpoints
from . import errors


def register_blueprints(app):
    app.register_blueprint(errors.app)
    app.register_blueprint(endpoints.app)
