from ultralytics import YOLO

from Utils import Path
from models.panOCR import PANOCRModel


class PANOCRController:
    def __init__(self):
        self.object_detector = YOLO(Path.MODEL)
        self.model = PANOCRModel(self.object_detector)

    def process_image(self, image):
        # ultralytics.checks()
        try:
            return self.model.extract_text(image)
        except Exception as e:
            return {"status": -1, "message": "Please recapture ", "code": "MB", "devMsg": str(e)}
