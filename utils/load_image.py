from PIL import Image
import base64
import requests
from io import BytesIO

from utils import UrlType


class ImageLoader:
    def __init__(self):
        self.url_type = None

    def load_image(self, input):
        self.url_type = UrlType.check(input)
        if self.url_type == UrlType.URL:
            return self._url_to_image(input)
        elif self.url_type == UrlType.BASE64:
            return self._base64_to_image(input)
        elif self.url_type == UrlType.FILE:
            return self._file_to_image(input)
        else:
            raise Exception("unprocessable entity")

    def _url_to_image(self, url):
        image_content = self._get_url_content(url)
        return self._open_image(image_content)

    def _base64_to_image(self, data):
        encoded_data = data.split(",")[1]
        base64_decoded = base64.b64decode(encoded_data)
        return self._open_image(base64_decoded)

    def _get_url_content(self, url):
        response = requests.get(url)
        return response.content if response.ok else None

    def _open_image(self, content):
        image_bytes = BytesIO(content) if content else None
        return Image.open(image_bytes).convert("RGB")

    def _file_to_image(self, file):
        file_content = file.read()
        return self._open_image(file_content)
