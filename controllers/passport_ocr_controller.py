import base64
import io
import re
import torch
from io import BytesIO
import requests
from PIL import Image, ImageEnhance, ImageFilter
import torchvision.transforms.functional as F

from data_models import PassportData, ResponseData, PassportBackData, PassportFrontData
from models.text_extraction.text_extractor import TextExtractor
from utils import UrlType, IdType


class PassportOCRController:
    def __init__(self, segment_model, passport_model):
        self.segment_model = segment_model
        self.passport_model = passport_model
        self.text_extractor = TextExtractor()
        self.data = PassportData()

    def get_image(self, image):
        url_type = UrlType.check(image)
        if url_type == UrlType.URL:
            img = Image.open(BytesIO(requests.get(image).content)).convert("RGB")
        elif url_type == UrlType.BASE64:
            img = Image.open(BytesIO(base64.b64decode(image))).convert("RGB")
        else:
            img = None
        return img

    def crop_img(self, image, bbox, padding=0):
        contrast_enhancer = ImageEnhance.Contrast(image)
        image_high_contrast = contrast_enhancer.enhance(1.5)
        image = image_high_contrast.filter(
            ImageFilter.UnsharpMask(radius=1, percent=100)
        )

        # Make a copy of the original image
        cutout_img = image.copy()

        # Define the padding values
        padding_top = padding
        padding_bottom = padding
        padding_left = padding
        padding_right = padding

        # Calculate the new bounding box coordinates with padding
        bbox_with_padding = (
            bbox[0].item() - padding_left,
            bbox[1].item() - padding_top,
            bbox[2].item() + padding_right,
            bbox[3].item() + padding_bottom,
        )

        # Crop the image using the new bounding box coordinates
        cutout_img = F.crop(
            cutout_img,
            bbox_with_padding[1],
            bbox_with_padding[0],
            bbox_with_padding[3] - bbox_with_padding[1],
            bbox_with_padding[2] - bbox_with_padding[0],
        )

        # cutout_img.show()

        return cutout_img

    def process_card_number(self, img, box):
        raw_text = self.text_extractor.extract_text(
            self.crop_img(img, bbox=box, padding=5)
        )
        pattern = r"\n(\d+)"
        matches = re.findall(pattern, raw_text)
        if len(matches) > 0:
            extracted_number = matches[0]
            self.data.details.cardNumber.text = extracted_number
        else:
            self.data.details.cardNumber.text = raw_text

    def process_dob(self, img, box):
        raw_text = self.text_extractor.extract_text(
            self.crop_img(img, bbox=box, padding=5)
        )
        text = re.search(r"\d{2}/\d{2}/\d{4}", raw_text)
        if text:
            self.data.details.DOB.text = text.group()

    def process_expiry_date(self, img, box):
        raw_text = self.text_extractor.extract_text(
            self.crop_img(img, bbox=box, padding=4), custom_config=r"--psm 1"
        )
        text = re.search(r"\b\d{2}/\d{2}/\d{4}\b", raw_text)
        if text:
            self.data.details.expiryDate.text = text.group()

    def process_gender(self, img, box):
        raw_text = self.text_extractor.extract_text(
            self.crop_img(img, bbox=box, padding=5)
        )

        if "F" in raw_text:
            self.data.details.gender.text = "F"
        elif "M" in raw_text:
            self.data.details.gender.text = "M"

    def process_signature(self, img, box):
        signature = self.crop_img(img, bbox=box, padding=-7)
        width, height = signature.size
        signature = signature.crop((0, 30, width, height))
        buffered = io.BytesIO()
        signature.save(buffered, format="PNG")
        image_bytes = buffered.getvalue()

        # Encode bytes as base64 string
        base64_image = base64.b64encode(image_bytes).decode("ascii")
        self.data.details.signature.text = base64_image

    def get_passport_ocr(self, image):
        try:
            img = self.get_image(image)
            if img is None:
                return ResponseData(
                    status=1,
                    message="Given image is unreadable,Please try again",
                    devMsg="the given image isn't readable yet, returned None",
                )
        except Exception as e:
            return ResponseData(
                status=-1, message="Please recapture", code="IIC", devMsg=str(e)
            )

        try:
            self.passport_model.to("cuda" if torch.cuda.is_available() else "cpu")
            # print("cuda" if torch.cuda.is_available() else "cpu")
            results = self.passport_model(source=img, conf=0.5)  # , save=True)
        # className = { 0: "UAE",1: "card number",2: "dob", 3: "emblem",4: "expiry date",
        #     5: "gender",6: "id number",7: "name",8: "nationality",9: "photo",
        #     10: "signature"}

        except Exception as e:
            return ResponseData(
                status=-1,
                message="Please recapture",
                code="MB",
                devMsg=str(e),
                data=self.data,
            )

        backlist = [1, 2, 4, 5, 10]
        backlist_tensor = torch.tensor(backlist).to("cpu")
        cls_tensor = torch.tensor(results[0].boxes.cls).to("cpu")

        if torch.any(cls_tensor.eq(0)) or torch.any(cls_tensor.eq(3)):
            self.data = PassportFrontData()
            self.data.idType = IdType.PASSPORTFRONT.name
        elif torch.any(torch.isin(cls_tensor, backlist_tensor)):
            self.data = PassportBackData()
            self.data.idType = IdType.PASSPORTBACK.name

        # print(results[0].boxes.cls)

        try:
            for box in results[0].boxes:
                # print(results[0].names.get(int(box.cls[0])))
                # print("confidence: " + str(box.conf))
                # print(box)
                x1, y1, x2, y2 = box.xyxy[0]
                x1, x2, y1, y2 = int(x1), int(x2), int(y1), int(y2)

                if int(box.cls[0]) == 1:
                    self.data.details.cardNumber.confidence = round(box.conf.item(), 2)
                    self.process_card_number(img, box.xyxy[0])

                elif int(box.cls[0]) == 2:
                    self.data.details.DOB.confidence = round(box.conf.item(), 2)
                    self.process_dob(img, box.xyxy[0])

                elif int(box.cls[0]) == 4:
                    self.data.details.expiryDate.confidence = round(box.conf.item(), 2)
                    self.process_expiry_date(img, box.xyxy[0])

                elif int(box.cls[0]) == 5:
                    self.data.details.gender.confidence = round(box.conf.item(), 2)
                    self.process_gender(img, box.xyxy[0])

                elif int(box.cls[0]) == 6:
                    self.data.details.idNumber.confidence = round(box.conf.item(), 2)
                    raw_text = self.text_extractor.extract_text(
                        self.crop_img(img, bbox=box.xyxy[0])
                    )
                    self.data.details.idNumber.text = raw_text

                elif int(box.cls[0]) == 7:
                    self.data.details.name.confidence = round(box.conf.item(), 2)
                    raw_text = self.text_extractor.extract_text(
                        self.crop_img(img, bbox=box.xyxy[0])
                    )
                    self.data.details.name.text = raw_text

                elif int(box.cls[0]) == 8:
                    self.data.details.nationality.confidence = round(box.conf.item(), 2)
                    raw_text = self.text_extractor.extract_text(
                        self.crop_img(img, bbox=box.xyxy[0])
                    )
                    self.data.details.nationality.text = raw_text
                elif int(box.cls[0]) == 9:
                    self.data.details.photo.confidence = round(box.conf.item(), 2)
                    photo = self.crop_img(img, bbox=box.xyxy[0], padding=-7)
                    width, height = photo.size
                    photo = photo.crop((0, 30, width, height))
                    buffered = io.BytesIO()
                    photo.save(buffered, format="PNG")
                    image_bytes = buffered.getvalue()

                    # Encode bytes as base64 string
                    base64_image = base64.b64encode(image_bytes).decode("ascii")
                    self.data.details.photo.text = base64_image

                elif int(box.cls[0]) == 10:
                    self.data.details.signature.confidence = round(box.conf.item(), 2)
                    self.process_signature(img, box.xyxy[0])

        except Exception as e:
            return ResponseData(
                status=-1,
                devMsg=str(e),
                message="Please try again",
                data=self.data.to_dict(),
            )

        return ResponseData(
            status=0, data=self.data.to_dict(), message="Data retrieved successfully"
        )
