from app.utils import url_to_img
from .textExtraction.textExtractor import TextExtractor


class ISUOCRModel:
    def __init__(self):
        self.text_extractor = TextExtractor()

    def extract(self, image, lang, oem, psm):
        if image.startswith("http") or image.startswith("https"):
            np_img = url_to_img(image)
        else:
            return {
                "status": -1,
                "message": "Invalid Input it currently accepts URLs Only",
            }
        try:
            config = "-l " + lang + " --oem " + str(oem) + " --psm " + str(psm)
            return self.text_extractor.extract_text(np_img, custom_config=config)
        except Exception as e:
            return str(e)
