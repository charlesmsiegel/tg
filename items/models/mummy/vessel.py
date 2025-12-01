from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from items.models.core.item import ItemModel


class Vessel(ItemModel):
    """
    Magical container for storing Ba/Sekhem energy.
    Represents Background: Vessel for Mummy.
    Like a battery for spiritual power.
    """

    type = "vessel"
    gameline = "mtr"

    # ========================================
    # CAPACITY
    # ========================================

    rank = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Quality/power of the vessel (1-10)",
    )

    background_cost = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Background points (usually equals rank)",
    )

    # Storage capacity (Ba points)
    max_ba = models.IntegerField(
        default=10,
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        help_text="Maximum Ba this vessel can store",
    )

    current_ba = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Current Ba stored",
    )

    # ========================================
    # VESSEL TYPE
    # ========================================

    VESSEL_TYPE_CHOICES = [
        ("canopic", "Canopic Jar"),
        ("scarab", "Scarab Amulet"),
        ("ankh", "Ankh"),
        ("crystal", "Crystal or Gemstone"),
        ("urn", "Ceremonial Urn"),
        ("statue", "Small Statue"),
        ("cartouche", "Cartouche"),
        ("other", "Other"),
    ]

    vessel_type = models.CharField(
        max_length=20,
        choices=VESSEL_TYPE_CHOICES,
        default="canopic",
        help_text="Form of the vessel",
    )

    # ========================================
    # TRANSFER PROPERTIES
    # ========================================

    # How much Ba can be transferred per turn
    transfer_rate = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Ba per turn that can be added/withdrawn",
    )

    # Efficiency (some Ba might be lost in transfer)
    efficiency = models.IntegerField(
        default=100,
        validators=[MinValueValidator(50), MaxValueValidator(100)],
        help_text="Percentage of Ba retained during transfer (50-100%)",
    )

    # ========================================
    # SPECIAL PROPERTIES
    # ========================================

    is_portable = models.BooleanField(default=True, help_text="Can this vessel be easily carried?")

    requires_ritual = models.BooleanField(
        default=False, help_text="Does transferring Ba require a ritual?"
    )

    is_attuned = models.BooleanField(
        default=False,
        help_text="Is this vessel attuned to a specific mummy? (only they can use it)",
    )

    # If attuned, to whom?
    attuned_to = models.ForeignKey(
        "characters.Mummy",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="attuned_vessels",
        help_text="Mummy this vessel is attuned to",
    )

    # ========================================
    # PHYSICAL DESCRIPTION
    # ========================================

    material = models.CharField(
        max_length=100,
        blank=True,
        help_text="Gold, alabaster, lapis lazuli, etc.",
    )

    inscriptions = models.TextField(blank=True, help_text="Hieroglyphic or magical inscriptions")

    # ========================================
    # HELPER METHODS
    # ========================================

    def store_ba(self, amount):
        """Store Ba in vessel, return actual amount stored"""
        space_available = self.max_ba - self.current_ba
        # Apply transfer rate limit
        amount = min(amount, self.transfer_rate)
        # Apply space limit
        amount_to_store = min(amount, space_available)
        # Apply efficiency
        actual_stored = int(amount_to_store * (self.efficiency / 100.0))

        self.current_ba += actual_stored
        self.save()
        return actual_stored

    def withdraw_ba(self, amount):
        """Withdraw Ba from vessel, return actual amount withdrawn"""
        # Apply transfer rate limit
        amount = min(amount, self.transfer_rate)
        # Apply current storage limit
        amount_to_withdraw = min(amount, self.current_ba)

        self.current_ba -= amount_to_withdraw
        self.save()
        return amount_to_withdraw

    def is_full(self):
        """Is the vessel at maximum capacity?"""
        return self.current_ba >= self.max_ba

    def is_empty(self):
        """Is the vessel depleted?"""
        return self.current_ba == 0

    def can_use(self, mummy):
        """Check if a mummy can use this vessel"""
        if self.is_attuned and self.attuned_to != mummy:
            return False
        return True

    def save(self, *args, **kwargs):
        """Auto-calculate max_ba from rank, set background_cost"""
        self.max_ba = self.rank * 10
        self.background_cost = self.rank
        # Ensure current doesn't exceed max
        self.current_ba = min(self.current_ba, self.max_ba)
        super().save(*args, **kwargs)

    # ========================================
    # URLS
    # ========================================

    def get_absolute_url(self):
        return reverse("items:mummy:vessel", args=[str(self.id)])

    def get_update_url(self):
        return reverse("items:mummy:update:vessel", kwargs={"pk": self.pk})

    @classmethod
    def get_creation_url(cls):
        return reverse("items:mummy:create:vessel")

    def get_heading(self):
        return "mtr_heading"

    class Meta:
        verbose_name = "Vessel"
        verbose_name_plural = "Vessels"
