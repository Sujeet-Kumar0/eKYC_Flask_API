# Create a blueprint for the views
import logging
from flask import Blueprint, jsonify, request, send_file

from controllers import create_logs_controller

logger = logging.getLogger(__name__)


main_bp = Blueprint("index", __name__)

get_logs = create_logs_controller()


# Maintenance endpoint
@main_bp.route("/getLogs")
def call_get_logs():
    # Code to handle the maintenance endpoint
    # ...
    logger.warning("\n\nCalled Maintenance endpoint")
    logger.warning("Requesting logs from :%s", request.remote_addr)
    path = get_logs.download_folder_path()
    response = send_file(path, as_attachment=True, download_name="logs.zip")
    logger.info("Zipped logs are being sent to :%s", request.remote_addr)
    return response


logger.info("API Started")


# Status endpoint
@main_bp.route("/")
def status():
    logger.info("API Started: index called")
    return jsonify({"status": "API is running"})
