import io
import boto3
import logging

logger = logging.getLogger(__name__)


class FaceMatchingAWSModel:
    def __init__(self):
        self.client = boto3.client("rekognition")

    # I have no idea what going on here i just googled this.
    def _image_to_bytes(self, image):
        image_bytes = io.BytesIO()
        image.save(image_bytes, format="JPEG")
        image_bytes.seek(0)
        return image_bytes.read()

    def call_aws_compare_faces(self, source_file, target_file):
        logger.info("Calling AWS Model")
        source_bytes = self._image_to_bytes(source_file)
        target_bytes = self._image_to_bytes(target_file)

        response = self.client.compare_faces(
            SourceImage={"Bytes": source_bytes}, TargetImage={"Bytes": target_bytes}
        )

        # for faceMatch in response["FaceMatches"]:
        #     position = faceMatch["Face"]["BoundingBox"]
        #     similarity = str(faceMatch["Similarity"])
        #     logger.info(
        #         "The face at "
        #         + str(position["Left"])
        #         + " "
        #         + str(position["Top"])
        #         + " matches with "
        #         + similarity
        #         + "% confidence"
        #     )

        return response
