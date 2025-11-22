from characters.models.core import CharacterModel
from core.models import Model, ModelManager, ModelQuerySet
from django.db import models
from django.urls import reverse
from locations.models.core import LocationModel
from polymorphic.managers import PolymorphicManager


class ItemQuerySet(ModelQuerySet):
    """Custom queryset for ItemModel with chainable query patterns."""

    # Inherits all methods from ModelQuerySet
    pass


# Create ItemModelManager from the QuerySet to expose all QuerySet methods on the manager
ItemModelManager = PolymorphicManager.from_queryset(ItemQuerySet)


class ItemModel(Model):
    type = "item"

    owned_by = models.ManyToManyField(CharacterModel, blank=True)
    located_at = models.ManyToManyField(LocationModel, blank=True)

    objects = ItemModelManager()

    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Items"

    def get_absolute_url(self):
        return reverse("items:item", args=[str(self.id)])

    def get_update_url(self):
        return reverse("items:update:item", args=[str(self.id)])

    @classmethod
    def get_creation_url(cls):
        return reverse("items:create:item")

    def get_heading(self):
        return "wod_heading"

    def owned_by_list(self):
        return list(self.owned_by.all())
