from app.models.AadhaarFrontOCRModel import AadhaarFrontOCRModel


class AadhaarFrontOCRController:

    def __init__(self):
        self.model = AadhaarFrontOCRModel()

    def process_image(self, image):
        try:
            return self.model.extract_image(image)
        except Exception as e:
            return {"status": -1, "message": "Please recapture ", "code": "MB", "devMsg": str(e)}
