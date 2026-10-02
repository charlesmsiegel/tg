from django.apps import AppConfig

import accounts.checks  # noqa: F401  (registers the system checks)


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"

    def ready(self):
        # Receivers import models, so Django's app registry must be ready first.
        import accounts.signals  # noqa: F401
