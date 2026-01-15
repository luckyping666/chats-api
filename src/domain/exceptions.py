class DomainError(Exception):
    """Base domain exception."""
    pass


class ValidationError(DomainError):
    """Raised when domain validation fails."""
    pass


class ChatNotFound(DomainError):
    """Raised when chat does not exist."""
    pass
