

from django.core.exceptions import ValidationError


class InvalidPasswordError(ValidationError):
    """
    Raised when password does not meet the validity requirements.
    """
    pass
