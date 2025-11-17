from core.models import Model
from django.db import models


class ApocalypticFormTrait(Model):
    """Represents a specific ability/trait available in apocalyptic form."""

    type = "apocalyptic_form_trait"

    # Description of what this trait does
    description = models.TextField(default="")

    # Associated house (optional - some traits might be universal)
    house = models.ForeignKey(
        "House",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="apocalyptic_traits",
    )

    class Meta:
        verbose_name = "Apocalyptic Form Trait"
        verbose_name_plural = "Apocalyptic Form Traits"
        ordering = ["name"]

    def __str__(self):
        return self.name
