from django.db import models
from django.urls import reverse

from items.models.core import ItemModel


class VampireArtifact(ItemModel):
    """
    Represents a Vampire-specific magical or significant item.
    Could include enchanted weapons, occult items, ancient relics, etc.
    """

    type = "vampire_artifact"
    gameline = "vtm"

    # Power level
    power_level = models.IntegerField(
        default=1,
        help_text="Power level of artifact (1-5)",
    )

    # Background cost (if acquired through Backgrounds)
    background_cost = models.IntegerField(
        default=0,
        help_text="Background points required to own",
    )

    # Properties
    is_cursed = models.BooleanField(default=False, help_text="Artifact is cursed")

    is_unique = models.BooleanField(
        default=False,
        help_text="One-of-a-kind artifact",
    )

    requires_blood = models.BooleanField(
        default=False,
        help_text="Requires blood to activate/use",
    )

    # Effects
    powers = models.TextField(
        blank=True,
        help_text="Description of artifact's powers and effects",
    )

    # History/Lore
    history = models.TextField(
        blank=True,
        help_text="History and provenance of artifact",
    )

    class Meta:
        verbose_name = "Vampire Artifact"
        verbose_name_plural = "Vampire Artifacts"

    def get_absolute_url(self):
        return reverse("items:vampire:artifact", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("items:vampire:update:artifact", args=[str(self.id)])

    @classmethod
    def get_creation_url(cls):
        return reverse("items:vampire:create:artifact")
