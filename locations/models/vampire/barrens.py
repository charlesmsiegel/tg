from django.db import models
from django.urls import reverse
from locations.models.core import LocationModel


class Barrens(LocationModel):
    """
    Represents Barrens - dangerous, contested, or abandoned vampire territory.
    The Barrens are areas outside normal Camarilla control, often Anarch zones
    or no-man's-land between vampire domains.
    """

    type = "barrens"

    # Territory characteristics
    size = models.IntegerField(
        default=1,
        help_text="Size of the barrens territory (1-5 dots)",
    )

    danger_level = models.IntegerField(
        default=3,
        help_text="How dangerous the area is (1=relatively safe, 5=extremely deadly)",
    )

    population_density = models.IntegerField(
        default=0,
        help_text="Mortal population density (0=abandoned, 5=densely populated)",
    )

    # Control and politics
    is_contested = models.BooleanField(
        default=True,
        help_text="Multiple factions fighting for control",
    )

    is_anarch_territory = models.BooleanField(
        default=False,
        help_text="Controlled by Anarchs",
    )

    is_sabbat_territory = models.BooleanField(
        default=False,
        help_text="Controlled by Sabbat",
    )

    is_unclaimed = models.BooleanField(
        default=False,
        help_text="No faction has claimed this territory",
    )

    controlling_faction = models.CharField(
        max_length=200,
        blank=True,
        help_text="Name of gang, coterie, or faction that controls this area",
    )

    # Resources and features
    has_feeding_grounds = models.BooleanField(
        default=True,
        help_text="Area has mortals available for feeding",
    )

    feeding_quality = models.IntegerField(
        default=1,
        help_text="Quality of available vessels (1=desperate/dangerous, 5=plentiful/safe)",
    )

    has_shelter = models.BooleanField(
        default=True,
        help_text="Abandoned buildings or structures that can provide shelter",
    )

    has_resources = models.BooleanField(
        default=False,
        help_text="Area contains valuable resources (weapons, money, etc.)",
    )

    # Threats
    masquerade_threat = models.IntegerField(
        default=3,
        help_text="Risk of Masquerade breaches (1=low risk, 5=constant breaches)",
    )

    lupine_activity = models.BooleanField(
        default=False,
        help_text="Werewolves active in this territory",
    )

    hunter_activity = models.BooleanField(
        default=False,
        help_text="Vampire hunters active in this area",
    )

    mortal_gang_activity = models.BooleanField(
        default=False,
        help_text="Dangerous mortal gangs operate here",
    )

    # Barrens type
    barrens_type = models.CharField(
        max_length=100,
        blank=True,
        help_text="E.g., 'Industrial wasteland', 'Ruined district', 'War zone', 'Slums'",
    )

    # Notable features
    notable_locations = models.TextField(
        blank=True,
        help_text="Abandoned factories, gang hideouts, ruins, etc.",
    )

    class Meta:
        verbose_name = "Barrens"
        verbose_name_plural = "Barrens"

    def get_update_url(self):
        return reverse("locations:vampire:update:barrens", args=[str(self.id)])

    @classmethod
    def get_creation_url(cls):
        return reverse("locations:vampire:create:barrens")

    def get_heading(self):
        return "vtm_heading"

    def get_control_status(self):
        """Return a description of who controls this territory."""
        if self.is_unclaimed:
            return "Unclaimed"
        if self.is_anarch_territory:
            return "Anarch"
        if self.is_sabbat_territory:
            return "Sabbat"
        if self.is_contested:
            return "Contested"
        if self.controlling_faction:
            return self.controlling_faction
        return "Unknown"
