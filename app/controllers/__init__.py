from .AadhaarBackOCRControllers import AadhaarBackOCRController
from .AadhaarFrontOCRControllers import AadhaarFrontOCRController
from .AadhaarMaskingControllers import AadhaarMaskingController
from .FaceMatchingController import FaceMatchingController
from .ISUOCRController import ISUOCRController
from .panOCRControllers import PANOCRController

__all__ = [
    "AadhaarFrontOCRController",
    "AadhaarBackOCRController",
    "FaceMatchingController",
    "PANOCRController",
    "ISUOCRController",
    "AadhaarMaskingController",
]
