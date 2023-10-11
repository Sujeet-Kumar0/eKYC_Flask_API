import logging
from flask import Blueprint, jsonify, abort
import time
import asyncio

from .request_timeout_error import RequestTimeoutError
from .utils import create_response, get_image
from controllers import create_pan_ocr_controller


logger = logging.getLogger(__name__)

panocr_bp = Blueprint("panocr", __name__)


@panocr_bp.route("/panextract", methods=["POST"])
async def call_pan_ocr():
    pan_ocr_controller = create_pan_ocr_controller()
    try:
        image, class_value, seg_value = get_image()
    except Exception as e:
        return jsonify(error=str(e)), 400

    logger.info("\n\n\nLOG: calling PAN extract method %s", image)

    try:
        start_time = time.time()
        timeout_duration = 10  # Set the timeout duration to 10 seconds
        responce = []

        async for r in pan_ocr_controller.main(image, class_value, seg_value):
            responce.append(r)

        # Check if the timeout has been reached
        if time.time() - start_time > timeout_duration:
            pass
            # raise RequestTimeoutError(
            #     payload=ResponseData(
            #         status=-1,
            #         message="Request Time Out",
            #         devMsg="Timeout Error...BOOM.",
            #     )
            # )

    except asyncio.TimeoutError:
        return abort(408, description="Time out .... boom Æ ♥ ª Ñ")

    del pan_ocr_controller

    logger.debug("Response: " + str(responce))

    return create_response(responce[0])


@panocr_bp.errorhandler(RequestTimeoutError)
def request_timeout(e):
    return jsonify(e.payload), e.status_code
