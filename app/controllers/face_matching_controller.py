from app.models.FaceMatchingModel import FaceMatchingModel


def face_matching_controller(image1, image2, models=None, metrics=None, backends=None, enforce=True):
    model = FaceMatchingModel()
    try:
        return model.verify(image1, image2, models, metrics, backends, enforce)
    except Exception as e:
        return {"status": -1, "message": "Please recapture ", "code": "MB", "devMsg": str(e)}, 400
