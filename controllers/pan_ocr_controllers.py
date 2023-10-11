import logging
import torch
from controllers.o_c_r_controller import OCRController
from models.pan_model import *
from models.text_extraction.text_extractor import TextExtractor
from utils import IdType

from utils.image_crop import crop_image

logger = logging.getLogger(__name__)


class PANOCRController(OCRController):
    def __init__(self, pan_model, segmentation_model):
        super().__init__(pan_model, idType=IdType.PAN)
        self.old_data_model = {
            "name": "",
            "fatherName": "",
            "DOB": "",
            "pan": "",
        }
        self.text_extractor = TextExtractor()

    def process_results(self, results):
        for result in results:
            result_data = {}
            for box in result.boxes:
                box_s = box.data.cpu()
                bbox, conf, label = (
                    torch.round(box_s[0][:4]).int(),
                    round(box_s[0][4].item(), 2),
                    box_s[0][5].item(),
                )

                if label in result_data:
                    if conf > result_data[label]["confidence_score"]:
                        result_data[label]["bounding_box"] = bbox
                        result_data[label]["confidence_score"] = conf
                else:
                    result_data[label] = {
                        "bounding_box": bbox,
                        "confidence_score": conf,
                    }

        return result_data

    def extract_text(self, image):
        extracted_text = self.text_extractor.extract_text(image)

        # print("Extracted text is: \n" + extracted_text)

        return extracted_text.removeprefix("\n").removesuffix("\n").strip()

    def extract_data(self, result_data, cropped_img):
        className = {0: "dob", 1: "father name", 2: "name", 3: "pan number"}

        for label, data in result_data.items():
            if className.get(label) == "dob":
                cutout_img = crop_image(
                    cropped_img, data.pop("bounding_box"), padding=5
                )
                raw_text = self.text_extractor.call_GCP(cutout_img)
                dob = filter_d_o_b(raw_text)
                logger.debug(str(dob))
                self.data_model.details.dob.text = dob
                self.data_model.details.dob.confidence = data.pop("confidence_score")
                self.old_data_model["DOB"] = dob

            elif className.get(label) == "father name":
                cutout_img = crop_image(
                    cropped_img, data.pop("bounding_box"), padding=5
                )
                raw_text = self.text_extractor.call_GCP(cutout_img)
                self.data_model.details.fatherName.confidence = data.pop(
                    "confidence_score"
                )
                father_name = filter_father_name(raw_text)
                logger.debug(str(father_name))
                self.data_model.details.fatherName.text = father_name
                self.old_data_model["fatherName"] = father_name

            elif className.get(label) == "name":
                cutout_img = crop_image(
                    cropped_img, data.pop("bounding_box"), padding=5
                )
                raw_text = self.text_extractor.call_GCP(cutout_img)
                name = filter_name(raw_text)
                logger.debug(str(name))
                self.data_model.details.name.confidence = data.pop("confidence_score")
                self.data_model.details.name.text = name
                self.old_data_model["name"] = name

            elif className.get(label) == "pan number":
                cutout_img = crop_image(
                    cropped_img, data.pop("bounding_box"), padding=5
                )
                raw_text = self.text_extractor.call_GCP(cutout_img)
                pan_number = filter_p_a_n_Number(raw_text)
                logger.debug(str(pan_number))
                self.data_model.details.pan.text = pan_number
                self.data_model.details.pan.confidence = data.pop("confidence_score")
                self.old_data_model["pan"] = pan_number
