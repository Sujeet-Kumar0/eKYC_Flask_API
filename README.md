# eKYC Flask API

**Target Audience:** Experienced computer vision developers preparing to productionize a YOLO-based object detection and OCR pipeline for document KYC automation.

---

## Navigation

- [1. Overview](#1-overview)
- [2. YOLO Object Detection Implementation](#2-yolo-object-detection-implementation)
  - [2.1. Architecture & Model Details](#21-architecture--model-details)
  - [2.2. YOLO Pipeline Components](#22-yolo-pipeline-components)
  - [2.3. Integration Points](#23-integration-points)
- [3. Code Structure & Organization](#3-code-structure--organization)
- [4. Dependency Mapping](#4-dependency-mapping)
- [5. System Architecture Diagram](#5-system-architecture-diagram)
- [6. Training and Inference Pipelines](#6-training-and-inference-pipelines)
- [7. Code Quality Analysis](#7-code-quality-analysis)
- [8. Technical Recommendations](#8-technical-recommendations)
- [9. Production Readiness Checklist](#9-production-readiness-checklist)

---

## 1. Overview

This repository implements eKYC workflows for Indian documents (Aadhaar, PAN) using:
- **YOLO-based object detection** (using `ultralytics` YOLO, likely v8)
- **Tesseract OCR**
- **Document-specific data parsing and extraction**
- **Flask API server** for model serving and HTTP endpoints

---

## 2. YOLO Object Detection Implementation

### 2.1. Architecture & Model Details

- **Library Used:** [ultralytics](https://github.com/ultralytics/ultralytics) YOLO, likely YOLOv8 (based on import style).
- **Invocation:** 
  ```python
  from ultralytics import YOLO
  self.object_detector = YOLO(Path.MODEL)
  ```
- **Backbone:** The YOLO model's backbone is implicitly chosen by the weights file at `Path.MODEL`. The code does not explicitly specify architecture (e.g., CSPDarknet, etc.), but YOLOv8 uses a custom backbone.
- **Detection Heads & Anchors:** Managed internally by `ultralytics` YOLO. Anchor strategies (anchor-free by default in YOLOv8) are not customized in code.
- **Model Loading:** Model weights are loaded via `Path.MODEL`.

#### YOLO-Driven Flow
- Images are preprocessed and passed through the YOLO model for object detection (e.g., PAN card region localization).
- Detected regions are used for downstream OCR.

### 2.2. YOLO Pipeline Components

- **Data Augmentation:** Not explicit in code; likely handled via Ultralytics YOLO CLI/training scripts (if used—**no training scripts are present in this repo**).
- **Loss Functions:** Managed by Ultralytics YOLO library; **not custom-coded** here.
- **Non-Maximum Suppression (NMS):** Handled inside YOLO inference (`self.model(source=processed_image, ...)`)—no custom NMS code.
- **Confidence Thresholding:** Set via YOLO model parameters (not explicit in code—defaults apply).
- **Image Preprocessing:** See `ImagePreprocessor` class:
  - Size checks, resizing, grayscale conversion, blurriness checking, Otsu thresholding, morphological operations (open/close).
  - Code Example:
    ```python
    preprocessor = ImagePreprocessor(np_img)
    preprocessor.check_image_size()
    preprocessor.resize_image()
    preprocessor.convert_to_grayscale()
    preprocessor.check_image_blurriness()
    preprocessor.perform_otsu_threshold()
    ```
- **Bounding Box Decoding/Visualization:** Managed by YOLO/Ultralytics; bounding boxes may be used to crop regions for OCR.

### 2.3. Integration Points

| Asset                  | Code Reference / Path           | Description                                      |
|------------------------|---------------------------------|--------------------------------------------------|
| YOLO Model Weights     | `Path.MODEL`                    | Model file for YOLO object detection             |
| YOLO Inference         | `ultralytics.YOLO`              | Called in `PANOCRController` for detection       |
| Config Files           | Not present                     | Model config is internal to weights; no .yaml    |
| Class Definitions      | `TextExtractor`, `ImagePreprocessor` | Region cropping, text extraction, etc.      |
| Output Formats         | JSON via Flask API              | API endpoints return extracted text, status, etc.|

---

## 3. Code Structure & Organization

```
eKYC_Flask_API/
├── app/
│   ├── controllers/       # Flask controllers incl. YOLO object detection interface
│   ├── models/            # OCR, detection, data parsing, preprocessing
│   │   ├── preProcessor/      # Image preprocessing (resize, threshold, etc.)
│   │   ├── textExtraction/    # Text extraction logic (Tesseract interface)
│   │   ├── textCleaner/       # Text cleaning utilities
│   │   ├── FilterAadhaarBackData.py  # Aadhaar-specific data postprocessing
│   │   └── panOCR.py          # PAN-specific pipeline (YOLO+OCR)
│   ├── endpoints.py        # Flask route definitions
│   ├── utils/              # Path, helpers, I/O, etc.
│   ├── templates/          # HTML forms for manual testing
│   └── static/             # CSS, static files
├── tests/                  # Unittest cases for extraction methods
├── requirements.txt        # Python pip dependency list
├── Dockerfile              # Container build specification
├── README.md               # Project overview
```

**Key Files:**
- `app/controllers/pan_o_c_r_controllers.py` — Main entry for YOLO-based PAN extraction
- `app/models/panOCR.py` — PAN pipeline: object detection + OCR + postprocessing
- `app/models/preProcessor/imagePreProcessor.py` — All image preprocessing steps
- `app/models/textExtraction/textExtractor.py` — Tesseract OCR integration
- `app/endpoints.py` — HTTP API endpoints

---

## 4. Dependency Mapping

### Python Requirements

- **Python 3.10** (see README)
- `ultralytics` (YOLO) — version unspecified, but must be compatible with YOLOv8
- `torch` (PyTorch) — required for YOLO
- `opencv-python` (cv2) — preprocessing, image I/O
- `Pillow` (PIL) — likely for image handling
- `Flask` — API server
- `pytesseract` — OCR
- `numpy`
- `scipy` (potentially for image ops)
- `spacy` — for address parsing post-OCR
- `gunicorn` — for production WSGI

**System (Dockerfile):**
- `tesseract-ocr-all` — all language packs for Tesseract
- `build-essential`, `g++`, `gcc`, `cmake`, `libopenblas-dev`, OpenCV libraries, etc.

**Note:** Exact library versions are **not pinned** in code/requirements.txt (potential reproducibility issue).

---

## 5. System Architecture Diagram

```mermaid
flowchart TD
    A[HTTP Request (Image)] --> B[Flask Endpoint]
    B --> C[Controller (e.g., PANOCRController)]
    C --> D[YOLO Model (ultralytics)]
    D --> E[Bounding Boxes]
    E --> F[Crop / Preprocess (ImagePreprocessor)]
    F --> G[Tesseract OCR (TextExtractor)]
    G --> H[Data Postprocessing (e.g., FilterPANData)]
    H --> I[API Response (JSON)]
```

---

## 6. Training and Inference Pipelines

### 6.1 Training Pipeline

**NOTE:** No training scripts or configuration files are present in the repo; model is assumed to be trained externally.

- **Typical Flow (not in repo):**
    1. Dataset loading (YOLO format, .txt labels)
    2. Data augmentation via Ultralytics CLI or custom scripts
    3. Model training (ultralytics CLI/API)
    4. Metric tracking (e.g., mAP, recall)
    5. Model weights exported to `Path.MODEL`

### 6.2 Inference Pipeline

- **Input:** Image (URL, base64, or numpy)
- **Image Preprocessing:** Size check → Resize → Grayscale → Otsu threshold → Morphology
- **YOLO Prediction:** `self.model(source=processed_image, save_crop=True, hide_labels=True,...)`
- **Crop Detected Regions:** Detected bounding boxes are used to crop image regions
- **OCR:** Cropped regions passed to Tesseract via `TextExtractor`
- **Postprocessing:** Extracted text is parsed (regex, NLP) to obtain structured data
- **Output:** API returns JSON with extracted fields, error codes if failed

---

## 7. Code Quality Analysis

### 7.1 Naming Conventions

- **Class names:** CamelCase (e.g., `PANOCRModel`, `AadhaarBackOCRModel`)
- **Function names:** snake_case (e.g., `extract_image`, `clear_field`)
- **Some inconsistency:** e.g., `aadhaar_front_o_c_r_controller` vs. `AadhaarBackOCRController`

### 7.2 Documentation Gaps

- **Docstrings:** Largely absent in classes and methods.
- **README:** Minimal, lacks user/dev instructions for model retraining or advanced deployment.
- **Inline Comments:** Present in some functions, but many blocks lack explanation.

### 7.3 Code Quality Issues

- **Hardcoded paths:** e.g., `"runs"` for YOLO output
- **Error handling:** Exceptions are caught and returned as dicts, but dev messages could be more informative
- **Dead/commented code:** Many sections are commented out or left as placeholders
- **No configuration abstraction:** Parameters (thresholds, paths) are in code rather than a config file

---

## 8. Technical Recommendations

### 8.1 Code Refactoring Suggestions

- **Reduce Duplication:** Utility functions for repeated preprocessing, error formatting
- **Improve Modularity:** Separate detection, OCR, and postprocessing into distinct, testable modules
- **Add Docstrings:** For all public classes/methods
- **Parameterize Configs:** Use config files (YAML/JSON) for model paths, thresholds, etc.
- **Centralize Error Codes/Messages:** For maintainability

### 8.2 Performance Optimizations

- **Batch Processing:** Current inference is single-image; consider batch API for efficiency
- **GPU Utilization:** Explicit device selection is present; monitor memory usage for large jobs
- **Data Loading:** For training, use PyTorch DataLoader (if/when training scripts are added)
- **Inference Speed:** Profile bottlenecks in preprocessing and OCR steps

### 8.3 Architectural Improvements

- **Separation of Concerns:** Controllers should not own heavy model logic; move to dedicated service layer
- **Logging:** Integrate logging (standard Python `logging` or Sentry)
- **Testing:** Unit tests exist for extraction, but expand to cover controllers and API endpoints
- **Configuration Management:** Use environment variables + config files

### 8.4 Infrastructure Enhancements

- **Model Versioning:** Store and reference model weights with version tags
- **Experiment Tracking:** Integrate MLflow or similar for reproducible results
- **Deployment:** Provide Docker Compose, add health checks
- **Monitoring:** Add Prometheus/Grafana, Sentry for error monitoring

---

## 9. Production Readiness Checklist

- [ ] **Input Validation:** API should validate image format, size, and content
- [ ] **Graceful Error Handling:** Return user-friendly messages, detailed logs for developers
- [ ] **Resource Management:** Clean up temp files, manage GPU/CPU usage
- [ ] **Scalability:** Support multi-threaded or multi-process inference for concurrent requests
- [ ] **Security:** Sanitize inputs, protect endpoints, handle sensitive data securely
- [ ] **Test Coverage:** Extend unittests, introduce integration tests for API
- [ ] **Documentation:** Expand README, add API usage examples, reference retraining steps

---

## References

- [Ultralytics YOLO Docs](https://docs.ultralytics.com/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [Docker](https://docs.docker.com/)
- [PyTorch](https://pytorch.org/)

---

# End of Documentation
