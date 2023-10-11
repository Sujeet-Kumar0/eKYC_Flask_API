from .aadhaar_o_c_r_blueprint import aadhaarocr_bp
from .facematching_blueprint import facematching_bp
from .main_blueprint import main_bp
from .panocr_blueprint import panocr_bp
from app.errors import errors_bp


def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(panocr_bp)
    app.register_blueprint(aadhaarocr_bp)
    app.register_blueprint(errors_bp)
    app.register_blueprint(facematching_bp)
