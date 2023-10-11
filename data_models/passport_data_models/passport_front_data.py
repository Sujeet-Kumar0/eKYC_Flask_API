class PassportFrontData:
    def __init__(self):
        self.idType = ""
        self.confidence = 0.0
        self.details = self.Details()

    def to_dict(self):
        return {
            "idType": self.idType,
            "confidence": self.confidence,
            "details": self.details.to_dict(),
        }

    class Details:
        def __init__(self):
            self.idNumber = self.Attribute()
            self.name = self.Attribute()
            self.nationality = self.Attribute()
            self.photo = self.Attribute()

        def to_dict(self):
            return {
                "idNumber": self.idNumber.to_dict(),
                "name": self.name.to_dict(),
                "nationality": self.nationality.to_dict(),
                "photo": self.photo.to_dict(),
            }

        class Attribute:
            def __init__(self):
                self.confidence = 0.0
                self.text = ""

            def to_dict(self):
                return {"confidence": self.confidence, "text": self.text}
