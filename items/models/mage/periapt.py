from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import CheckConstraint, Q
from django.urls import reverse

from .wonder import Wonder


class Periapt(Wonder):
    type = "periapt"

    arete = models.IntegerField(default=0)
    power = models.ForeignKey(
        "characters.Effect", blank=True, null=True, on_delete=models.SET_NULL
    )
    max_charges = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        help_text="Maximum number of charges the periapt can hold",
    )
    current_charges = models.IntegerField(
        default=1,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Current number of charges remaining",
    )
    is_consumable = models.BooleanField(
        default=True, help_text="Whether the periapt is destroyed when charges are depleted"
    )

    class Meta:
        verbose_name = "Periapt"
        verbose_name_plural = "Periapts"
        constraints = [
            CheckConstraint(
                check=Q(arete__gte=0, arete__lte=10),
                name="items_periapt_arete_range",
                violation_error_message="Periapt arete must be between 0 and 10",
            ),
            CheckConstraint(
                check=Q(max_charges__gte=1, max_charges__lte=100),
                name="items_periapt_max_charges_range",
                violation_error_message="Periapt max charges must be between 1 and 100",
            ),
            CheckConstraint(
                check=Q(current_charges__gte=0, current_charges__lte=100),
                name="items_periapt_current_charges_range",
                violation_error_message="Periapt current charges must be between 0 and 100",
            ),
        ]

    def get_update_url(self):
        return reverse("items:mage:update:periapt", args=[str(self.id)])

    @classmethod
    def get_creation_url(cls):
        return reverse("items:mage:create:periapt")

    def set_power(self, power):
        self.power = power
        self.save()
        return True

    def has_power(self):
        return self.power is not None

    def use_charge(self):
        """Use one charge from the periapt. Returns True if successful, False if no charges remain."""
        if self.current_charges > 0:
            self.current_charges -= 1
            self.save()
            return True
        return False

    def recharge(self, amount=1):
        """Recharge the periapt by the specified amount. Cannot exceed max_charges."""
        new_charges = min(self.current_charges + amount, self.max_charges)
        self.current_charges = new_charges
        self.save()
        return True

    def is_depleted(self):
        """Check if the periapt has no charges remaining."""
        return self.current_charges == 0

    def charges_remaining(self):
        """Return the number of charges remaining."""
        return self.current_charges
