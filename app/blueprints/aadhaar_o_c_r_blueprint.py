import logging
from flask import Blueprint, abort, jsonify
import asyncio
import time

from .request_timeout_error import RequestTimeoutError
from .utils import create_response, get_image
from controllers import (
    create_aadhaar_front_ocr_controller,
    create_aadhaar_masking_controller,
    create_aadhaar_back_ocr_controller,
)
from data_models import ResponseData


logger = logging.getLogger(__name__)


aadhaarocr_bp = Blueprint("aadhaarocr", __name__)


# Route for aadhaar front OCR
# This route accepts both JSON and form data
@aadhaarocr_bp.route("/aadhaarfrontextract", methods=["POST"])
async def call_aadhaar_front_ocr():
    aadhaar_front_ocr_controller = create_aadhaar_front_ocr_controller()

    try:
        image, class_value, seg_value = get_image()
    except Exception as e:
        return jsonify(error=str(e)), 400

    logger.info("\n\n\nLOG request from Aadhaar Front Extraction: %s", image)

    try:
        start_time = time.time()
        timeout_duration = 10  # Set the timeout duration to 10 seconds

        async for r in aadhaar_front_ocr_controller.main(image, class_value, seg_value):
            responce = r

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

    del aadhaar_front_ocr_controller
    logger.debug("Response: " + str(responce))

    return create_response(responce)


# Route for aadhaar back OCR
# This route accepts both JSON and form data
@aadhaarocr_bp.route("/aadhaarbackextract", methods=["POST"])
async def call_aadhaar_back_ocr():
    aadhaar_back_ocr_controller = create_aadhaar_back_ocr_controller()

    try:
        image, class_value, seg_value = get_image()
    except Exception as e:
        return jsonify(error=str(e)), 422

    logger.info("\n\n\nLOG:Request from Aadhaar back Extract Image: %s", image)

    try:
        start_time = time.time()
        timeout_duration = 10  # Set the timeout

        async for r in aadhaar_back_ocr_controller.main(image, class_value, seg_value):
            responce = r

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

    del aadhaar_back_ocr_controller

    logger.debug("Response: " + str(responce))

    return create_response(responce)


# Route to mask the given aadhaar image
# This route accepts both JSON and form data
@aadhaarocr_bp.route("/aadhaarmasking", methods=["POST"])
def call_aadhaar_masking():
    aadhaar_masking_controller = create_aadhaar_masking_controller()
    logger.info("\n\nLOG:Request from Aadhaar Masking Image")

    try:
        image, _, _ = get_image(image_key="imageUrl")
    except Exception as e:
        return jsonify(error=str(e)), 422

    responce: ResponseData = list(
        aadhaar_masking_controller.get_aadhaar_masking(image)
    )[0]
    del aadhaar_masking_controller

    return create_response(responce)


@aadhaarocr_bp.errorhandler(RequestTimeoutError)
def invalid_api_usage(e):
    return jsonify(e.payload), e.status_code
