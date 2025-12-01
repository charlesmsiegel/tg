"""
Character managers for handling complex character operations.

These managers implement composition over inheritance by extracting
complex business logic from model mixins into dedicated manager classes.
"""

from .background_manager import BackgroundManager
from .merit_flaw_manager import MeritFlawManager

__all__ = ["MeritFlawManager", "BackgroundManager"]
