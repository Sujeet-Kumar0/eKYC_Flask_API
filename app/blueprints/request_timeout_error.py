class RequestTimeoutError(Exception):
    status_code = 408
    payload = None

    def __init__(self, message="Please Try Again", payload=None):
        super().__init__()
        self.message = message
        self.payload = payload
