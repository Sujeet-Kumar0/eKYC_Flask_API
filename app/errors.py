from .blueprints.request_timeout_error import RequestTimeoutError
from data_models import ResponseData
from flask import Blueprint, jsonify

errors_bp = Blueprint("errors", __name__)


@errors_bp.app_errorhandler(404)
def not_found_error(error):
    return (
        jsonify(
            ResponseData(
                status=-1,
                devMsg=str(error),
                message="The Path which you are trying to access dosent exist",
            )
        ),
        404,
    )


@errors_bp.app_errorhandler(405)
def not_found_error(error):
    return (
        jsonify(
            ResponseData(
                status=-1,
                devMsg=str(error),
                message="You are not meant to use like this.",
            )
        ),
        405,
    )


@errors_bp.app_errorhandler(500)
def internal_error(error):
    return jsonify(ResponseData(status=-1, devMsg=str(error))), 500


@errors_bp.app_errorhandler(RequestTimeoutError)
def invalid_api_usage(e):
    return jsonify(e.to_dict()), e.status_code
