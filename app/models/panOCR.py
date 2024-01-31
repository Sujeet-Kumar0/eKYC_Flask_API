import os
import re
import shutil

import cv2
import torch

from app.utils import Path, TextFileManager, URL_Type, UrlType, base64_to_img, url_to_img
from . import filterPANData
from .preProcessor.imagePreProcessor import ImagePreprocessor, image_preprocessor
from .textExtraction.textExtractor import TextExtractor


class PANOCRModel:
    # Create instances of the TextExtractor and TextFileManager classes
    def __init__(self, object_detector):
        # self.image_preprocessor = ImagePreprocessor()
        self.text_extractor = TextExtractor()
        self.text_file_manager = TextFileManager()
        self.filter = filterPANData.PANDataReader()
        self.model = object_detector

    def clear_field(self, path):
        result = []
        error = None

        if not os.path.exists(path):
            error = "Path doesn't exist"
        else:
            for (root, _, files) in os.walk(path):
                for f in files:
                    image = cv2.imread(os.path.join(root, f))
                    if image is not None:
                        text = self.text_extractor.extraction(image)
                        result.append(text)
                    else:
                        error = "image is corrupt"

        return result, error

    def clear_dob(self, path):

        return self.clear_field(path)

    def clear_name(self, path):
        return self.clear_field(path)

    def clear_father_name(self, path):
        return self.clear_field(path)

    def clear_pan_number(self, path, image):
        data, error = self.clear_field(path)
        if error is not None:
            self.model(source=image, save_crop=True, hide_labels=True, save_txt=True, box=False, line_thickness=1)
            data, error = self.clear_field(Path.PATHS[3])  # added image argument to the recursive call

        return data, None

    @staticmethod
    def _get_image_from_input(image):
        # im sorry I don't know how switching is done in python
        url_type = URL_Type.check(image)
        if url_type == UrlType.URL:
            np_img = url_to_img(image)
        elif url_type == UrlType.BASE64:
            np_img = base64_to_img(image)
        elif url_type == UrlType.NUMPY:
            np_img = image
        else:
            raise ValueError("Invalid input, it accepts URLs or Base64 only")
        return np_img

    def extract_text(self, image):

        shutil.rmtree("runs", ignore_errors=True)
        try:
            np_img = self._get_image_from_input(image)
        except ValueError as e:
            return {"status": -1, "message": str(e)}

        # image pre-processing
        try:
            preprocessor = ImagePreprocessor(np_img)
            preprocessor.check_image_size()
            preprocessor.resize_image()
            preprocessor.check_brightness()
            preprocessor.convert_to_grayscale()
            preprocessor.check_image_blurriness()
            preprocessor.convert_to_colour()
            processed_image = preprocessor.img

        except Exception as e:
            return {"status": -1, "message": "Sorry!, Please recapture the image again.", "code": "IPPC",
                    "devMesg": str(e.args)}

        self.model.to('cuda' if torch.cuda.is_available() else 'cpu')
        print('cuda' if torch.cuda.is_available() else 'cpu')
        self.model(source=processed_image, save_crop=True, hide_labels=True,
                   save_txt=True, box=False, line_thickness=1, hide_conf=True, conf=0.5)

        paths = Path.PATHS

        og_list = [self.clear_dob(paths[0]), self.clear_name(paths[1]), self.clear_father_name(paths[2]),
                   self.clear_pan_number(paths[3], processed_image)]

        raw_text = []
        for tup in og_list:
            for elem in tup[0]:
                if elem not in raw_text:
                    raw_text.append(elem)
            if tup[1] is not None:
                print(tup[1])

        # print(raw_text)

        # file_path = 'outputs/output.txt'
        # self.text_file_manager.write_text_to_file(str(raw_text), file_path)
        #
        # # Use the TextFileManager to read the text from the file
        # text_from_file = self.text_file_manager.read_text_from_file(file_path)
        # print(text_from_file)

        data = self.filter.read_pan_data(raw_text)

        # Initialize an empty dictionary to store the output
        output_dict = {}

        # Read the contents of the label file into a dictionary
        if os.path.exists(Path.LABEL_PATH):
            with open(Path.LABEL_PATH, "r") as f:
                for line in f:
                    key, *values = map(float, line.split())
                    if key in output_dict:
                        output_dict[key].append([values[:2], values[2:]])
                    else:
                        output_dict[key] = [[values[:2], values[2:]]]

        if output_dict:
            data["labels"] = output_dict

        # to_unicode = str
        # # Use the TextFileManager to write the text to a file
        # file_path = './outputs/info.json'
        # output_file_data = json.dumps(data, indent=4, sort_keys=True, separators=(',', ': '), ensure_ascii=False)
        # self.text_file_manager.write_text_to_file(to_unicode(output_file_data), file_path)

        # # Use the TextFileManager to read the text from the file
        # text_from_file = self.text_file_manager.read_text_from_file(file_path)
        # print(text_from_file)

        if data["pan"] is None:
            try:
                processed_image = image_preprocessor(np_img)
            except Exception as e:
                return {"status": -1, "message": "Sorry!, Please recapture the image again.", "code": "IPPC",
                        "devMesg": str(e.args)}
            # Text Extraction
            raw_text = self.text_extractor.extract_text(processed_image)
            # print(raw_text)
            pan = re.search(r'([A-Z]){5}([O0-9]){4}([A-Z]){1}', raw_text)
            if pan:
                data["pan"] = pan.group()

            else:
                return {"status": -1, "message": "Sorry,Please recapture the PAN Image"}

        # data = json.JSONEncoder(sort_keys=True, ensure_ascii=False).encode(to_unicode(data))
        return {"status": 0, "data": data, "message": "Data retrieved successful"}
