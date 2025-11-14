from django.db import models
from django.urls import reverse
from items.models.core import ItemModel


class Cantrip(ItemModel):
    """
    Cantrips are the spells/magical effects of Changelings.
    They combine an Art (method) with Realms (targets).
    """

    type = "cantrip"

    # Art system
    art = models.CharField(
        max_length=30,
        choices=[
            ("autumn", "Autumn"),
            ("chicanery", "Chicanery"),
            ("chronos", "Chronos"),
            ("contract", "Contract"),
            ("dragons_ire", "Dragon's Ire"),
            ("legerdemain", "Legerdemain"),
            ("metamorphosis", "Metamorphosis"),
            ("naming", "Naming"),
            ("oneiromancy", "Oneiromancy"),
            ("primal", "Primal"),
            ("pyretics", "Pyretics"),
            ("skycraft", "Skycraft"),
            ("soothsay", "Soothsay"),
            ("sovereign", "Sovereign"),
            ("spring", "Spring"),
            ("summer", "Summer"),
            ("wayfare", "Wayfare"),
            ("winter", "Winter"),
        ],
        blank=True,
        default="",
    )

    # Realm system (what the cantrip affects)
    primary_realm = models.CharField(
        max_length=30,
        choices=[
            ("actor", "Actor"),
            ("fae", "Fae"),
            ("nature", "Nature"),
            ("prop", "Prop"),
        ],
        blank=True,
        default="",
    )

    modifier_realms = models.JSONField(
        default=list,
        help_text="List of modifier realms: 'scene', 'time'",
    )

    # Cantrip details
    level = models.IntegerField(default=1, choices=[(i, str(i)) for i in range(1, 6)])
    glamour_cost = models.CharField(
        max_length=20, blank=True, default="", help_text="Glamour cost (e.g., '1 Wyrd')"
    )
    difficulty = models.IntegerField(
        default=8, help_text="Base difficulty (usually 8, modified by circumstances)"
    )
    duration = models.TextField(
        blank=True, default="", help_text="Duration of effect"
    )
    range = models.CharField(
        max_length=100, blank=True, default="", help_text="Range of effect"
    )
    effect = models.TextField(blank=True, default="", help_text="Detailed effect")
    type_of_effect = models.CharField(
        max_length=20,
        choices=[("chimerical", "Chimerical"), ("wyrd", "Wyrd"), ("both", "Both")],
        blank=True,
        default="",
    )
    bunk_examples = models.JSONField(
        default=list, help_text="List of example bunks for this cantrip"
    )

    class Meta:
        verbose_name = "Cantrip"
        verbose_name_plural = "Cantrips"

    def get_update_url(self):
        return reverse("items:changeling:update:cantrip", args=[str(self.id)])

    @classmethod
    def get_creation_url(cls):
        return reverse("items:changeling:create:cantrip")

    def get_heading(self):
        return "ctd_heading"

    def __str__(self):
        if self.art and self.name:
            return f"{self.name} ({self.art.title()} {self.level})"
        return super().__str__()
