from ultralytics import YOLO
from models.pan_model import text_cleaner

from utils.constants import Path
import logging

from utils.image_crop import crop_image


aadhaar_model = YOLO(Path.AADHAAR_FRONT_WEIGHTS_PATH)

logger = logging.getLogger()


def get_photo(image):
    results = aadhaar_model(image)
    # print(results)
    names = {
        0: "aadhaar number",
        1: "dob",
        2: "emblem",
        3: "gender",
        4: "goi symbol",
        5: "issue date",
        6: "name",
        7: "photo",
        8: "vid",
    }

    bbox = None
    cut_out_image = None
    max_conf = 0
    for list in results[0].boxes.data:
        if names[list[5].item()] == names.get(7) and list[4].item() > max_conf:
            logger.debug(names[list[5].item()])
            logger.debug(round(list[4].item(), 2))
            max_conf = round(list[4].item(), 2)
            bbox = list[:4].int()
    if bbox is not None:
        cut_out_image = crop_image(image, bbox, padding=0)

    # cut_out_image.show()
    if cut_out_image is None:
        raise Exception("No picture Found")
    return cut_out_image


def process_name(text):
    if "father" in text.lower():
        return ""
    clean_text = text_cleaner(text)
    sents = clean_text.split(".")
    # Filter out empty sentences and get the sentence with the largest length
    name = max([sent for sent in sents if sent.strip()], key=len, default="")
    return name
