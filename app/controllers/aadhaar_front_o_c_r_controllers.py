from app.models.AadhaarFrontOCRModel import AadhaarFrontOCRModel


def aadhaar_front_o_c_r_controller(image):
    model = AadhaarFrontOCRModel()
    try:
        return model.extract_image(image)
    except Exception as e:
        return {"status": -1, "message": "Please recapture ", "code": "MB", "devMsg": str(e)}, 400
