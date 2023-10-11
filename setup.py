from deepface import DeepFace

models = ["VGG-Face", "Facenet", "Facenet512", "OpenFace", "DeepID", "ArcFace", "Dlib"]
for model in models:
    try:
        print("Building Model: " + model)
        DeepFace.build_model(model)
    except ValueError:
        print("Error occured while building Model: " + model)
    except Exception as e:
        print("Error occured while building Model: " + model + "\nError: " + str(e))
