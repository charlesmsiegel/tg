from django.db import models
from django.urls import reverse

from locations.models.core import LocationModel


class Nihil(LocationModel):
    """Void in the Tempest where nothing exists - dangerous empty zones."""

    type = "nihil"
    gameline = "wto"

    VOID_TYPE_CHOICES = [
        ("emptiness", "Pure Emptiness - Complete void"),
        ("corruption", "Corruption Zone - Tainted by Oblivion"),
        ("maelstrom_scar", "Maelstrom Scar - Remnant of great storm"),
        ("spectre_nest", "Spectre Nest - Spawning ground"),
        ("forgotten", "Forgotten Place - Erased from memory"),
        ("transition", "Transition Zone - Between realms"),
        ("other", "Other"),
    ]

    STABILITY_CHOICES = [
        ("permanent", "Permanent - Fixed void"),
        ("expanding", "Expanding - Growing larger"),
        ("contracting", "Contracting - Shrinking"),
        ("unstable", "Unstable - Constantly shifting"),
        ("ephemeral", "Ephemeral - Temporary phenomenon"),
    ]

    void_type = models.CharField(max_length=20, choices=VOID_TYPE_CHOICES, default="emptiness")

    stability = models.CharField(max_length=20, choices=STABILITY_CHOICES, default="permanent")

    # Hazard ratings
    hazard_level = models.IntegerField(
        default=10, help_text="Overall danger level (1-10, higher = more dangerous)"
    )
    oblivion_proximity = models.IntegerField(
        default=5,
        help_text="Proximity to Oblivion itself (1-10, higher = closer)",
    )
    entropy_rating = models.IntegerField(
        default=5,
        help_text="Rate of entropy and dissolution (1-10)",
    )

    # Size and scope
    estimated_size = models.CharField(
        max_length=200,
        blank=True,
        help_text="Approximate dimensions (e.g., '100 yards across', 'infinite')",
    )

    # Effects on travelers
    corpus_drain = models.BooleanField(
        default=True, help_text="Drains Corpus from wraiths who enter"
    )
    pathos_drain = models.BooleanField(
        default=True, help_text="Drains Pathos from wraiths who enter"
    )
    memory_loss = models.BooleanField(
        default=False, help_text="Causes memory loss or disorientation"
    )
    shadow_attraction = models.BooleanField(
        default=False, help_text="Attracts and empowers Shadows"
    )

    # Navigation
    avoidable = models.BooleanField(
        default=True, help_text="Can be navigated around with knowledge"
    )
    marked = models.BooleanField(default=False, help_text="Marked or charted by travelers")

    # Phenomena
    spectral_activity = models.IntegerField(default=0, help_text="Level of Spectre presence (0-10)")
    contains_relics = models.BooleanField(
        default=False, help_text="May contain lost relics or artifacts"
    )

    # Origin (optional narrative)
    origin_story = models.TextField(
        blank=True,
        help_text="How this void came to be (e.g., 'Destroyed Necropolis', 'Ancient battle site')",
    )

    class Meta:
        verbose_name = "Nihil"
        verbose_name_plural = "Nihils"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} (Nihil)"

    def get_absolute_url(self):
        return reverse("locations:wraith:nihil", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("locations:wraith:update:nihil", args=[str(self.id)])

    @classmethod
    def get_creation_url(cls):
        return reverse("locations:wraith:create:nihil")
