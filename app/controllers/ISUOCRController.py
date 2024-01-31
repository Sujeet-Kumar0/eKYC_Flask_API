from app.models.ISUOCRModel import ISUOCRModel


class ISUOCRController:
    def __init__(self):
        self.model = ISUOCRModel()

    def get_text(self, image, lang, oem, psm):
        try:
            return self.model.extract(image, lang, oem, psm)
        except Exception as e:
            return {
                "status": -1,
                "message": "Please recapture ",
                "code": "MB",
                "devMsg": str(e),
            }
