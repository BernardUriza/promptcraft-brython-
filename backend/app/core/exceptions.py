# PromptCraft - Custom Exceptions

from typing import Optional, Any


class PromptCraftException(Exception):
    """Base exception for PromptCraft application."""

    def __init__(
        self,
        message: str = "An error occurred",
        status_code: int = 500,
        details: Optional[dict[str, Any]] = None
    ):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class AuthenticationError(PromptCraftException):
    """Raised when authentication fails."""

    def __init__(
        self,
        message: str = "Authentication failed",
        details: Optional[dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            status_code=401,
            details=details
        )


class AuthorizationError(PromptCraftException):
    """Raised when user lacks permission."""

    def __init__(
        self,
        message: str = "Permission denied",
        details: Optional[dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            status_code=403,
            details=details
        )


class NotFoundError(PromptCraftException):
    """Raised when resource is not found."""

    def __init__(
        self,
        resource: str = "Resource",
        resource_id: Optional[str | int] = None,
        details: Optional[dict[str, Any]] = None
    ):
        message = f"{resource} not found"
        if resource_id:
            message = f"{resource} with id '{resource_id}' not found"
        super().__init__(
            message=message,
            status_code=404,
            details=details
        )


class ValidationError(PromptCraftException):
    """Raised when validation fails."""

    def __init__(
        self,
        message: str = "Validation failed",
        errors: Optional[list[dict[str, Any]]] = None,
        details: Optional[dict[str, Any]] = None
    ):
        details = details or {}
        if errors:
            details["errors"] = errors
        super().__init__(
            message=message,
            status_code=422,
            details=details
        )


class RateLimitError(PromptCraftException):
    """Raised when rate limit is exceeded."""

    def __init__(
        self,
        message: str = "Rate limit exceeded",
        retry_after: Optional[int] = None,
        details: Optional[dict[str, Any]] = None
    ):
        details = details or {}
        if retry_after:
            details["retry_after"] = retry_after
        super().__init__(
            message=message,
            status_code=429,
            details=details
        )


class DuplicateError(PromptCraftException):
    """Raised when trying to create duplicate resource."""

    def __init__(
        self,
        resource: str = "Resource",
        field: str = "field",
        details: Optional[dict[str, Any]] = None
    ):
        message = f"{resource} with this {field} already exists"
        super().__init__(
            message=message,
            status_code=409,
            details=details
        )


class XPTransactionError(PromptCraftException):
    """Raised when XP transaction fails."""

    def __init__(
        self,
        message: str = "XP transaction failed",
        details: Optional[dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            status_code=400,
            details=details
        )


class StreakError(PromptCraftException):
    """Raised when streak operation fails."""

    def __init__(
        self,
        message: str = "Streak operation failed",
        details: Optional[dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            status_code=400,
            details=details
        )
