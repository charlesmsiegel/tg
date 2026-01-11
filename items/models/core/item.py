from django.db import models
from django.urls import reverse

from characters.models.core import CharacterModel
from core.models import Model, ModelManager, ModelQuerySet
from locations.models.core import LocationModel


class ItemQuerySet(ModelQuerySet):
    """Custom queryset for ItemModel with chainable query patterns."""

    # Inherits all methods from ModelQuerySet
    pass


# Create ItemModelManager from ModelManager to inherit polymorphic_ctype optimization
ItemModelManager = ModelManager.from_queryset(ItemQuerySet)


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

    def owned_by_list(self):
        return list(self.owned_by.all())
