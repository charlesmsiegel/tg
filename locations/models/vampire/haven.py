from characters.models.core import MeritFlaw
from django.db import models
from django.urls import reverse
from locations.models.core import LocationModel


class HavenSizeChoices(models.IntegerChoices):
    CRAMPED = 1, "Cramped (1 dot)"
    SMALL = 2, "Small (2 dots)"
    AVERAGE = 3, "Average (3 dots)"
    SPACIOUS = 4, "Spacious (4 dots)"
    LUXURIOUS = 5, "Luxurious (5 dots)"


class Haven(LocationModel):
    """
    Represents a Vampire's Haven (resting place/sanctuary).
    Based on the Haven Background (V20, p.111).
    """

    type = "haven"

    # Haven attributes (Background dots)
    size = models.IntegerField(default=1, choices=HavenSizeChoices.choices)
    security = models.IntegerField(default=0)
    location = models.IntegerField(
        default=0,
        help_text="Quality of location (prestige, safety, convenience)",
    )

    # Total Haven Background value (typically size + security + location + any other factors)
    total_rating = models.IntegerField(default=0)

    # Special features
    has_guardian = models.BooleanField(
        default=False, help_text="Haven protected by guardian (ghoul, etc.)"
    )
    has_luxury = models.BooleanField(
        default=False, help_text="Haven has luxurious appointments"
    )
    is_hidden = models.BooleanField(
        default=False, help_text="Haven location is concealed"
    )
    has_library = models.BooleanField(
        default=False, help_text="Haven contains library"
    )
    has_workshop = models.BooleanField(
        default=False, help_text="Haven contains workshop"
    )

    # Merits and Flaws
    merits_and_flaws = models.ManyToManyField(
        MeritFlaw, blank=True, through="HavenMeritFlawRating"
    )

    class Meta:
        verbose_name = "Haven"
        verbose_name_plural = "Havens"

    def get_update_url(self):
        return reverse("locations:vampire:update:haven", args=[str(self.id)])

    @classmethod
    def get_creation_url(cls):
        return reverse("locations:vampire:create:haven")

    def get_heading(self):
        return "vtm_heading"

    def calculate_total_rating(self):
        """Calculate total Haven Background rating."""
        total = self.size + self.security + self.location
        if self.has_guardian:
            total += 1
        if self.has_luxury:
            total += 1
        if self.is_hidden:
            total += 1
        if self.has_library:
            total += 1
        if self.has_workshop:
            total += 1
        self.total_rating = total
        return total

    def save(self, *args, **kwargs):
        """Override save to recalculate total rating."""
        self.calculate_total_rating()
        super().save(*args, **kwargs)


class HavenMeritFlawRating(models.Model):
    """Through table for Haven merits and flaws with ratings."""

    haven = models.ForeignKey(Haven, on_delete=models.CASCADE)
    mf = models.ForeignKey(MeritFlaw, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    class Meta:
        unique_together = ("haven", "mf")
