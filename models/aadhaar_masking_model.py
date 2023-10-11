from PIL import ImageDraw
import re
import logging

from models.text_extraction.text_extractor import TextExtractor

logger = logging.getLogger(__name__)


class AadhaarMaskingModel:
    def __init__(self):
        self.text_extractor = TextExtractor()

    def mask_aadhaar(self, image):
        self.text_extractor.call_GCP(image)
        data = self.text_extractor.data
        sents = data[0].description.split("\n")
        aadhaar_numbers = self.find_aadhaar_numbers(sents)

        if not aadhaar_numbers:
            raise Exception("No Aadhaar Number Found")

        masked_image = self.apply_mask(image, data, aadhaar_numbers[0].split()[:2])
        # masked_image.show()
        return masked_image

    def find_aadhaar_numbers(self, data):
        aadhaar_pattern = re.compile(r"\d{4}\s\d{4}\s\d{4}")
        vid_pattern = re.compile(r"\d{4}\s\d{4}\s\d{4}\s\d{4}")
        aadhaar_numbers = []

        for text in data:
            text = vid_pattern.sub("", text)
            matches = aadhaar_pattern.findall(text)
            aadhaar_numbers.extend(matches)

        return aadhaar_numbers

    def apply_mask(self, image, text_data, aadhaar_numbers):
        masked_image = image.copy()
        draw = ImageDraw.Draw(masked_image)

        for text in text_data:
            if text.description.isdigit() and text.description in aadhaar_numbers:
                self.draw_mask_and_symbol(draw, text)

        return masked_image

    def draw_mask_and_symbol(self, draw, text):
        vertex = [(vertex.x, vertex.y) for vertex in text.bounding_poly.vertices]
        draw.rectangle([vertex[0], vertex[2]], fill=(0, 0, 0), width=2)

        # symbol = "xxxx"
        # x_min, y_min = vertex[0]
        # x_max, y_max = vertex[2]
        # box_width, box_height = x_max - x_min, y_max - y_min
        # font_size = max(box_width, box_height) // 2
        # font = ImageFont.truetype("arial.ttf", font_size)
        # text_size = draw.textsize(symbol, font=font)
        # text_x = max(x_min, (x_min + x_max - text_size[0]) // 2)
        # text_y = max(y_min, y_min) - 20
        # draw.text((text_x, text_y), symbol, fill=(0, 0, 0), font=font)
