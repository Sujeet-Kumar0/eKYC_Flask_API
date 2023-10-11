from controllers.passport_ocr_controller import PassportOCRController
from controllers.aadhaar_front_ocr_controllers import AadhaarFrontOCRController
from controllers.aadhaar_back_ocr_controllers import AadhaarBackOCRController
from .pan_ocr_controllers import PANOCRController
from .face_matching_controllers import FaceMatchingController
from .aadhaar_masking_controllers import AadhaarMaskingController
from .logs_download_controllers import LogsDownloadController
from .o_c_r_controller import OCRController
from controllers.factory import (
    create_pan_ocr_controller,
    create_passport_ocr_controller,
    create_aadhaar_back_ocr_controller,
    create_aadhaar_front_ocr_controller,
    create_face_matching,
    create_aadhaar_masking_controller,
    create_logs_controller,
)

__all__ = [
    "create_pan_ocr_controller",
    "create_passport_ocr_controller",
    "create_aadhaar_back_ocr_controller",
    "create_aadhaar_front_ocr_controller",
    "create_face_matching",
    "create_aadhaar_masking_controller",
    "create_logs_controller",
]
