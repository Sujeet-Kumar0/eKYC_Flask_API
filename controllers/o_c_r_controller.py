import logging
import torch
import gc

from data_models import ResponseData, AadhaarFrontModel, AadhaarBackModel, PANDataModel
from models.classify_model import Classification_Model
from models.segmentation_model import SegmentationModel
from models.text_extraction import TextExtractor
from utils import STRING, IdType, ImageLoader

logger = logging.getLogger(__name__)

torch.cuda.empty_cache()
gc.enable()


class OCRController:
    def __init__(self, model, idType):
        self.model = model
        self.idType: IdType = idType
        self.segmentation_model = SegmentationModel()
        self.classification_model = Classification_Model()
        self.image_loader = ImageLoader()
        self.text_extractor = TextExtractor()

    def __del__(self):
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        gc.collect()

    def process_results(self, results):
        raise NotImplementedError("Subclasses should implement this method.")

    def extract_data(self, result_data, cropped_img):
        raise NotImplementedError("Subclasses should implement this method.")

    def _id_map(self):
        idType_map = {
            IdType.AADHAARFRONT: (
                STRING.CLASSIFICATION_DEV_MSG_FRONT,
                STRING.CLASSIFICATION_MSG_FRONT,
                AadhaarFrontModel(),
                1,
                0,
            ),
            IdType.AADHAARBACK: (
                STRING.CLASSIFICATION_DEV_MSG_BACK,
                STRING.CLASSIFICATION_MSG_BACK,
                AadhaarBackModel(),
                0,
                0,
            ),
            IdType.PAN: (
                STRING.CLASSIFICATION_DEV_MSG_PAN,
                STRING.CLASSIFICATION_MSG_PAN,
                PANDataModel(),
                2,
                1,
            ),
        }
        return idType_map.get(self.idType)

    async def main(self, image, classification=True, segmentation=True):
        try:
            image = self.image_loader.load_image(image)
        except Exception as e:
            logger.error("Exception occurred", exc_info=True)
            yield ResponseData(status=-1, devMsg=str(e), code="IIC")
            return

        self.data_model = self._id_map()[2]
        self.data_model.idType = self.idType.name

        if classification and (
            self.classification_model.call_classification_model(image)
            != self._id_map()[3]
        ):
            yield ResponseData(
                status=-1,
                devMsg=self._id_map()[0],
                message=self._id_map()[1],
            )
            return

        if segmentation:
            cropped_img, confidence = self.segmentation_model.segment_image(
                image, self._id_map()[4]
            )

            if cropped_img is None:
                yield ResponseData(
                    status=-1,
                    devMsg=STRING.SEGMENTATION_DEV_MSG,
                )
                return

            self.data_model.confidence = confidence
        else:
            cropped_img = image
        # cropped_img = Resize((640, 640))(cropped_img)

        results = self.model(source=cropped_img)

        result_data = self.process_results(results)

        if not result_data:
            yield ResponseData(
                status=-1,
                devMsg=STRING.OBJECT_DETECTION_DEV_MSG,
                message=STRING.OBJECT_DETECTION_MSG,
            )
            return

        self.extract_data(result_data, cropped_img)

        data = self.data_model.to_dict()
        data.update(self.old_data_model)

        del self.data_model
        del image
        del results
        del cropped_img

        logger.info("LOG: data: %s", data)

        yield ResponseData(
            status=0,
            message=STRING.SUCCESS_MSG,
            data=data,
            devMsg=STRING.WARNING_MSG,
        )
