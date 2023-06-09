from deepface import DeepFace
from flask import Flask, request, render_template, jsonify
from flask_cors import CORS

from controllers import (
    FaceMatchingController,
    AadhaarFrontOCRController,
    ISUOCRController,
    PANOCRController,
    AadhaarBackOCRController,
    AadhaarMaskingController,
)

models = ["VGG-Face", "Facenet", "Facenet512", "OpenFace", "DeepID", "ArcFace", "SFace"]
for model in models:
    try:
        print("Building Model: " + model)
        DeepFace.build_model(model)
    except ValueError:
        print("Error occured while building Model: " + model)

app = Flask(__name__)
CORS(app)
app.config["JSON_SORT_KEYS"] = True

face_matching_controller = FaceMatchingController()
aadhaar_front_ocr_controller = AadhaarFrontOCRController()
aadhaar_back_ocr_controller = AadhaarBackOCRController()
pan_ocr_controller = PANOCRController()
isu_ocr_controller = ISUOCRController()
aadhaar_front_masking_controller = AadhaarMaskingController()


# Root route for the application.
# This route handles GET requests and renders the "index.html" template
@app.route("/")
def hello_world():
    return render_template("index.html", value="Please attached urls of Photos")


# Route for face matching
# This route accepts both JSON and form data
@app.route("/aadhaarfacematch", methods=["POST"])
def call_face_matching():
    if request.is_json:
        data = request.get_json()
        image1 = data["image1"]
        image2 = data["image2"]
    else:
        image1 = request.form["image1"]
        image2 = request.form["image2"]
    return jsonify(face_matching_controller.verify(image1, image2))


@app.route("/manual/aadhaarFaceMatch", methods=["POST"])
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

    return jsonify(
        face_matching_controller.manual_mode(
            image1, image2, model, metrics, backend, enforce_detection
        )
    )


# Route for aadhaar front OCR
# This route accepts both JSON and form data
@app.route("/aadhaarfrontextract", methods=["POST"])
def call_aadhaar_front_ocr():
    if request.is_json:
        data = request.get_json()
        image = data["image"]
    else:
        # Form Data
        image = request.form["image"]
    return aadhaar_front_ocr_controller.process_image(image)


# Route for aadhaar back OCR
# This route accepts both JSON and form data
@app.route("/aadhaarbackextract", methods=["POST"])
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
    return jsonify(pan_ocr_controller.process_image(image))


# Route to extract and verify Aadhaar card Details in total
# This route accepts both JSON and form data
@app.route("/aadhaarfrontmasking", methods=["POST"])
def call_aadhaar_front_masking():
    if request.is_json:
        data = request.get_json()
        imageUrl = data["imageUrl"]
    else:
        imageUrl = request.form["imageUrl"]
    return jsonify(aadhaar_front_masking_controller.get_aadhaar_masking(imageUrl))

# Route to extract and verify Aadhaar card Details in total
# This route accepts both JSON and form data
@app.route("/aadhaarmasking", methods=["POST"])
def call_aadhaar_masking():
    if request.is_json:
        data = request.get_json()
        imageUrl = data["imageUrl"]
    else:
        imageUrl = request.form["imageUrl"]
    return jsonify(aadhaar_front_masking_controller.get_aadhaar_masking(imageUrl))


# Route for Generic OCR
# This route accepts both JSON and form data
@app.route("/isuOCR", methods=["POST"])
def call_isu_o_c_r():
    lang = "eng"
    oem = 3
    psm = 3
    if request.is_json:
        data = request.get_json()
        image = data["image"]

        # Optional values
        lang = data.get("lang", "eng")
        oem = data.get("oem", 3)
        psm = data.get("psm", 3)

    else:
        image = request.form["image"]
    return jsonify(isu_ocr_controller.get_text(image, lang, oem, psm))


# Route to extract and verify Aadhaar card Details in total
# This route accepts both JSON and form data
@app.route("/aadhaarExtract", methods=["POST"])
def call_aadhaar_extract():
    if request.is_json:
        data = request.get_json()
        image1 = data["front"]
        image2 = data["back"]
    else:
        image1 = request.form["front"]
        image2 = request.form["back"]
    return jsonify("Under Development")


# Error handler for 404 (Path Not Found Error) errors
@app.errorhandler(404)
def page_not_found(error):
    return render_template("not_found.html"), 404


# Error handler for 400 errors
@app.errorhandler(400)
def bad_request(error):
    return render_template("bad_request.html", error=error), 400


# Error handler for 401 errors
@app.errorhandler(401)
def unauthorized(error):
    return render_template("unauthorized.html", error=error), 401


# Error handler for 403 errors
@app.errorhandler(403)
def forbidden(error):
    return render_template("forbidden.html", error=error), 403


# Error handler for 405 errors
@app.errorhandler(405)
def method_not_allowed(error):
    return render_template("method_not_allowed.html", error=error), 405


# Error handler for 406 errors
@app.errorhandler(406)
def not_acceptable(error):
    return render_template("not_acceptable.html", error=error), 406


# Error handler for 415 errors
@app.errorhandler(415)
def unsupported_media_type(error):
    return render_template("unsupported_media_type.html", error=error), 415


# Error handler for 422 errors
@app.errorhandler(422)
def unprocessable_entity(error):
    return render_template("unprocessable_entity.html", error=error), 422


# Error handler for 429 errors
@app.errorhandler(429)
def too_many_requests(error):
    return render_template("too_many_requests.html", error=error), 429


# Error handler for 500 errors
@app.errorhandler(500)
def internal_server_error(error):
    return render_template("internal_error.html", error=error), 500


# Error handler for 503 errors
@app.errorhandler(503)
def service_unavailable(error):
    return render_template("service_unavailable.html", error=error), 503


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
