from flask import Blueprint
from flask import request, render_template

from .controllers import *

aadhaar_back_ocr_controller = AadhaarBackOCRController()
pan_ocr_controller = PANOCRController()
isu_ocr_controller = ISUOCRController()
aadhaar_front_masking_controller = AadhaarMaskingController()

app = Blueprint('all_routes', __name__)


# Root route for the application.
# This route handles GET requests and renders the "index.html" template
@app.route("/")
def hello_world():
    return render_template("index.html", value="Please attached urls of Photos")


face_matching_bp = Blueprint("face_matching_routes", __name__)


# Route for face matching
# This route accepts both JSON and form data
@face_matching_bp.route("/aadhaarfacematch", methods=["POST"])
def call_face_matching():
    if request.is_json:
        data = request.get_json()
        image1 = data["image1"]
        image2 = data["image2"]
    else:
        image1 = request.form["image1"]
        image2 = request.form["image2"]
    return face_matching_controller(image1, image2)


@face_matching_bp.route("/manual/aadhaarFaceMatch", methods=["POST"])
def call_face_matching_in_manual():
    data = request.get_json()

    if not data:
        return {"message": "empty input set passed"}

    # Required values
    image1 = data["image1"]
    image2 = data["image2"]

    # Optional values
    model = data.get("model", None)
    backend = data.get("backend", None)
    enforce_detection = data.get("enforce_detection", True)
    metrics = data.get("metric", None)
    align = data.get("align", True)

    return face_matching_controller(image1, image2, model, metrics, backend, enforce_detection
                                    )


aadhaar_bp = Blueprint("aadhaar_routes")


# Route for aadhaar front OCR
# This route accepts both JSON and form data
@aadhaar_bp.route("/aadhaarfrontextract", methods=["POST"])
def call_aadhaar_front_ocr():
    if request.is_json:
        data = request.get_json()
        image = data["image"]
    else:
        # Form Data
        image = request.form["image"]
    return aadhaar_front_o_c_r_controller(image)


# Route for aadhaar back OCR
# This route accepts both JSON and form data
@aadhaar_bp.route("/aadhaarbackextract", methods=["POST"])
def call_aadhaar_back_ocr():
    if request.is_json:
        data = request.get_json()
        image = data["image"]
    else:
        image = request.form["image"]
    return aadhaar_back_ocr_controller.process_image(image)


# Route for pan OCR
# This route accepts both JSON and form data
@app.route("/panextract", methods=["POST"])
def pan_o_c_r():
    if request.is_json:
        data = request.get_json()
        image = data["image"]
    else:
        image = request.form["image"]
    return pan_ocr_controller.process_image(image)


# Route to extract and verify Aadhaar card Details in total
# This route accepts both JSON and form data
@aadhaar_bp.route("/aadhaarmasking", methods=["POST"])
def call_aadhaar_masking():
    if request.is_json:
        data = request.get_json()
        image_url = data["imageUrl"]
    else:
        image_url = request.form["imageUrl"]
    return aadhaar_front_masking_controller.get_aadhaar_masking(image_url)


# Route to extract and verify Aadhaar card Details in total
# This route accepts both JSON and form data
@aadhaar_bp.route("/aadhaarExtract", methods=["POST"])
def call_aadhaar_extract():
    if request.is_json:
        data = request.get_json()
        image1 = data["front"]
        image2 = data["back"]
    else:
        image1 = request.form["front"]
        image2 = request.form["back"]
    return "Under Development"
