from characters.models.core import CharacterModel
from core.models import Model, ModelManager
from django.db import models
from django.urls import reverse
from locations.models.core import LocationModel


class ItemModelManager(ModelManager):
    """Custom manager for ItemModel with specialized query patterns."""

    def pending_approval_for_user(self, user):
        """Items awaiting approval in user's chronicles (optimized)"""
        # Items use status in ['Un', 'Sub'], different from characters
        return (
            self.filter(status__in=["Un", "Sub"], chronicle__in=user.chronicle_set.all())
            .select_related("chronicle", "owner")
            .order_by("name")
        )


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
