from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from game.models import Chronicle


class PhysicalPlace(models.Model):
    """
    Represents a mundane physical location in the real world.

    A PhysicalPlace can be associated with multiple LocationModel instances
    (e.g., a Node, Elysium, Haunt, etc.) to represent different supernatural
    aspects of the same physical location.

    This allows cross-gameline integration where:
    - Pike Place Market can be both a Node (Mage) and a Rack (Vampire)
    - A church can be an Elysium (Vampire), a Haunt (Wraith), and more
    - Seattle as a City can have multiple supernatural Domains, Holdings, etc.
    """

    name = models.CharField(max_length=200)
    description = models.TextField(default="", blank=True)

    # Address/location info
    address = models.CharField(max_length=500, blank=True)
    city = models.CharField(max_length=200, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)

    # Geographic coordinates (optional)
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )

    # Place type (mundane classification)
    PLACE_TYPE_CHOICES = [
        ("building", "Building"),
        ("landmark", "Landmark"),
        ("park", "Park/Green Space"),
        ("district", "District/Neighborhood"),
        ("city", "City"),
        ("region", "Region/Area"),
        ("underground", "Underground/Subterranean"),
        ("waterway", "Waterway"),
        ("other", "Other"),
    ]
    place_type = models.CharField(
        max_length=20, choices=PLACE_TYPE_CHOICES, default="building"
    )

    # Ownership and access
    owner = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True
    )
    chronicle = models.ForeignKey(
        Chronicle, on_delete=models.SET_NULL, blank=True, null=True
    )

    # Visibility
    display = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Physical Place"
        verbose_name_plural = "Physical Places"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("locations:physical_place", args=[str(self.id)])

    def get_update_url(self):
        return reverse("locations:update:physical_place", args=[str(self.id)])

    @classmethod
    def get_creation_url(cls):
        return reverse("locations:create:physical_place")

    def get_supernatural_locations(self):
        """
        Get all supernatural locations linked to this physical place.

        Returns a queryset of all LocationModel instances that reference
        this PhysicalPlace.
        """
        return self.locations.all()

    def get_supernatural_locations_by_gameline(self):
        """
        Get supernatural locations grouped by gameline.

        Returns a dict mapping gameline codes to lists of locations.
        """
        from django.conf import settings

        locations = self.get_supernatural_locations().select_related("polymorphic_ctype")
        result = {}
        for loc in locations:
            gameline = loc.get_gameline()
            if gameline not in result:
                result[gameline] = []
            result[gameline].append(loc)
        return result

    def get_full_address(self):
        """Return formatted full address."""
        parts = []
        if self.address:
            parts.append(self.address)
        if self.city:
            parts.append(self.city)
        if self.state:
            parts.append(self.state)
        if self.postal_code:
            parts.append(self.postal_code)
        if self.country:
            parts.append(self.country)
        return ", ".join(parts)

    def has_coordinates(self):
        """Check if geographic coordinates are set."""
        return self.latitude is not None and self.longitude is not None

    def clean(self):
        """Validate physical place data before saving."""
        super().clean()
        errors = {}

        # Validate name is not empty
        if not self.name or not self.name.strip():
            errors["name"] = "Name is required"

        # Validate coordinates are both set or both empty
        if (self.latitude is None) != (self.longitude is None):
            errors["latitude"] = "Both latitude and longitude must be provided, or neither"
            errors["longitude"] = "Both latitude and longitude must be provided, or neither"

        # Validate latitude range
        if self.latitude is not None:
            if self.latitude < -90 or self.latitude > 90:
                errors["latitude"] = "Latitude must be between -90 and 90"

        # Validate longitude range
        if self.longitude is not None:
            if self.longitude < -180 or self.longitude > 180:
                errors["longitude"] = "Longitude must be between -180 and 180"

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        """Ensure validation runs on save."""
        self.full_clean()
        super().save(*args, **kwargs)
