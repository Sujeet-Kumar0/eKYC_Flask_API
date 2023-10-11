import os


class Path:
    ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    RELATIVE_WEIGHTS_PATH = "weights/segementation_weights.pt"

    SEGMENTATION_MODEL = os.path.join(ROOT_DIR, RELATIVE_WEIGHTS_PATH)

    PAN_MODEL = os.path.join(ROOT_DIR, "weights/best3.pt")

    PASSPORT_MODEL = os.path.join(ROOT_DIR, "weights/passport_weights.pt")

    AADHAAR_FRONT_WEIGHTS_PATH = os.path.join(ROOT_DIR, "weights/best.pt")

    AADHAAR_BACK_WEIGHTS_PATH = os.path.join(ROOT_DIR, "weights/best2.pt")

    STATES_JSON = os.path.join(ROOT_DIR, "states.json")

    CLASSIFICATION_MODEL = os.path.join(ROOT_DIR, "weights/classification.pt")


class STRING:
    PLZ_TRY = "Please try again"

    CLASSIFICATION_DEV_MSG = "Unable to classify {}."

    CLASSIFICATION_MESSAGE = "Please upload proper {} card."

    IMAGE_PROCESSING_ERROR = "Unsupported Image, resulted None"

    SEGMENTATION_DEV_MSG = "Segementation/Image Cropping Failed"

    OBJECT_DETECTION_DEV_MSG = "No detection were found"

    OBJECT_DETECTION_MSG = "No information was found in the image. Please Try again."

    CLASSIFICATION_DEV_MSG_FRONT = CLASSIFICATION_DEV_MSG.format("Aadhaar Front")

    CLASSIFICATION_DEV_MSG_BACK = CLASSIFICATION_DEV_MSG.format("Aadhaar Back")

    CLASSIFICATION_DEV_MSG_PAN = CLASSIFICATION_DEV_MSG.format("PAN")

    CLASSIFICATION_MSG_FRONT = CLASSIFICATION_MESSAGE.format("Aadhaar Bottom Front")

    CLASSIFICATION_MSG_BACK = CLASSIFICATION_MESSAGE.format("Aadhaar Bottom Back")

    CLASSIFICATION_MSG_PAN = CLASSIFICATION_MESSAGE.format("PAN")

    SUCCESS_MSG = "Data retrieved successfully"

    WARNING_MSG = "WARNING:JSON response body will be changed soon.Please update the frontend accordingly"
