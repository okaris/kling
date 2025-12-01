"""Custom exceptions for Kling SDK."""


class KlingError(Exception):
    """Base exception for all Kling SDK errors."""

    pass


class KlingAPIError(KlingError):
    """Raised when the Kling API returns an error."""

    def __init__(self, message: str, code: int = 0, request_id: str = ""):
        self.message = message
        self.code = code
        self.request_id = request_id
        super().__init__(f"[{code}] {message} (request_id: {request_id})")


class KlingValidationError(KlingError):
    """Raised when request validation fails."""

    pass


class KlingTimeoutError(KlingError):
    """Raised when a task times out."""

    pass
