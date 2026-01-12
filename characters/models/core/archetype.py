from core.models import Model, URLMethodsMixin


class Archetype(URLMethodsMixin, Model):
    type = "archetype"
    gameline = "wod"
    url_namespace = "characters"
    url_name = "archetype"

    class Meta:
        verbose_name = "Archetype"
        verbose_name_plural = "Archetypes"
