class PassportBackData:
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
            self.cardNumber = self.Attribute()
            self.gender = self.Attribute()
            self.DOB = self.Attribute()
            self.expiryDate = self.Attribute()
            self.signature = self.Attribute()

        def to_dict(self):
            return {
                "cardNumber": self.cardNumber.to_dict(),
                "gender": self.gender.to_dict(),
                "DOB": self.DOB.to_dict(),
                "expiryDate": self.expiryDate.to_dict(),
                "signature": self.signature.to_dict(),
            }

        class Attribute:
            def __init__(self):
                self.confidence = 0.0
                self.text = ""

            def to_dict(self):
                return {"confidence": self.confidence, "text": self.text}
