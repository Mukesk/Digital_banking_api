class BaseCustomException(Exception):
    def __init__(self, message: str, status_code: int):
        self.message = message
        self.status_code = status_code
        super().__init__(message)

class RateLimitExceededException(BaseCustomException):
    def __init__(self):
        super().__init__("Rate limit exceeded", 429)

class InsufficientFundsException(BaseCustomException):
    def __init__(self):
        super().__init__("Insufficient funds for this transaction", 400)
