import logging
from ultralytics import YOLO
from utils import Path

logger = logging.getLogger(__name__)


class Classification_Model:
    def __init__(self):
        self.model = YOLO(Path.CLASSIFICATION_MODEL)

    def run_classification(self, image, result_queue):
        result = self.call_classification_model(image)
        result_queue.put(result)

    def call_classification_model(self, image):
        names = {0: "aadhaar back", 1: "aadhaar front", 2: "pan"}
        results = self.model(source=image)
        data = results[0].probs.top1
        del results
        logger.info("Data: " + str(data))
        logger.debug("Result: " + str(names.get(data)))
        return data
