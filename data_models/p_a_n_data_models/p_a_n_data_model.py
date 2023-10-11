class PANDataModel:
    def __init__(self):
        self.idType = ""
        self.confidence = ""
        self.details = self.Details()

    def to_dict(self):
        return {
            "idType": self.idType,
            "confidence": self.confidence,
            "details": self.details.to_dict(),
        }

    class Details:
        def __init__(self):
            self.pan = self.Attribute()
            self.fatherName = self.Attribute()
            self.name = self.Attribute()
            self.dob = self.Attribute()

        def to_dict(self):
            return {
                "pan": self.pan.to_dict(),
                "fatherName": self.fatherName.to_dict(),
                "name": self.name.to_dict(),
                "DOB": self.dob.to_dict(),
            }

        class Attribute:
            def __init__(self):
                self.confidence = 0.0
                self.text = ""

            def to_dict(self):
                return {"confidence": self.confidence, "text": self.text}
