from django.db import models

from core.models import Model, ModelManager, ModelQuerySet
from core.registry_urls import RegistryURLMixin


class ItemQuerySet(ModelQuerySet):
    """Custom queryset for ItemModel with chainable query patterns."""

    # Inherits all methods from ModelQuerySet
    pass


# Create ItemModelManager from ModelManager to inherit polymorphic_ctype optimization
ItemModelManager = ModelManager.from_queryset(ItemQuerySet)


class ItemModel(RegistryURLMixin, Model):
    type = "item"

    owned_by = models.ManyToManyField("characters.CharacterModel", blank=True)
    located_at = models.ManyToManyField("locations.LocationModel", blank=True)

    objects = ItemModelManager()

    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Items"

    def owned_by_list(self):
        return list(self.owned_by.all())
