from django.db import models
from django.urls import reverse

from items.models.core import ItemModel


class HunterRelic(ItemModel):
    """
    Mystical items with supernatural properties.
    These are rare in Hunter: the Reckoning, but may include blessed objects,
    holy relics, or items touched by the Messengers.
    """

    type = "hunter_relic"
    gameline = "htr"

    # Power level
    power_level = models.IntegerField(
        default=1,
        help_text="Power level of relic (1-5)",
    )

    # Background cost (if acquired through Backgrounds)
    background_cost = models.IntegerField(
        default=0,
        help_text="Background points required to own",
    )

    # Properties
    is_blessed = models.BooleanField(
        default=False,
        help_text="Item is blessed by divine/higher power",
    )

    is_cursed = models.BooleanField(
        default=False,
        help_text="Item carries a curse",
    )

    requires_faith = models.BooleanField(
        default=False,
        help_text="Requires faith or conviction to activate",
    )

    is_unique = models.BooleanField(
        default=False,
        help_text="One-of-a-kind relic",
    )

    # Effects
    powers = models.TextField(
        blank=True,
        help_text="Description of relic's powers and effects",
    )

    activation_cost = models.CharField(
        max_length=200,
        blank=True,
        help_text="Cost to activate (e.g., '1 Willpower', '1 Conviction')",
    )

    # Connection to higher powers
    origin = models.TextField(
        blank=True,
        help_text="Origin and history of the relic",
    )

    # Side effects or limitations
    limitations = models.TextField(
        blank=True,
        help_text="Limitations, drawbacks, or side effects",
    )

    class Meta:
        verbose_name = "Hunter Relic"
        verbose_name_plural = "Hunter Relics"

    def get_update_url(self):
        return reverse("items:hunter:update:relic", args=[str(self.id)])

    @classmethod
    def get_creation_url(cls):
        return reverse("items:hunter:create:relic")

    def get_heading(self):
        return "htr_heading"
