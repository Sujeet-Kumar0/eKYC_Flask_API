import torch
from ultralytics import YOLO

from utils import Path

import logging

from utils.image_crop import crop_image

logger = logging.getLogger(__name__)


class SegmentationModel:
    def __init__(self):
        self.segmentation_model = YOLO(Path.SEGMENTATION_MODEL)

    def run_segmentation(self, image, id_map_value, result_queue):
        result = self.segment_image(image, id_map_value)
        result_queue.put(result)

    def segment_image(self, image, value: int):
        results = self.segmentation_model(image)

        max_confidence = 0
        bbox = None
        for box in results[0].boxes:
            data = box.data.cpu()
            label = results[0].names[int(data[0][5])]
            logger.info(
                "Label: "
                + label
                + "\n"
                + "Confidence: "
                + str(round(data[0][4].item(), 2))
            )

            if int(data[0][5]) == value and data[0][4] > max_confidence:
                max_confidence = data[0][4]
                bbox = torch.round(data[0][:4]).int()

        if bbox is not None:
            logger.info("Found card with bbox")
            cropped_img = crop_image(image, bbox)

            return cropped_img, round(max_confidence.item(), 2)

        else:
            logger.warning(
                "Bounding box with lable "
                + str(results[0].names[value])
                + " not found."
            )
            return None, 0
