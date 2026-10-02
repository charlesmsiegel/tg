from django.apps import AppConfig


class GameConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "game"

    def ready(self):
        # Receivers import models, so Django's app registry must be ready first.
        import game.signals  # noqa: F401
