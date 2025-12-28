from core.models import BaseMeritFlawRating
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import CheckConstraint, Q
from django.urls import reverse
from locations.models.core.location import LocationModel


class Tomb(LocationModel):
    """
    Burial place and sanctuary for Amenti.
    Similar to Haven for Vampires or Chantry for Mages.
    """

    type = "tomb"
    gameline = "mtr"

    # ========================================
    # TOMB RATING SYSTEM (Background: Tomb)
    # ========================================

    rank = models.IntegerField(
        default=1,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        help_text="Overall power/quality of the tomb (0-10)",
    )

    # Components of Tomb rating (similar to Haven)
    SIZE_CHOICES = [
        (0, "None/Cramped"),
        (1, "Small Chamber"),
        (2, "Medium Tomb"),
        (3, "Large Tomb Complex"),
        (4, "Vast Necropolis"),
        (5, "Legendary Pyramid"),
    ]

    size = models.IntegerField(
        choices=SIZE_CHOICES,
        default=1,
        help_text="Physical size of the tomb",
    )

    security = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text="Traps, magical wards, hidden entrances (0-5)",
    )

    sanctity = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text="Sacred power and connection to the underworld (0-5)",
    )

    # ========================================
    # TOMB PROPERTIES
    # ========================================

    # Era of construction
    ERA_CHOICES = [
        ("predynastic", "Predynastic (Before 3100 BCE)"),
        ("old_kingdom", "Old Kingdom (2686-2181 BCE)"),
        ("middle_kingdom", "Middle Kingdom (2055-1650 BCE)"),
        ("new_kingdom", "New Kingdom (1550-1077 BCE)"),
        ("late_period", "Late Period (664-332 BCE)"),
        ("ptolemaic", "Ptolemaic (332-30 BCE)"),
        ("modern", "Modern (Newly Created)"),
    ]

    era = models.CharField(
        max_length=20,
        choices=ERA_CHOICES,
        default="old_kingdom",
        blank=True,
        help_text="Historical period of construction",
    )

    # Special features (booleans)
    has_false_chambers = models.BooleanField(
        default=False, help_text="Decoy chambers to confuse grave robbers"
    )

    has_hieroglyphic_wards = models.BooleanField(
        default=False, help_text="Protective hieroglyphic inscriptions"
    )

    has_treasure_cache = models.BooleanField(
        default=False, help_text="Stores valuable grave goods and artifacts"
    )

    has_sarcophagus = models.BooleanField(
        default=True, help_text="Contains a sarcophagus for resting"
    )

    has_cult_shrine = models.BooleanField(
        default=False, help_text="Shrine for mortal cult followers to worship"
    )

    has_underworld_portal = models.BooleanField(
        default=False, help_text="Gateway to Duat (Egyptian underworld)"
    )

    # ========================================
    # SPIRITUAL PROPERTIES
    # ========================================

    # Ba accumulation (like Node quintessence)
    ba_per_week = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Ba generated per week when resting here",
    )

    # Tomb-specific barrier
    duat_barrier = models.IntegerField(
        default=7,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        help_text="Difficulty to access Duat (Egyptian underworld) from here",
    )

    # ========================================
    # RESONANCE & CHARACTER
    # ========================================

    # Merits and Flaws for tomb
    merits_and_flaws = models.ManyToManyField(
        "characters.MeritFlaw",
        through="TombMeritFlawRating",
        blank=True,
        help_text="Special properties and flaws of this tomb",
    )

    # Guardians (could be Ushabti, traps, curses)
    guardian_description = models.TextField(
        blank=True,
        help_text="Describe guardians: Ushabti servants, spectral protectors, traps, etc.",
    )

    # ========================================
    # HISTORY
    # ========================================

    original_occupant = models.CharField(
        max_length=200,
        blank=True,
        help_text="Who was originally buried here (if known)",
    )

    discovered_date = models.CharField(
        max_length=100,
        blank=True,
        help_text="When was this tomb discovered/entered in modern times",
    )

    archaeological_status = models.CharField(
        max_length=200,
        blank=True,
        help_text="Is it registered? Looted? Secret? Tourist site?",
    )

    # ========================================
    # HELPER METHODS
    # ========================================

    def calculate_total_rating(self):
        """Calculate total tomb rating from components"""
        return self.size + self.security + self.sanctity

    def save(self, *args, **kwargs):
        """Auto-update rank based on components"""
        self.rank = self.calculate_total_rating()
        # Lower barriers in powerful tombs
        if self.rank >= 7:
            self.duat_barrier = max(3, 7 - (self.rank - 7))
        super().save(*args, **kwargs)

    # ========================================
    # URLS
    # ========================================

    def get_absolute_url(self):
        return reverse("locations:mummy:tomb", args=[str(self.id)])

    def get_update_url(self):
        return reverse("locations:mummy:update:tomb", kwargs={"pk": self.pk})

    @classmethod
    def get_creation_url(cls):
        return reverse("locations:mummy:create:tomb")

    def get_heading(self):
        return "mtr_heading"

    class Meta:
        verbose_name = "Tomb"
        verbose_name_plural = "Tombs"


class TombMeritFlawRating(BaseMeritFlawRating):
    """Through model for Tomb merit/flaw ratings."""

    tomb = models.ForeignKey(Tomb, on_delete=models.CASCADE)

    class Meta:
        unique_together = ["tomb", "mf"]
        constraints = [
            CheckConstraint(
                check=Q(rating__gte=-10, rating__lte=10),
                name="locations_tombmeritflawrating_rating_range",
                violation_error_message="Tomb merit/flaw rating must be between -10 and 10",
            ),
        ]
