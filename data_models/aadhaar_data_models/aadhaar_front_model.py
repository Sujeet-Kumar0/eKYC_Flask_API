from .aadhaar_data_model import AadhaarDataModel


class AadhaarFrontModel:
    def __init__(self):
        self.idType = ""
        self.confidence = 0.0
        self.validated = False
        self.details = self.AaFrontDetailsModel()

    def to_dict(self):
        return {
            "idType": self.idType,
            "confidience": self.confidence,
            "details": self.details.to_dict(),
            "validate": self.validated,
        }

    class AaFrontDetailsModel:
        def __init__(self):
            self.name = self.Attribute()
            self.gender = self.Attribute()
            self.DOB = self.Attribute()
            self.issueDate = self.Attribute()
            self.vid = self.Attribute()
            self.aadhaarNumber = AadhaarDataModel()
            self.photo = self.Attribute()

        def to_dict(self):
            photo_dict = self.photo.to_dict()
            photo_dict.pop("text")
            return {
                "name": self.name.to_dict(),
                "gender": self.gender.to_dict(),
                "aadhaarNumber": self.aadhaarNumber.to_dict(),
                "issueDate": self.issueDate.to_dict(),
                "DOB": self.DOB.to_dict(),
                "vid": self.vid.to_dict(),
                "photo": photo_dict,
            }

        class Attribute:
            def __init__(self):
                self.confidence = 0.0
                self.text = ""

            def to_dict(self):
                return {"confidence": self.confidence, "text": self.text}
