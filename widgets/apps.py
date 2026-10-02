"""
Django App Configuration for Widgets App

Auto-registers the AJAX endpoint URL so users don't need to modify urls.py
"""

import importlib
import warnings

from django.apps import AppConfig
from django.conf import settings
from django.urls import path

from .views import auto_chained_ajax_view


class WidgetsConfig(AppConfig):
    name = "widgets"
    default_auto_field = "django.db.models.BigAutoField"
    verbose_name = "Form Widgets"

    def ready(self):
        """Auto-register the AJAX URL when Django starts."""
        self._register_url()

    def _register_url(self):
        """Inject our AJAX endpoint into the root URLconf."""
        try:
            # Import the root URL configuration
            urlconf_module = importlib.import_module(settings.ROOT_URLCONF)

            # Check if we've already added it (happens during testing/reloads)
            existing_names = [
                getattr(p, "name", None) for p in getattr(urlconf_module, "urlpatterns", [])
            ]

            if "__chained_select_ajax__" not in existing_names:
                # Add our URL pattern
                urlconf_module.urlpatterns.insert(
                    0,
                    path(
                        "__chained_select__/",
                        auto_chained_ajax_view,
                        name="__chained_select_ajax__",
                    ),
                )
        except Exception as e:
            # Don't crash the app if URL registration fails
            # (might happen in some test scenarios)
            warnings.warn(
                f"widgets: Could not auto-register URL: {e}. "
                "You may need to add the URL manually.",
                RuntimeWarning,
                stacklevel=2,
            )
