from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import CheckConstraint, Q
from django.urls import reverse
from items.models.core import ItemModel


class Treasure(ItemModel):
    """
    Treasures are magically powerful items created or bound with Glamour.
    They represent enchanted artifacts available to Changelings.
    """

    type = "treasure"
    gameline = "ctd"

    rating = models.IntegerField(
        default=1,
        choices=[(i, str(i)) for i in range(1, 6)],
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="1-2 dots: Minor, 3-4: Significant, 5: Legendary",
    )

    # Treasure type
    treasure_type = models.CharField(
        max_length=30,
        choices=[
            ("weapon", "Weapon"),
            ("armor", "Armor"),
            ("talisman", "Talisman"),
            ("wonder", "Wonder"),
            ("other", "Other"),
        ],
        blank=True,
        default="",
    )

    # Creation and properties
    creator = models.CharField(
        max_length=100, blank=True, default="", help_text="Who created this Treasure"
    )
    creation_method = models.TextField(blank=True, default="", help_text="How it was created")
    permanence = models.BooleanField(default=True, help_text="Whether this Treasure is permanent")

    # Abilities and effects
    effects = models.JSONField(
        default=list, blank=True, help_text="List of special abilities/effects"
    )  # list is callable - safe
    special_abilities = models.TextField(
        blank=True, default="", help_text="Description of special abilities"
    )

    # Glamour properties
    glamour_storage = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(50)],
        help_text="If it can store Glamour, how much",
    )
    glamour_affinity = models.CharField(
        max_length=30,
        blank=True,
        default="",
        help_text="Type of Glamour it attracts or uses",
    )

    class Meta:
        verbose_name = "Treasure"
        verbose_name_plural = "Treasures"
        constraints = [
            CheckConstraint(
                check=Q(rating__gte=1, rating__lte=5),
                name="items_treasure_rating_range",
                violation_error_message="Treasure rating must be between 1 and 5",
            ),
            CheckConstraint(
                check=Q(glamour_storage__gte=0, glamour_storage__lte=50),
                name="items_treasure_glamour_storage_range",
                violation_error_message="Glamour storage must be between 0 and 50",
            ),
        ]

    def get_update_url(self):
        return reverse("items:changeling:update:treasure", args=[str(self.id)])

    @classmethod
    def get_creation_url(cls):
        return reverse("items:changeling:create:treasure")

    def get_heading(self):
        return "ctd_heading"

    def __str__(self):
        if self.name and self.rating:
            return f"{self.name} (★{'★' * (self.rating - 1)})"
        return super().__str__()
