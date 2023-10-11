import logging
import random
from deepface import DeepFace

# models = ["VGG-Face", "Facenet", "Facenet512", "OpenFace", "DeepFace", "DeepID", "ArcFace", "Dlib", "SFace"]
# self.backends = ['opencv', 'ssd', 'dlib', 'mtcnn', 'retinaface', 'mediapipe']

logger = logging.getLogger(__name__)


class FaceMatchingModel:
    def __init__(self):
        self.models = ["Dlib"]
        self.metrics = ["cosine", "euclidean", "euclidean_l2"]
        self.backends = ["dlib"]
        self.is_setup_done = False
        if not self.is_setup_done:
            self.setup()

    def setup(self):
        for model in self.models:
            try:
                logger.debug("Building Model: " + model)
                DeepFace.build_model(model)
            except ValueError:
                logger.debug("Error occured while building Model: " + model)
            except Exception as e:
                logger.error(
                    "Error occured while building Model: "
                    + model
                    + "\nError: "
                    + str(e)
                )

        self.is_setup_done = True

    def call_deepface(self, image1, image2, deepFace):
        # if not self.is_setup_done:
        #     self.setup()

        model = deepFace.get("model", None)
        backend = deepFace.get("backend", None)
        enforce = deepFace.get("enforce_detection", True)
        metrics = deepFace.get("metric", None)
        align = deepFace.get("align", True)

        selected_models = model or random.choice(self.models)
        selected_metrics = metrics or random.choice(self.metrics)
        selected_backends = backend or random.choice(self.backends)

        try:
            result = DeepFace.verify(
                image1,
                image2,
                model_name=selected_models,
                distance_metric=selected_metrics,
                detector_backend=selected_backends,
                enforce_detection=enforce,
                align=align,
            )
            result["verified"] = bool(result["verified"])

        except Exception as e:
            result = {
                "status": -1,
                "error": str(e),
                "model": selected_models,
                "similarity_metric": selected_metrics,
                "detector_backend": selected_backends,
                "verified": False,
            }
            logger.error(str(result))

        logger.info(str(result))
        return result
