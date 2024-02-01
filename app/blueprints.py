from . import endpoints
from . import errors


def register_blueprints(app):
    app.register_blueprint(errors.app)
    app.register_blueprint(endpoints.app)
    app.register_blueprint(endpoints.face_matching_bp)
