from enum import Enum, auto


class IdType(Enum):
    PASSPORT = auto()
    PASSPORTFRONT = auto()
    PASSPORTBACK = auto()
    AADHAARFRONT = auto()
    AADHAARBACK = auto()
    PAN = auto()
