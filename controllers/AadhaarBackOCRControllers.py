from models.AadhaarBackOCRModel import AadhaarBackOCRModel


class AadhaarBackOCRController:

    def __init__(self):
        self.model = AadhaarBackOCRModel()

    def process_image(self, image):
        try:
            return self.model.extract_image(image)
        except Exception as e:
            return {"status": -1, "message": "Please recapture ", "code": "MB", "devMsg": str(e)}
