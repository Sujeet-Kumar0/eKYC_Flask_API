import random

from deepface import DeepFace

from app.utils import URL_Type
from app.utils import UrlType


class FaceMatchingModel:
    def __init__(self):
        self.models = [
            "VGG-Face",
            "Facenet",
            "Facenet512",
            "OpenFace",
            "DeepID",
            "ArcFace",
            "SFace",
        ]
        # models = ["VGG-Face", "Facenet", "Facenet512", "OpenFace", "DeepFace", "DeepID", "ArcFace", "Dlib", "SFace"]
        self.metrics = ["cosine", "euclidean", "euclidean_l2"]
        self.backends = ["opencv", "mtcnn"]
        # backends = ['opencv', 'ssd', 'dlib', 'mtcnn', 'retinaface', 'mediapipe']
        self.is_setup_done = False

    def setup(self):
        for model in self.models:
            try:
                print("Building Model: " + model)
                DeepFace.build_model(model)
            except ValueError:
                print("Error occured while building Model: " + model)
        self.is_setup_done = True

    def verify(
            self, image1, image2, models=None, metrics=None, backends=None, enforce=True
    ):
        input_type1 = URL_Type.check(image1)
        input_type2 = URL_Type.check(image2)

        if input_type1 is UrlType.NONE or input_type2 is UrlType.NONE:
            return {
                "status": -1,
                "error": "Invalid input: Inputs should be either Base64 or Url or Numpy Array",
            }
        elif input_type1 != input_type2:
            return {
                "status": -1,
                "error": "Both inputs should be either Base64 or Url or Numpy Array",
            }

        if not self.is_setup_done:
            self.setup()

        selected_models = models or random.choice(self.models)
        selected_metrics = metrics or random.choice(self.metrics)
        selected_backends = backends or random.choice(self.backends)

        try:
            result = DeepFace.verify(
                image1,
                image2,
                model_name=selected_models,
                distance_metric=selected_metrics,
                detector_backend=selected_backends,
                enforce_detection=enforce,
            )
        except Exception as e:
            return {
                "status": -2,
                "error": str(e),
                "model": selected_models,
                "similarity_metric": selected_metrics,
                "detector_backend": selected_backends,
                "verified": False,
            }

        return result
