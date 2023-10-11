from dataclasses import dataclass
from typing import Any


@dataclass
class ResponseData:
    status: int
    message: str = "Please Try Again"
    data: Any = None
    devMsg: str = ""
    code: str = ""
