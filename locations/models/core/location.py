from characters.models.core import CharacterModel
from core.models import Model, ModelManager, ModelQuerySet
from django.db import models
from django.urls import reverse
from game.models import Scene
from polymorphic.managers import PolymorphicManager


class LocationQuerySet(ModelQuerySet):
    """Custom queryset for LocationModel with chainable query patterns."""

    def top_level(self):
        """Top-level locations (no parent)"""
        return self.filter(parent=None)


# Create LocationModelManager from the QuerySet to expose all QuerySet methods on the manager
LocationModelManager = PolymorphicManager.from_queryset(LocationQuerySet)


class LocationModel(Model):
    type = "location"

    parent = models.ForeignKey(
        "LocationModel",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="children",
    )
    owned_by = models.ForeignKey(
        CharacterModel, blank=True, null=True, on_delete=models.SET_NULL
    )

    gauntlet = models.IntegerField(default=7)
    shroud = models.IntegerField(default=7)
    dimension_barrier = models.IntegerField(default=6)
    creation_status = models.IntegerField(default=1)

    objects = LocationModelManager()

    class Meta:
        verbose_name = "Location"
        verbose_name_plural = "Location"

    def get_absolute_url(self):
        return reverse("locations:location", args=[str(self.id)])

    def get_update_url(self):
        return reverse("locations:update:location", args=[str(self.id)])

    @classmethod
    def get_creation_url(cls):
        return reverse("locations:create:location")

    def get_heading(self):
        return "wod_heading"

    def get_scenes(self):
        return Scene.objects.filter(location=self)

    def owned_by_list(self):
        if self.owned_by:
            return [self.owned_by]
        else:
            return []
