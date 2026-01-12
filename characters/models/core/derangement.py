from core.models import Model, URLMethodsMixin


class Derangement(URLMethodsMixin, Model):
    type = "derangement"
    gameline = "wod"
    url_namespace = "characters"
    url_name = "derangement"

    class Meta:
        verbose_name = "Derangement"
        verbose_name_plural = "Derangements"
