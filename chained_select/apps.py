"""
Django App Configuration for Chained Select

Auto-registers the AJAX endpoint URL so users don't need to modify urls.py
"""

from django.apps import AppConfig


class ChainedSelectConfig(AppConfig):
    name = "chained_select"
    default_auto_field = "django.db.models.BigAutoField"

    def ready(self):
        """Auto-register the AJAX URL when Django starts."""
        self._register_url()

    def _register_url(self):
        """Inject our AJAX endpoint into the root URLconf."""
        import importlib

        from django.conf import settings
        from django.urls import path

        try:
            # Import the root URL configuration
            urlconf_module = importlib.import_module(settings.ROOT_URLCONF)

            # Import our view
            from .views import auto_chained_ajax_view

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
            import warnings

            warnings.warn(
                f"chained_select: Could not auto-register URL: {e}. "
                "You may need to add the URL manually.",
                RuntimeWarning,
            )
