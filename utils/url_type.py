from enum import Enum, auto


class UrlType(Enum):
    URL = auto()
    BASE64 = auto()
    FILE = auto()
    NONE = auto()

    def check(url):
        if isinstance(url, str) and (url.startswith("http") or url.startswith("https")):
            return UrlType.URL
        elif isinstance(url, str) and url.startswith("data:image"):
            return UrlType.BASE64
        elif hasattr(url, "filename"):
            return UrlType.FILE
        return UrlType.NONE
