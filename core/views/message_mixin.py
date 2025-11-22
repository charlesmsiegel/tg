"""
DEPRECATED: This module is maintained for backward compatibility only.

Please import from core.mixins instead:
    from core.mixins import (
        SuccessMessageMixin,
        ErrorMessageMixin,
        MessageMixin,
        DeleteMessageMixin,
    )
"""

# Import for backward compatibility
from core.mixins import (
    SuccessMessageMixin,
    ErrorMessageMixin,
    MessageMixin,
    DeleteMessageMixin,
)

__all__ = [
    'SuccessMessageMixin',
    'ErrorMessageMixin',
    'MessageMixin',
    'DeleteMessageMixin',
]
