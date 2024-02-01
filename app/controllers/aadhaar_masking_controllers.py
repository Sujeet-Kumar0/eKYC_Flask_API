import base64

import cv2
import numpy as np
import requests

from app.models import AadhaarMaskingModel
from app.utils import URL_Type
from app.utils import UrlType


class AadhaarMaskingController:

    def __init__(self):
        self.model = AadhaarMaskingModel()

    def get_aadhaar_masking(self, image):
        """
        This method is used to get the aadhaar masking result
        :param image: image base64 encoded
        :return:
        """
        url_type = URL_Type.check(image)
        if url_type == UrlType.URL:
            response = requests.get(image)
            img_array = np.array(
                bytearray(response.content),
                dtype=np.uint8)  # Convert the image array to an OpenCV image

        elif url_type == UrlType.BASE64:
            encoded_data = image.split(",")[1]
            base64_decoded = base64.b64decode(encoded_data)
            img_array = np.array(bytearray(base64_decoded), dtype=np.uint8)

        elif url_type == UrlType.NUMPY:
            img_array = image

        else:
            return {
                "status": -1,
                "message": "Invalid Input it accepts URLs,Base64 Only",
                "code": "INA"
            }

        try:
            img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

            masked_image = self.model.imgprocess(img)

            # cv2.imwrite("imshow.jpg", masked_image)
            # with open("imshow.jpg", "rb") as img_file:
            #     my_string = base64.b64encode(img_file.read())

            _, im_arr = cv2.imencode(
                ".jpg",
                masked_image)  # im_arr: image in Numpy one-dim array format.
            # im_bytes = im_arr.tobytes()
            my_string = base64.b64encode(im_arr)

            # my_string = base64.encodebytes(masked_image)

            return {
                "status": 0,
                "message": "Image Masked Successfully",
                "image": str(my_string)[2:-1],
            }
        except Exception as e:
            return {
                "status": -1,
                "message": "Sorry!, unable to process image.Please recapture and try again",
                "image": "",
                "devMsg": str(e),
                "code": "MB"
            }
