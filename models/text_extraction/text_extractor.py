import base64
from concurrent.futures import ThreadPoolExecutor
import io
import logging
from google.cloud import vision
import requests
from PIL import Image


logger = logging.getLogger(__name__)


class TextExtractor:
    def __init__(self):
        pass

    def _image_to_bytes(self, image):
        image_bytes = io.BytesIO()
        image.save(image_bytes, format="JPEG")
        image_bytes.seek(0)
        return image_bytes.read()

    def _image_to_base64(self, image):
        byte_stream = io.BytesIO()
        image.save(byte_stream, format="JPEG")
        byte_stream_value = byte_stream.getvalue()
        return base64.b64encode(byte_stream_value).decode("utf-8")

    def call_GCP(self, image):
        logger.info("\ncalled GCP OCR")
        content = self._image_to_bytes(image)
        client = vision.ImageAnnotatorClient()

        image = vision.Image(content=content)

        response = client.text_detection(image=image)
        texts = response.text_annotations
        self.data = texts
        # print("Texts:")

        # for text in texts:
        #     print(f'\n"{text.description}"')

        #     vertices = [
        #         f"({vertex.x},{vertex.y})" for vertex in text.bounding_poly.vertices
        #     ]

        #     print("bounds: {}".format(",".join(vertices)))

        if response.error.message:
            logger.error("Error: {}".format(response.error.message))
            raise Exception(
                "{}\nFor more info on error messages, check: "
                "https://cloud.google.com/apis/design/errors".format(
                    response.error.message
                )
            )

        return texts[0].description if texts and texts[0].description != "" else ""

    def call_ocr_via_api(self, image):
        data = []
        base64_string = self._image_to_base64(image)
        json_payload = {"input": base64_string}
        logger.info(json_payload)
        with ThreadPoolExecutor() as executor:
            try:
                response = executor.submit(
                    requests.post,
                    url="http://172.16.3.215:8080/isuocr",
                    json=json_payload,
                ).result()
            except Exception as e:
                logger.error(
                    "Error in AWS OCR: " + str(e),
                    stack_info=True,
                )
                pass
        response_json = response.json()
        for block in response_json["Blocks"]:
            if block["BlockType"] == "LINE":
                data.append(block["Text"])
        data = " ".join(data)
        data = data.replace(".", "")
        # response = requests.post("http://172.16.3.215:8080/isuocr", json=json_payload)
        logger.info(data)
        return data


# if __name__ == "__main__":
#     textExtractor = TextExtractor()

#     data = textExtractor.call_ocr_via_api(
#         image=Image.open("C:\\Users\\Sujeet\\Downloads\\418.png")
#     )

#     print(data)
