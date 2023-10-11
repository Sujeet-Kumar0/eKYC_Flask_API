from flask import jsonify, request
from .invalid_request_error import InvalidRequestError


def get_image(image_key="image"):
    # setting up default values
    class_value = True
    seg_value = True

    if request.is_json:
        data = request.get_json()
        image = data.get(image_key)
        class_value = data.get("classification", True)
        seg_value = data.get("segmentation", True)

    elif request.form.get(image_key):
        image = request.form[image_key]

    # Check if the image is uploaded as a file
    elif request.files.get(image_key):
        image = request.files[image_key]

    # Invaild Error
    else:
        raise InvalidRequestError("Invalid request")

    return image, class_value, seg_value


def create_response(responce):
    # Returns responce
    if responce.status != 0:
        return jsonify(responce), 400
    return jsonify(responce)
