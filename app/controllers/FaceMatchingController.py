from app.models.FaceMatchingModel import FaceMatchingModel


class FaceMatchingController:
    def __init__(self):
        self.model = FaceMatchingModel()

    def verify(self, image1, image2):
        try:
            return self.model.verify(image1, image2)
        except Exception as e:
            return {"status": -1, "message": "Please recapture ", "code": "MB", "devMsg": str(e)}

    def manual_mode(self, image1, image2, models, metrics, backends, enforce):
        try:
            return self.model.verify(image1, image2, models, metrics, backends, enforce)
        except Exception as e:
            return {"status": -2, "message": "Error in Model PS:To Developer:'You SUCK at this'" + str(e)}
