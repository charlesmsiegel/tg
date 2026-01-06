"""
Django App Configuration for Chained Select - Backward Compatibility

This app is deprecated. The widgets app now handles URL registration.
"""

from django.apps import AppConfig


class ChainedSelectConfig(AppConfig):
    name = "chained_select"
    default_auto_field = "django.db.models.BigAutoField"

    def ready(self):
        """No longer registers URLs - widgets app handles this."""
        pass
