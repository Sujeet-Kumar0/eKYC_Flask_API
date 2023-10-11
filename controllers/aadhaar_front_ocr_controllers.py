import torch
import re
import logging
from .o_c_r_controller import OCRController
from models.aadhaar_model import process_name
from utils import IdType, crop_image

torch.cuda.empty_cache()

logger = logging.getLogger(__name__)


class AadhaarFrontOCRController(OCRController):
    def __init__(self, aadhaar_front_model, segmentation_model):
        super().__init__(aadhaar_front_model, idType=IdType.AADHAARFRONT)
        self.old_data_model = {
            "name": "",
            "DOB": "",
            "aadhaarNumber": "",
            "gender": "",
            "father": "",
            "issueDate": "",
            "idType": IdType.AADHAARFRONT.name,
        }

    def process_results(self, results):
        mark = 0

        result_data = {}
        for box in results[0].boxes:
            box_s = box.data.cpu()
            bbox, conf, label = (
                torch.round(box_s[0][:4]).int(),
                round(box_s[0][4].item(), 2),
                box_s[0][5].item(),
            )

            if label == 4 or label == 2:
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
            logger.info("Huh!!, its not that eazy to pass buddy (> <)..")

        return result_data

    def is_valid_aadhaar(self, aadhaar_number):
        # Remove any spaces or dashes from the Aadhaar number
        aadhaar_number = aadhaar_number.replace(" ", "").replace("-", "")

        # Check if Aadhaar number is exactly 12 digits
        if len(aadhaar_number) != 12:
            logger.info("called check digit failed")
            return False

        # Check if Aadhaar number consists of only digits
        if not aadhaar_number.isdigit():
            print("called check digit-only failed")
            return False

        # Check if the first digit is between 1 and 9
        if not 1 <= int(aadhaar_number[0]) <= 9:
            print("called check first digit-only failed")
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

        # return True

    # def extract_text(self, image):
    #     pixel_values = self.processor(images=image, return_tensors="pt").pixel_values

    #     generated_ids = self.model.generate(pixel_values)
    #     generated_text = self.processor.batch_decode(
    #         generated_ids, skip_special_tokens=True
    #     )[0]

    #     return generated_text

    def extract_data(self, result_data, cropped_img):
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

        date_pattern = re.compile(r"\d{2}/\d{2}/\d{4}")
        # Print the stored results
        for label, data in result_data.items():
            if names.get(label) == "aadhaar number":
                logger.info("\nFound a adhaar number")
                aadhaar_details = self.data_model.details.aadhaarNumber
                cutout_image = crop_image(
                    cropped_img, data.pop("bounding_box"), padding=10
                )
                text = self.text_extractor.call_ocr_via_api(cutout_image)
                logger.info(text)
                text = re.sub(r"\D+", "", text)
                aadhaar_number = text[:12]
                aadhaar_number = aadhaar_number if len(aadhaar_number) == 12 else ""
                # update data
                aadhaar_details.text = aadhaar_number
                aadhaar_details.confidence = data.pop("confidence_score")
                aadhaar_details.isVerified = self.is_valid_aadhaar(text)
                self.old_data_model["aadhaarNumber"] = aadhaar_number

            if names.get(label) == "vid":
                logger.info("\nProcessing VID...")
                vid_details = self.data_model.details.vid
                cutout_image = crop_image(
                    cropped_img, data.pop("bounding_box"), padding=10
                )
                text = self.text_extractor.call_ocr_via_api(cutout_image)
                logger.info(text)
                text = re.sub(r"\D+", "", text)
                vid = "".join(text.split())
                # update data
                vid_details.text = vid
                vid_details.confidence = data.pop("confidence_score")

            if names.get(label) == "dob":
                logger.info("\nExtracting DOB information")
                dob_details = self.data_model.details.DOB
                cutout_image = crop_image(cropped_img, data.pop("bounding_box"), 10)
                text = date_pattern.search(
                    self.text_extractor.call_ocr_via_api(cutout_image)
                )
                logger.info(text)
                if text:
                    dob = text.group()
                    dob_details.text = dob
                    self.old_data_model["DOB"] = dob
                else:
                    dob_details.text = ""
                dob_details.confidence = data.pop("confidence_score")

            if names.get(label) == "gender":
                logger.info("\nGender Found")
                gender_details = self.data_model.details.gender
                cutout_image = crop_image(
                    cropped_img, data.pop("bounding_box"), padding=10
                )
                gender = self.text_extractor.call_ocr_via_api(cutout_image)
                logger.info(gender)
                if "female" in gender.lower():
                    gender = "FEMALE"
                elif "male" in gender.lower():
                    gender = "MALE"
                else:
                    gender = ""
                gender_details.text = gender
                gender_details.confidence = data.pop("confidence_score")
                self.old_data_model["gender"] = gender

            if names.get(label) == "issue date":
                logger.info("\nExtracting issue date from the card")
                issuesdate_details = self.data_model.details.issueDate
                cutout_image = crop_image(
                    cropped_img, data.pop("bounding_box"), padding=10
                )
                text = self.text_extractor.call_ocr_via_api(cutout_image)
                text = date_pattern.search(text)
                logger.info(text)
                if text:
                    issues_date = text.group()
                    issuesdate_details.text = issues_date
                    self.old_data_model["issueDate"] = issues_date
                else:
                    issuesdate_details.text = ""
                issuesdate_details.confidence = data.pop("confidence_score")

            if names.get(label) == "name":
                logger.info("\nName")
                name_details = self.data_model.details.name
                cutout_image = crop_image(cropped_img, data.pop("bounding_box"), 10)
                raw_text = self.text_extractor.call_ocr_via_api(cutout_image)
                name = process_name(raw_text)
                logger.info(name)
                name_details.text = name
                name_details.confidence = data.pop("confidence_score")
                self.old_data_model["name"] = name

            if names.get(label) == "photo":
                logger.info("It has a photo")
                self.data_model.details.photo.confidence = data.pop("confidence_score")
