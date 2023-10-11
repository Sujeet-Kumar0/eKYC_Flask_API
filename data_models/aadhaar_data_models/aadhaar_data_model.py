class AadhaarDataModel:
    def __init__(self):
        self.confidence = 0.0
        self.text = ""
        self.isVerified = False

    def to_dict(self):
        return {
            "confidence": self.confidence,
            "text": self.text,
            "isVerified": self.isVerified,
        }
