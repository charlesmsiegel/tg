from django.db import models
from django.urls import reverse
from locations.models.core import LocationModel


class WraithFreehold(LocationModel):
    """Independent wraith territory outside Hierarchy control."""

    type = "wraith_freehold"

    GOVERNMENT_TYPE_CHOICES = [
        ("council", "Council Rule"),
        ("democracy", "Democracy"),
        ("autocracy", "Autocracy"),
        ("anarchy", "Anarchy"),
        ("theocracy", "Theocracy"),
        ("oligarchy", "Oligarchy"),
        ("other", "Other"),
    ]

    HIERARCHY_RELATION_CHOICES = [
        ("independent", "Independent - No formal relations"),
        ("neutral", "Neutral - Tolerated by Hierarchy"),
        ("alliance", "Alliance - Formal agreement with Hierarchy"),
        ("hostile", "Hostile - At odds with Hierarchy"),
        ("secret", "Secret - Hidden from Hierarchy"),
        ("tributary", "Tributary - Pays tribute to Hierarchy"),
    ]

    # Population and governance
    population = models.IntegerField(default=0, help_text="Number of wraith inhabitants")
    government_type = models.CharField(
        max_length=20, choices=GOVERNMENT_TYPE_CHOICES, default="council"
    )
    leader = models.CharField(
        max_length=100, blank=True, help_text="Name of primary leader or ruling body"
    )

    # Relations
    hierarchy_relation = models.CharField(
        max_length=20, choices=HIERARCHY_RELATION_CHOICES, default="independent"
    )
    allied_factions = models.TextField(
        blank=True, help_text="Factions, guilds, or legions allied with this freehold"
    )

    # Resources and capabilities
    defense_rating = models.IntegerField(default=1, help_text="Defensive strength (1-10)")
    resource_level = models.IntegerField(
        default=1, help_text="Available resources and wealth (1-10)"
    )

    # Special features
    has_soulforges = models.BooleanField(
        default=False, help_text="Contains soulforging facilities"
    )
    has_library = models.BooleanField(
        default=False, help_text="Contains significant library or archives"
    )
    has_safe_passage = models.BooleanField(
        default=False, help_text="Offers safe passage through territory"
    )
    hidden = models.BooleanField(
        default=False, help_text="Location is hidden or secret"
    )

    # Philosophy/purpose
    founding_principle = models.TextField(
        blank=True,
        help_text="Core beliefs or reasons for independence (e.g., 'Freedom from tyranny', 'Guild solidarity')",
    )

    class Meta:
        verbose_name = "Wraith Freehold"
        verbose_name_plural = "Wraith Freeholds"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} (Freehold)"

    def get_absolute_url(self):
        return reverse("locations:wraith:freehold", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("locations:wraith:update:freehold", args=[str(self.id)])

    @classmethod
    def get_creation_url(cls):
        return reverse("locations:wraith:create:freehold")

    def get_heading(self):
        return "wto_heading"
