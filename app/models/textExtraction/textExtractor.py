import ftfy
import pytesseract

from app.models.preProcessor.imagePreProcessor import ImagePreprocessor
from app.utils import OSType, TextFileManager


class TextExtractor:
    def __init__(self):
        if OSType.get_os_type() == OSType.WIN:
            pytesseract.pytesseract.tesseract_cmd = (r"C:/Program Files/Tesseract-OCR/tesseract")

        self._fixer = ftfy
        self.text_file_manager = TextFileManager()

    def read_write_into_external_file(self, text):
        # Use the TextFileManager to write the text to a file
        file_path = "./outputs/output.txt"
        self.text_file_manager.write_text_to_file(text, file_path)

        # Use the TextFileManager to read the text from the file
        text_from_file = self.text_file_manager.read_text_from_file(file_path)
        print(text_from_file)

    def _fix_text(self, text):
        text = self._fixer.fix_text(text)
        text = self._fixer.fix_encoding(text)

        return text

    def extract_text(self, processed_image, custom_config=""):
        # custom_config = r'-l eng\+ori\+kan\+tel\+hin --psm 1'
        print(pytesseract.get_tesseract_version())
        text = pytesseract.image_to_string(processed_image, config=custom_config)

        text = self._fix_text(text)

        # self.read_write_into_external_file(text)

        return text

    def extraction(self, image):
        image_processing = ImagePreprocessor(image)
        image_processing.convert_to_grayscale()
        image_processing.perform_otsu_threshold()
        image_processing.remove_small_objects()
        image_processing.erode_image()
        final_image = image_processing.threshold
        # cv2.imshow("Final OCR", final_image)
        # cv2.waitKey(0)
        text = self.extract_text(final_image)

        return text
