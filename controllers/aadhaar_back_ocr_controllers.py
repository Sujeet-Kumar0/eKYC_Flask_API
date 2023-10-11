import re
import torch
from logging import getLogger
from .o_c_r_controller import OCRController
from models.process_address_model import process_address

from utils import IdType, crop_image

torch.cuda.empty_cache()

logger = getLogger(__name__)


class AadhaarBackOCRController(OCRController):
    def __init__(self, aadhaar_back_model, segmentation_model):
        super().__init__(aadhaar_back_model, idType=IdType.AADHAARBACK)
        self.old_data_model = {
            "address": "",
            "district": "",
            "city": "",
            "state": "",
            "pinCode": "",
            "og_add": "",
            "aadhaarNumber": "",
        }

    def process_results(self, results):
        mark = 0

        for result in results:
            result_data = {}

            for box in result.boxes:
                box_s = box.data.cpu()
                bbox, conf, label = (
                    torch.round(box_s[0][:4]).int(),
                    round(box_s[0][4].item(), 2),
                    box_s[0][5].item(),
                )

                if label == 2 or label == 3 or label == 4:
                    mark += 1

                if label in result_data:
                    if conf > result_data[label]["confidence_score"]:
                        result_data[label]["bounding_box"] = bbox
                        result_data[label]["confidence_score"] = conf
                else:
                    result_data[label] = {
                        "bounding_box": bbox,
                        "confidence_score": conf,
                    }

        logger.debug("Marks given are " + str(mark))
        if mark >= 2:
            logger.debug("yohuhooo passed")
            self.data_model.validated = True
        else:
            logger.debug("Huh!!, its not that eazy to pass buddy (> <)..")

        return result_data

    def is_valid_aadhaar(self, aadhaar_number):
        # Remove any spaces or dashes from the Aadhaar number
        aadhaar_number = aadhaar_number.replace(" ", "").replace("-", "")

        # Check if Aadhaar number is exactly 12 digits
        if len(aadhaar_number) != 12:
            return False

        # Check if Aadhaar number consists of only digits
        if not aadhaar_number.isdigit():
            return False

        # Check if the first digit is between 1 and 9
        if not 1 <= int(aadhaar_number[0]) <= 9:
            return False

        # Convert the Aadhaar number to a list of digits
        digits = [int(digit) for digit in aadhaar_number]

        # Calculate the checksum
        checksum = 0
        for i in range(0, 11):
            checksum += digits[i] * (11 - i)

        # Perform modulus 11 operation
        checksum %= 11
        checksum = 11 - checksum

        # Verify the checksum
        if checksum == 10:
            checksum = 0

        return checksum == digits[11]

    def extract_data(self, result_data, cropped_img):
        name = {
            0: "aadhaar number",
            1: "address",
            2: "emblem",
            3: "uiai icon",
            4: "uiai symbol",
            5: "vid",
        }

        for label, data in result_data.items():
            if name.get(label) == "aadhaar number":
                aadhaar_details = self.data_model.details.aadhaarDetails
                cutout_img = crop_image(
                    cropped_img, data.pop("bounding_box"), padding=5
                )
                text = self.text_extractor.call_GCP(cutout_img)
                text = re.sub(r"\D+", "", text)
                # aadhaar_number = "".join(text.split())
                aadhaar_number = text[:12]
                aadhaar_number = aadhaar_number if len(aadhaar_number) == 12 else ""
                # update data
                aadhaar_details.text = aadhaar_number
                aadhaar_details.isVerified = self.is_valid_aadhaar(aadhaar_number)
                aadhaar_details.confidence = data.pop("confidence_score")
                self.old_data_model["aadhaarNumber"] = aadhaar_number

            if name.get(label) == "address":
                address_details = self.data_model.details.address
                cutout_img = crop_image(
                    cropped_img, data.pop("bounding_box"), padding=7
                )
                text = self.text_extractor.call_GCP(cutout_img)
                address, pincode, state, district = process_address(text)
                address_details.address = address
                address_details.pincode = pincode
                address_details.state = state
                address_details.district = district
                self.old_data_model["address"] = address
                self.old_data_model["pinCode"] = pincode
                self.old_data_model["state"] = state
                self.old_data_model["district"] = district
                address_details.confidence = data.pop("confidence_score")
