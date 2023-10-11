import logging
from flask import Blueprint, jsonify, request

from .utils import create_response, get_image
from controllers import create_face_matching
from data_models.responce_data import ResponseData

logger = logging.getLogger(__name__)


facematching_bp = Blueprint("facematching", __name__)

face_matching_controller = create_face_matching()


# Route for face matching
# This route accepts both JSON and form data
@facematching_bp.route("/aadhaarfacematch", methods=["POST"])
def call_face_matching():
    logger.info("\n\n\nLOG:FaceMatching called")
    image1, _, _ = get_image(image_key="image1")
    image2, _, _ = get_image(image_key="image2")
    responce: ResponseData = face_matching_controller.verify(image1, image2)
    return create_response(responce)


@facematching_bp.route("/kotakAadhaarFaceMatch", methods=["POST"])
def call_face_matching_with_photo():
    logger.info("\n\n\nLOG:FaceMatching with Photo called")
    image1, _, _ = get_image(image_key="image1")
    image2, _, _ = get_image(image_key="image2")
    logger.debug("\nimage1: " + str(image1) + "\nimage2: " + str(image2))
    responce: ResponseData = face_matching_controller.verify(
        image1, image2, useAWS=True, photo_provided=True
    )
    return create_response(responce)


@facematching_bp.route("/manual/aadhaarFaceMatch", methods=["POST"])
def call_face_matching_in_manual():
    logger.info("\n\nLOG:FaceMatching MODE manual called")
    data = request.get_json()

    if not data:
        logger.warning("empty json passed")
        return {"message": "empty input set passed"}

    # Required values
    image1 = data["image1"]
    image2 = data["image2"]

    # Optional values
    deepFace = data.get("deepface", {})
    useAWS = data.get("use_aws", None)
    photo = data.get("photo_provided", False)

    return jsonify(
        face_matching_controller.verify(
            image1, image2, useAWS=useAWS, deepface=deepFace, photo_provided=photo
        )
    )
