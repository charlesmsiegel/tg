from core.models import Model
from django.db import models
from django.urls import reverse


class Chimera(Model):
    """
    Chimera are sentient or semi-sentient chimerical creations.
    They can be manifested from dreams or created through Treasures.
    """

    type = "chimera"

    # Chimera type and nature
    chimera_type = models.CharField(
        max_length=30,
        choices=[
            ("facsimile", "Facsimile"),
            ("simple_crafted", "Simple Crafted"),
            ("advanced_crafted", "Advanced Crafted"),
            ("complex_crafted", "Complex Crafted"),
            ("master_crafted", "Master Crafted"),
        ],
        blank=True,
        default="",
        help_text="Type determines sentience and abilities",
    )

    chimera_points = models.IntegerField(
        default=5, help_text="Power level: 5-10 (simple), 15-25 (moderate), 30-50 (master)"
    )

    # Sentience and behavior
    sentience_level = models.CharField(
        max_length=30,
        choices=[
            ("non_sentient", "Non-Sentient"),
            ("semi_sentient", "Semi-Sentient"),
            ("sentient", "Sentient"),
            ("fully_sentient", "Fully Sentient"),
        ],
        blank=True,
        default="non_sentient",
    )

    behavior = models.TextField(
        blank=True, default="", help_text="Behavioral patterns and tendencies"
    )

    # Physical properties
    appearance = models.TextField(
        blank=True, default="", help_text="Physical appearance and description"
    )
    durability = models.IntegerField(
        default=1,
        help_text="How durable/resilient is this Chimera (1-5)",
    )

    # Special abilities
    special_abilities = models.JSONField(
        default=list, help_text="List of special abilities"
    )
    can_interact_with_physical = models.BooleanField(
        default=False, help_text="Can physically interact with Autumn World"
    )

    # Relationship properties
    loyalty = models.IntegerField(
        default=0, help_text="Loyalty to creator (0-5)"
    )
    creator = models.CharField(
        max_length=100, blank=True, default="", help_text="Who created/manifested this"
    )

    # Origin and permanence
    origin = models.CharField(
        max_length=30,
        choices=[
            ("manifested_dream", "Manifested Dream"),
            ("treasure_bound", "Treasure Bound"),
            ("created_art", "Created via Art"),
            ("other", "Other"),
        ],
        blank=True,
        default="",
    )

    is_permanent = models.BooleanField(
        default=False, help_text="Is this a permanent Chimera"
    )

    # Dream connection
    dream_source = models.TextField(
        blank=True, default="", help_text="Which dream it originated from"
    )

    class Meta:
        verbose_name = "Chimera"
        verbose_name_plural = "Chimera"

    def get_update_url(self):
        return reverse("characters:changeling:update:chimera", args=[str(self.id)])

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:changeling:create:chimera")

    def get_heading(self):
        return "ctd_heading"

    def __str__(self):
        if self.name:
            return f"{self.name} ({self.get_chimera_type_display()})"
        return super().__str__()
