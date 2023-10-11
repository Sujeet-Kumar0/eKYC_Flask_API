class AddressDataModel:
    def __init__(self):
        self.pincode = ""
        self.district = ""
        self.state = ""
        self.address = ""
        self.confidence = 0.0

    def to_dict(self):
        return {
            "address": self.address,
            "district": self.district,
            "state": self.state,
            "pincode": self.pincode,
            "confidence":self.confidence
        }
