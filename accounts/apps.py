from django.apps import AppConfig

# Registers the system checks. It runs while apps are still loading, which is
# safe only because accounts.checks imports no models.
import accounts.checks  # noqa: F401


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"

    def ready(self):
        # Receivers import models, so Django's app registry must be ready first.
        import accounts.signals  # noqa: F401
