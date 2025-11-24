from django.db import models
from django.urls import reverse

from locations.models.core import LocationModel


class HuntingGround(LocationModel):
    """
    Area patrolled and monitored by hunters.
    Territory where hunters track and combat supernatural threats.
    """

    type = "hunting_ground"

    # Territory stats
    size = models.IntegerField(
        default=1,
        help_text="Size of territory (1-5: blocks to districts)",
    )

    population = models.IntegerField(
        default=1,
        help_text="Population density (1-5)",
    )

    supernatural_activity = models.IntegerField(
        default=1,
        help_text="Level of supernatural activity (1-5)",
    )

    # Known threats
    THREAT_TYPES = [
        ("vampire", "Vampire Activity"),
        ("werewolf", "Werewolf Activity"),
        ("mage", "Mage Activity"),
        ("wraith", "Ghost Activity"),
        ("changeling", "Fae Activity"),
        ("demon", "Infernal Activity"),
        ("unknown", "Unknown Supernatural"),
        ("mixed", "Multiple Threats"),
    ]

    primary_threat = models.CharField(
        max_length=50,
        choices=THREAT_TYPES,
        blank=True,
        help_text="Primary type of supernatural threat",
    )

    threat_description = models.TextField(
        blank=True,
        help_text="Details about known threats in the area",
    )

    # Control
    is_contested = models.BooleanField(
        default=False,
        help_text="Territory contested by rival hunters or supernaturals",
    )

    control_level = models.IntegerField(
        default=1,
        help_text="Hunter's control over the area (1-5)",
    )

    # Related hunters
    rival_cells = models.ManyToManyField(
        "characters.Hunter",
        blank=True,
        related_name="rival_territories",
    )

    # Intelligence
    contact_network = models.IntegerField(
        default=0,
        help_text="Network of informants and contacts (0-5)",
    )

    surveillance_coverage = models.IntegerField(
        default=0,
        help_text="Surveillance and monitoring coverage (0-5)",
    )

    # Events
    last_incident = models.DateField(
        blank=True,
        null=True,
        help_text="Date of last supernatural incident",
    )

    incident_log = models.TextField(
        blank=True,
        help_text="Log of incidents and encounters",
    )

    # Notable locations
    key_locations = models.TextField(
        blank=True,
        help_text="Important locations within the territory",
    )

    # Total rating
    total_rating = models.IntegerField(
        default=0,
        help_text="Total territory value/danger rating",
    )

    class Meta:
        verbose_name = "Hunting Ground"
        verbose_name_plural = "Hunting Grounds"

    def get_update_url(self):
        return reverse("locations:hunter:update:hunting_ground", args=[str(self.id)])

    @classmethod
    def get_creation_url(cls):
        return reverse("locations:hunter:create:hunting_ground")

    def get_heading(self):
        return "htr_heading"

    def calculate_total_rating(self):
        """Calculate total hunting ground value/danger."""
        total = (
            self.size
            + self.population
            + self.supernatural_activity
            + self.contact_network
            + self.surveillance_coverage
            + self.control_level
        )

        # Penalties
        if self.is_contested:
            total -= 2

        self.total_rating = max(0, total)
        return self.total_rating

    def save(self, *args, **kwargs):
        """Override save to recalculate total rating."""
        self.calculate_total_rating()
        super().save(*args, **kwargs)
