from .OSType import OSType


class Path:
    if OSType.get_os_type() == OSType.WIN:
        PATHS = ["runs/detect/predict/crops/dob/",
                 "runs/detect/predict/crops/name/",
                 "runs/detect/predict/crops/father name/",
                 "runs/detect/predict/crops/pan number/"]

        LABEL_PATH = "runs/detect/predict/labels/image0.txt"

        MODEL = "best.pt"

        STATES_JSON = "./states.json"

    elif OSType.get_os_type() == OSType.LINUX:
        PATHS = ["/app/runs/detect/predict/crops/dob/",
                 "/app/runs/detect/predict/crops/name/",
                 "/app/runs/detect/predict/crops/father name/",
                 "/app/runs/detect/predict/crops/pan number/"]

        LABEL_PATH = "/app/runs/detect/predict/labels/image0.txt"

        MODEL = "/app/best.pt"

        STATES_JSON = "/app/states.json"
