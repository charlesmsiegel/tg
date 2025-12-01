from django.db import models
from django.urls import reverse
from locations.models.core import LocationModel


class Domain(LocationModel):
    """
    Represents a Domain (territory controlled by a vampire).
    Based on the Domain Background (V20, p.110).
    """

    type = "domain"
    gameline = "vtm"

    # Domain size and quality
    size = models.IntegerField(
        default=0,
        help_text="Size of domain (1-5 dots)",
    )

    # Domain population/resources
    population = models.IntegerField(
        default=0,
        help_text="Population density and quality (1-5 dots)",
    )

    # Domain security/control
    control = models.IntegerField(
        default=0,
        help_text="Level of control over domain (1-5 dots)",
    )

    # Total Domain Background value
    total_rating = models.IntegerField(default=0)

    # Special features
    is_elysium = models.BooleanField(
        default=False,
        help_text="Domain contains or overlaps with Elysium",
    )

    has_rack = models.BooleanField(
        default=False, help_text="Domain contains quality hunting grounds"
    )

    is_disputed = models.BooleanField(default=False, help_text="Domain is contested by others")

    # Domain type
    domain_type = models.CharField(
        max_length=100,
        blank=True,
        help_text="E.g., 'Nightclub district', 'University campus', 'Industrial park'",
    )

    class Meta:
        verbose_name = "Domain"
        verbose_name_plural = "Domains"

    def get_update_url(self):
        return reverse("locations:vampire:update:domain", args=[str(self.id)])

    @classmethod
    def get_creation_url(cls):
        return reverse("locations:vampire:create:domain")

    def get_heading(self):
        return "vtm_heading"

    def calculate_total_rating(self):
        """Calculate total Domain Background rating."""
        total = self.size + self.population + self.control
        if self.has_rack:
            total += 1
        if self.is_disputed:
            total -= 1  # Disputed domains are worth less
        self.total_rating = max(0, total)  # Don't go negative
        return self.total_rating

    def save(self, *args, **kwargs):
        """Override save to recalculate total rating."""
        self.calculate_total_rating()
        super().save(*args, **kwargs)
