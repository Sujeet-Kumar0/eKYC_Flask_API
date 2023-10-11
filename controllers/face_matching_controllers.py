import logging
from concurrent.futures import ThreadPoolExecutor, TimeoutError
import numpy as np
from models.facematching_a_w_s_model import FaceMatchingAWSModel
from data_models import ResponseData
from models import aadhaar_model
from models.facematching_own_model import FaceMatchingModel
from utils import ImageLoader, UrlType

logger = logging.getLogger(__name__)


class FaceMatchingController:
    def __init__(self):
        self.image_loader = ImageLoader()
        self.model1 = FaceMatchingModel()
        self.model2 = FaceMatchingAWSModel()

    def process_image2(self, image):
        image_data = self.image_loader.load_image(image)
        photo = aadhaar_model.get_photo(image_data)
        return photo

    def verify(self, image1, image2, deepface={}, useAWS=None, photo_provided=False):
        try:
            img1 = UrlType.check(image1)
            img2 = UrlType.check(image2)
            if img1 is UrlType.NONE or img2 is UrlType.NONE:
                logger.error("Unprocessable image")
                responce = ResponseData(
                    status=-1,
                    devMsg="Invalid input: Inputs should be either Base64 or Url",
                    code="IIC",
                )
                logger.error("Error:Responce " + str(responce))
                return responce
        except Exception as e:
            logger.error(e.args)
            return ResponseData(status=-1, devMsg=str(e), code="IIC")

        result = {}
        with ThreadPoolExecutor() as executor:
            try:
                image_plw1 = executor.submit(self.image_loader.load_image, image1)
                if photo_provided:
                    image_plw2 = executor.submit(self.image_loader.load_image, image2)
                else:
                    image_plw2 = executor.submit(self.process_image2, image2)

                img1 = image_plw1.result()
                img2 = image_plw2.result()

                if useAWS != True:
                    result = executor.submit(
                        self.model1.call_deepface,
                        np.array(img1),
                        np.array(img2),
                        deepFace=deepface,
                    ).result(timeout=5)
                    result.update(
                        {"confidence": float(result.get("verified", 0) * 100)}
                    )

                    if result.get("verified") is False:
                        logger.info("Image verified false")

                        result = {}
                        responce = executor.submit(
                            self.model2.call_aws_compare_faces,
                            source_file=img1,
                            target_file=img2,
                        ).result()

                        result["verified"] = bool(len(responce["FaceMatches"]))
                        result["confidence"] = (
                            round(float(responce["FaceMatches"][0]["Similarity"]), 2)
                            if bool(len(responce["FaceMatches"]))
                            else 0.0
                        )
                else:
                    result = {}
                    responce = executor.submit(
                        self.model2.call_aws_compare_faces,
                        source_file=img1,
                        target_file=img2,
                    ).result()

                    result["verified"] = bool(len(responce["FaceMatches"]))
                    result["confidence"] = (
                        round(float(responce["FaceMatches"][0]["Similarity"]), 2)
                        if bool(len(responce["FaceMatches"]))
                        else 0.0
                    )

            except TimeoutError:
                logger.info("Image verification failed or timed out")

                result = {}
                responce = executor.submit(
                    self.model2.call_aws_compare_faces,
                    source_file=img1,
                    target_file=img2,
                ).result()

                result["verified"] = bool(len(responce["FaceMatches"]))
                result["confidence"] = (
                    round(float(responce["FaceMatches"][0]["Similarity"]), 2)
                    if bool(len(responce["FaceMatches"]))
                    else 0.0
                )
            except Exception as e:
                logger.exception(str(e))
                return ResponseData(status=-1, devMsg=str(e), code="IC")

        logger.info("LOG:result %s", str(result))
        return ResponseData(status=0, message="Operation performed.!", data=result)
