"""The result shape shared by chargen and spending services."""

from dataclasses import dataclass
from typing import Any


@dataclass
class ServiceResult:
    """Outcome of a state-changing operation.

    Mirrors ``XPSpendResult``/``FreebieSpendResult``: views flash ``message``
    on success and add ``error`` to the form otherwise.
    """

    success: bool
    message: str = ""
    error: str | None = None
    object: Any = None

    @classmethod
    def ok(cls, message="", obj=None):
        return cls(success=True, message=message, object=obj)

    @classmethod
    def fail(cls, error):
        return cls(success=False, error=error)
