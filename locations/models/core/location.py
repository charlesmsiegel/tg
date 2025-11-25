from characters.models.core import CharacterModel
from core.models import Model, ModelManager, ModelQuerySet
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from game.models import Scene
from polymorphic.managers import PolymorphicManager


class LocationQuerySet(ModelQuerySet):
    """Custom queryset for LocationModel with chainable query patterns."""

    def top_level(self):
        """Top-level locations (no parent)"""
        return self.filter(parent=None)


# Create LocationModelManager from ModelManager to inherit polymorphic_ctype optimization
LocationModelManager = ModelManager.from_queryset(LocationQuerySet)


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

    def clean(self):
        """Validate location data before saving."""
        super().clean()
        errors = {}

        # Validate gauntlet is in valid range (0-10)
        if self.gauntlet < 0 or self.gauntlet > 10:
            errors["gauntlet"] = "Gauntlet must be between 0 and 10"

        # Validate shroud is in valid range (0-10)
        if self.shroud < 0 or self.shroud > 10:
            errors["shroud"] = "Shroud must be between 0 and 10"

        # Validate dimension_barrier is in valid range (0-10)
        if self.dimension_barrier < 0 or self.dimension_barrier > 10:
            errors["dimension_barrier"] = "Dimension barrier must be between 0 and 10"

        # Validate creation_status is non-negative
        if self.creation_status < 0:
            errors["creation_status"] = "Creation status cannot be negative"

        if errors:
            raise ValidationError(errors)

    # Note: save() method inherited from Model base class already calls full_clean()
