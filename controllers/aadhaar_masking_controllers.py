import base64
import io
from PIL import Image
from data_models import ResponseData
from models.aadhaar_masking_model import AadhaarMaskingModel

from utils import ImageLoader

import logging

logger = logging.getLogger(__name__)


class AadhaarMaskingController:
    def __init__(self):
        self.model = AadhaarMaskingModel()
        self.image_loader = ImageLoader()

    def get_aadhaar_masking(self, image):
        """
        This method is used to get the aadhaar masking result
        :param image: image base64 encoded
        :yield:
        """
        try:
            img = self.image_loader.load_image(image)
        except Exception as e:
            yield ResponseData(status=-1, devMsg=str(e))
            return

        try:
            masked_image = self.model.mask_aadhaar(img)
            aspect_ratio = masked_image.height / masked_image.width
            target_height = 300
            target_width = int(target_height / aspect_ratio)
            masked_image = masked_image.resize(
                (target_width, target_height), Image.ANTIALIAS
            )

            # Create an in-memory byte stream
            byte_stream = io.BytesIO()

            # Convert PIL Image to JPEG and save it to the byte stream
            masked_image.save(byte_stream, format="JPEG")

            # Retrieve the byte stream value
            byte_stream_value = byte_stream.getvalue()

            # Encode byte stream as base64
            my_string = base64.b64encode(byte_stream_value).decode("utf-8")

            yield ResponseData(
                status=0,
                message="Image Masked Successfully",
                data={"image": my_string},
            )
            return
        except Exception as e:
            logger.error("Exception occurred: " + str(e))
            yield ResponseData(
                status=-1,
                message="Sorry!, unable to process image.Please recapture and try again",
                devMsg=str(e),
                code="MB",
            )
            return
