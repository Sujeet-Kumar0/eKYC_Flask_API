import os
from ultralytics import YOLO

# from app.config import Config
from controllers import (
    PassportOCRController,
    AadhaarFrontOCRController,
    AadhaarBackOCRController,
    PANOCRController,
    FaceMatchingController,
    AadhaarMaskingController,
    LogsDownloadController,
)
from utils import Path


aadhaar_front_model = YOLO(Path.AADHAAR_FRONT_WEIGHTS_PATH)
aadhaar_back_model = YOLO(Path.AADHAAR_BACK_WEIGHTS_PATH)
pan_model = YOLO(Path.PAN_MODEL)


def create_passport_ocr_controller():
    segment_model = YOLO(Path.SEGMENTATION_MODEL)
    passport_model = YOLO(
        Path.PASSPORT_MODEL
    )  # Instantiate the PassportModel class with appropriate arguments
    return PassportOCRController(segment_model, passport_model)


def create_aadhaar_front_ocr_controller():
    segementation_model = "YOLO(Path.SEGMENTATION_MODEL)"
    return AadhaarFrontOCRController(aadhaar_front_model, segementation_model)


def create_aadhaar_back_ocr_controller():
    segementation_model = "YOLO(Path.SEGMENTATION_MODEL)"
    return AadhaarBackOCRController(aadhaar_back_model, segementation_model)


def create_pan_ocr_controller():
    segementation_model = "YOLO(Path.SEGMENTATION_MODEL)"
    return PANOCRController(pan_model, segementation_model)


def create_face_matching():
    return FaceMatchingController()


def create_aadhaar_masking_controller():
    return AadhaarMaskingController()


def create_logs_controller():
    folder_path = os.path.abspath("logs")
    zip_path = folder_path + "\logs.zip"
    return LogsDownloadController(folder_path=folder_path, temp_zip_path=zip_path)
