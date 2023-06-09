from Utils import URL_Type
from Utils import UrlType
from Utils import base64_to_img
from Utils import url_to_img
from Utils.TextFileManager import TextFileManager
from models.FilterAadhaarBackData import AadhaarBackDataReader
from models.preProcessor.imagePreProcessor import ImagePreprocessor, image_preprocessor
from models.textExtraction.textExtractor import TextExtractor


class AadhaarBackOCRModel:

    def __init__(self):
        # self.image_preprocessor = ImagePreprocessor()
        self.text_extractor = TextExtractor()
        self.text_file_manager = TextFileManager()
        self.reader = AadhaarBackDataReader()

    def extract_image(self, image):

        data = {
            "address": "",
            "district": "",
            "city": "",
            "state": "",
            "pinCode": "",
            "og_add": "",
            "aadhaarNumber": "",
            "idType": "",
        }

        url_type = URL_Type.check(image)
        if url_type == UrlType.URL:
            np_img = url_to_img(image)
        elif url_type == UrlType.BASE64:
            np_img = base64_to_img(image)
        elif url_type == UrlType.NUMPY:
            np_img = image
        else:
            return {
                "status": -1,
                "message": "Invalid Input it accepts URLs,Base64 Only",
            }

        # image pre processing
        try:
            image_pre_processor = ImagePreprocessor(np_img)
            image_pre_processor.check_image_size()
            image_pre_processor.resize_image()
            image_pre_processor.convert_to_grayscale()
            image_pre_processor.check_image_blurriness()
            image_pre_processor.perform_otsu_threshold()
            # cv2.imshow("sample", processed_image)
            # cv2.waitKey(0)

        except Exception as e:
            return {
                "status": -1,
                "message": "Sorry!, Please recapture the image again.",
                "code": "IPPC",
                "devMesg": str(e.args),
            }

        # Text Extraction
        raw_text = self.text_extractor.extract_text(
            np_img, custom_config=r"-l eng\+ori\+kan\+tel\+hin")

        try:
            data = self.reader.read_aadhaar_back_data(raw_text, data)
            if data["og_add"] == "" or data["state"] == "":
                raw_text = self.text_extractor.extract_text(
                    image_pre_processor.gray_img,
                    custom_config=r"-l eng\+ori\+kan\+tel\+hin --psm 4")

                data = self.reader.read_aadhaar_back_data(raw_text, data)
                if data["og_add"] == "" or data["state"] == "" or data[
                        "district"] == "":
                    raw_text = self.text_extractor.extract_text(
                        image_pre_processor.threshold,
                        custom_config=r"-l eng\+ori\+kan\+tel\+hin --psm 4")

                    data = self.reader.read_aadhaar_back_data(raw_text, data)

            if data["aadhaarNumber"] == "":
                _, bottom = image_pre_processor.divide_half_horizontal()
                processed_image = image_preprocessor(bottom)

                raw_text = self.text_extractor.extract_text(
                    processed_image,
                    # custom_config=r"-l eng\+ori\+kan\+tel\+hin"
                )
                data["aadhaarNumber"] = self.reader.read_aadhaar_Number(
                    raw_text)

        except Exception as e:
            return {
                "status": -1,
                "message": "Sorry!, Please recapture the image again.",
                "devMsg": str(e.args)
            }

        data["aadhaarNumber"] = "".join(data["aadhaarNumber"].split())

        # to_unicode = str
        # output_data = to_unicode(
        #     json.dumps(data,
        #                indent=4,
        #                sort_keys=True,
        #                separators=(',', ': '),
        #                ensure_ascii=False))
        # # Use the TextFileManager to write the text to a file
        # file_path = './outputs/info.json'

        # self.text_file_manager.write_text_to_file(output_data, file_path)

        # # Use the TextFileManager to read the text from the file
        # text_from_file = self.text_file_manager.read_text_from_file(file_path)
        # print(text_from_file)

        if data is None:
            return {
                "status": -1,
                "message": "Sorry!, Please recapture the image again.",
                "devMsg": "No Text Found"
            }

        if data["og_add"] == "":
            return {
                "status": -1,
                "message": "Sorry!, Please recapture the image again.",
                "devMsg": "ther is nothing found in adress.[OG_ADD is Null]"
            }

        # if data["pinCode"] == "":
        #     return {
        #         "status": -1,
        #         "message": "Sorry!, Please recapture the image again.",
        #         "devMsg": "NO PIN CODE FOUND!",
        #     }

        if data["aadhaarNumber"] == "":
            return {
                "status": -1,
                "message": "Sorry!, Please recapture the image again.",
                "devMsg": "This is probably not a Aadhaar Card"
            }

        # data = json.JSONEncoder(ensure_ascii=False, sort_keys=True).encode(to_unicode(data))
        return {
            "status": 0,
            "data": data,
            "message": "Data retrieved successful"
        }
