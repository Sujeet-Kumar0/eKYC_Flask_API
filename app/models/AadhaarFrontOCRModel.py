from app.utils import TextFileManager
from app.utils import URL_Type
from app.utils import base64_to_img
from app.utils import url_to_img
from .FilterAadhaarFrontData import read_aadhaar_front_data
from .preProcessor.imagePreProcessor import ImagePreprocessor
from .textExtraction.textExtractor import TextExtractor


class AadhaarFrontOCRModel:

    def __init__(self):
        # self.image_preprocessor = ImagePreprocessor()
        self.text_extractor = TextExtractor()
        self.text_file_manager = TextFileManager()

    def extract_image(self, image):
        # print(image)
        url_type = URL_Type.check(image)
        if url_type == URL_Type.UrlType.URL:
            np_img = url_to_img(image)
        elif url_type == URL_Type.UrlType.BASE64:
            np_img = base64_to_img(image)
        elif url_type == URL_Type.UrlType.NUMPY:
            np_img = image
        else:
            return {
                "status": -1,
                "message": "Invalid Input it accepts URLs,Base64 Only",
            }

        # # image pre processing
        # try:
        #     # processed_image = image_preprocessor(np_img)
        #     preprocessor = ImagePreprocessor(np_img)
        #     preprocessor.check_image_size()
        #     preprocessor.resize_image()
        #     preprocessor.convert_to_grayscale()
        #     preprocessor.check_image_blurriness()
        #     preprocessor.perform_otsu_threshold()
        #     # preprocessor.improve_image_quality()
        #     processed_image = preprocessor.threshold

        #     # # Find contours
        #     # contours, hierarchy = cv2.findContours(processed_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        #     # # Draw contours on original image
        #     # img_with_contours = cv2.drawContours(np_img, contours, -1, (0, 255, 0), 2)

        #     # # Show image
        #     # cv2.imshow('Image with Contours', img_with_contours)
        #     # cv2.waitKey(0)
        #     # cv2.destroyAllWindows()
        # except Exception as e:
        #     return {
        #         "status": -1,
        #         "message": "Sorry!, Please recapture the image again.",
        #         "code": "IPPC",
        #         "devMsg": str(e.args),
        #     }

        # Text Extraction
        raw_text = self.text_extractor.extract_text(
            np_img, custom_config=r"-l eng\+ben\+guj\+hin\+kan\+mal\+ori\+pan\+tam\+tel")

        try:
            data = read_aadhaar_front_data(raw_text)
            if data["aadhaarNumber"] == "" or data["gender"] == "":
                raw_text = self.text_extractor.extract_text(
                    np_img  # , custom_config=r"-l eng\+ori\+kan\+tel\+hin"
                )
                data = read_aadhaar_front_data(raw_text)
                if data["aadhaarNumber"] == "" or data["gender"] == "":
                    preprocessor = ImagePreprocessor(np_img)
                    preprocessor.check_image_size()
                    preprocessor.resize_image()
                    preprocessor.convert_to_grayscale()
                    preprocessor.check_image_blurriness()
                    preprocessor.perform_otsu_threshold()
                    # preprocessor.improve_image_quality()
                    processed_image = preprocessor.threshold
                    # Text Extraction
                    raw_text = self.text_extractor.extract_text(
                        processed_image,
                        custom_config=r"-l eng\+ben\+guj\+hin\+kan\+mal\+ori\+pan\+tam\+tel --psm 1",
                    )
                    data = read_aadhaar_front_data(raw_text)
                    if data["aadhaarNumber"] == "":
                        preprocessor.improve_image_quality()
                        processed_image = preprocessor.threshold
                        raw_text = self.text_extractor.extract_text(
                            processed_image,
                            custom_config=r"-l eng\+ben\+guj\+hin\+kan\+mal\+ori\+pan\+tam\+tel --psm 1",
                        )
                        data = read_aadhaar_front_data(raw_text)
        except Exception as e:
            return {
                "status": -1,
                "message": "Sorry!, Please recapture the image again.",
                "code": "FCC",
                "devMsg": str(e.args),
            }

        # to_unicode = str
        # # data = to_unicode(data)

        # output_data = to_unicode(json.dumps(data,indent=4,sort_keys=True,separators=(",", ": "),ensure_ascii=False,))
        # # use the textfilemanager to write the text to a file
        # file_path = "./outputs/info.json"
        # self.text_file_manager.write_text_to_file(output_data, file_path)
        # # use the textfilemanager to read the text from the file
        # text_from_file = self.text_file_manager.read_text_from_file(file_path)
        # print(text_from_file)

        if data["aadhaarNumber"] == "":
            return {
                "status": -1,
                "message": "Sorry!, Please recapture the image again.",
                "devMsg": "NO AADHAAR number found throught string",
            }

        # data = json.JSONEncoder(sort_keys=True, ensure_ascii=False).encode(data)
        return {
            "status": 0,
            "data": data,
            "message": "Data retrieved successful"
        }
