"""
Character managers for handling complex character operations.

These managers implement composition over inheritance by extracting
complex business logic from model mixins into dedicated manager classes.
"""

from .merit_flaw_manager import MeritFlawManager
from .background_manager import BackgroundManager

__all__ = ["MeritFlawManager", "BackgroundManager"]
