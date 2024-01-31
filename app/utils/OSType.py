import sys
from enum import Enum, auto


class OSType(Enum):
    LINUX = auto()
    WIN = auto()
    MAC = auto()
    UNKNOWN = auto()

    @classmethod
    def get_os_type(cls):
        if sys.platform.startswith("win"):
            return cls.WIN
        elif sys.platform.startswith("darwin"):
            return cls.MAC
        elif sys.platform.startswith("linux"):
            return cls.LINUX
        else:
            return cls.UNKNOWN
