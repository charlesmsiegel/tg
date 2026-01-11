from django.db import models

from items.models.core.item import ItemModel


class SorcererArtifact(ItemModel):
    type = "sorcerer_artifact"
    gameline = "mta"

    rank = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Artifact (Sorcerer)"
        verbose_name_plural = "Artifacts (Sorcerer)"
