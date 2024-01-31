from enum import Enum, auto

import numpy as np


class UrlType(Enum):
    URL = auto()
    BASE64 = auto()
    NUMPY = auto()
    NONE = auto()


def check(url):
    if isinstance(url, str) and (url.startswith('http') or url.startswith('https')):
        return UrlType.URL
    elif isinstance(url, str) and url.startswith('data:image'):
        return UrlType.BASE64
    elif isinstance(url, np.ndarray):
        return UrlType.NUMPY
    return UrlType.NONE
