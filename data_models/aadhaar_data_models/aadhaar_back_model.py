from .aadhaar_data_model import AadhaarDataModel
from .address_data_model import AddressDataModel


class AadhaarBackModel:
    def __init__(self):
        self.idType = ""
        self.confidence = 0.0
        self.validated = False
        self.details = self.Details()

    def to_dict(self):
        return {
            "idType": self.idType,
            "confidence": self.confidence,
            "details": self.details.to_dict(),
            "validate": self.validated,
        }

    class Details:
        def __init__(self):
            self.address = AddressDataModel()
            self.aadhaarDetails = AadhaarDataModel()

        def to_dict(self):
            return {
                "address": self.address.to_dict(),
                "aadhaarNumber": self.aadhaarDetails.to_dict(),
            }
