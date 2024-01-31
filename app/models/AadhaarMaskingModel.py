import re

import cv2
import numpy as np
import pytesseract
from pytesseract import Output


class AadhaarMaskingModel:

    def __init__(self):
        self.aadhaar_pattern = re.compile(r'\d{4}\s\d{4}\s\d{4}')

    def imgprocess(self, img):

        # basic operation on image.
        # this is used check wether the image contains aadhaar number
        # if ssadhar number is not found it will raise an exception
        try:
            text = pytesseract.image_to_string(img)
            aadhaar_number = self.aadhaar_pattern.search(text).group()
        except:

            image = img
            kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
            img = cv2.filter2D(src=image, ddepth=-1, kernel=kernel)
            text = pytesseract.image_to_string(img)

            # Use regular expressions to extract the Aadhaar number
            aadhaar_number = self.aadhaar_pattern.search(text).group() or ""

        # From here it masking process starts.
        # This function returns data such as coordinates of text
        d = pytesseract.image_to_data(img, output_type=Output.DICT)

        # aadhaar number with two indices ar split into two group
        anum = aadhaar_number.split()
        img = np.array(img)

        for i in range(len(d['text'])):
            if d['text'][i].isdigit():
                if d['text'][i] == anum[0]:
                    x, y, w, h = d['left'][i], d['top'][i], d['width'][i], d['height'][i]
                    # mask the image.
                    _img = cv2.rectangle(img, (x, y), (x + w, y + h), (1, 1, 1), -1)
                elif d['text'][i] == anum[1]:
                    x1, y1, w1, h1 = d['left'][i], d['top'][i], d['width'][
                        i], d['height'][i]
                    _img = cv2.rectangle(img, (x1, y1), (x1 + w1, y1 + h1),
                                         (1, 1, 1), -1)
        return _img
