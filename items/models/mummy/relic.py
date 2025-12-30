from core.models import BaseResonanceRating
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from items.models.core.item import ItemModel


class MummyRelic(ItemModel):
    """
    Ancient Egyptian magical artifacts and items of power.
    Represents Background: Artifact for Mummy.
    """

    type = "mummy_relic"
    gameline = "mtr"

    # ========================================
    # POWER RATING
    # ========================================

    rank = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Power level of the artifact (1-10)",
    )

    background_cost = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Background points required to possess (usually equals rank)",
    )

    # ========================================
    # ARTIFACT PROPERTIES
    # ========================================

    RELIC_TYPE_CHOICES = [
        ("weapon", "Weapon (Khopesh, staff, etc.)"),
        ("jewelry", "Jewelry (Amulet, ankh, scarab, etc.)"),
        ("scroll", "Scroll or Papyrus"),
        ("canopic", "Canopic Jar"),
        ("statue", "Statue or Figurine"),
        ("crown", "Crown or Headdress"),
        ("tool", "Ritual Tool"),
        ("clothing", "Sacred Garment"),
        ("other", "Other"),
    ]

    relic_type = models.CharField(
        max_length=20,
        choices=RELIC_TYPE_CHOICES,
        default="jewelry",
        help_text="Type of artifact",
    )

    # Historical provenance
    ERA_CHOICES = [
        ("predynastic", "Predynastic"),
        ("old_kingdom", "Old Kingdom"),
        ("middle_kingdom", "Middle Kingdom"),
        ("new_kingdom", "New Kingdom"),
        ("late_period", "Late Period"),
        ("ptolemaic", "Ptolemaic"),
        ("unknown", "Unknown/Mythical"),
    ]

    era = models.CharField(
        max_length=20,
        choices=ERA_CHOICES,
        default="old_kingdom",
        blank=True,
        help_text="Historical period of creation",
    )

    original_owner = models.CharField(
        max_length=200,
        blank=True,
        help_text="Pharaoh, priest, or other original owner",
    )

    # ========================================
    # MAGICAL PROPERTIES
    # ========================================

    # Powers and abilities
    powers = models.TextField(
        blank=True, help_text="Describe the artifact's magical powers and effects"
    )

    # Ba cost to activate
    ba_cost = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(20)],
        help_text="Ba points required to activate (0 = passive)",
    )

    # Hekau association
    associated_hekau = models.CharField(
        max_length=50,
        blank=True,
        help_text="Hekau path this artifact is tied to (if any)",
    )

    # Activation requirements
    requires_sekhem = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        help_text="Minimum Sekhem required to use (0 = no requirement)",
    )

    requires_ritual = models.BooleanField(
        default=False, help_text="Does activation require a ritual?"
    )

    # ========================================
    # SPECIAL PROPERTIES
    # ========================================

    is_cursed = models.BooleanField(default=False, help_text="Does this artifact carry a curse?")

    is_unique = models.BooleanField(default=False, help_text="Is this a one-of-a-kind artifact?")

    is_sentient = models.BooleanField(
        default=False, help_text="Does the artifact have its own will/consciousness?"
    )

    # Resonance (similar to Mage Wonders)
    resonance = models.ManyToManyField(
        "characters.Resonance",  # Reuse Mage's Resonance model from characters app
        through="RelicResonanceRating",
        blank=True,
        help_text="Mystical resonance of the artifact",
    )

    # ========================================
    # PHYSICAL DESCRIPTION
    # ========================================

    material = models.CharField(
        max_length=100,
        blank=True,
        help_text="Gold, lapis lazuli, obsidian, etc.",
    )

    hieroglyphic_inscription = models.TextField(
        blank=True, help_text="Any hieroglyphic text on the item"
    )

    # ========================================
    # HISTORY & LORE
    # ========================================

    history = models.TextField(blank=True, help_text="Historical background and legends")

    current_location_notes = models.TextField(
        blank=True, help_text="How was it recovered? Where has it been?"
    )

    # ========================================
    # HELPER METHODS
    # ========================================

    def can_activate(self, mummy):
        """Check if a mummy can activate this relic"""
        if self.requires_sekhem > mummy.sekhem:
            return False
        if self.ba_cost > mummy.ba:
            return False
        return True

    def save(self, *args, **kwargs):
        """Auto-set background_cost to rank if not specified"""
        if not self.background_cost:
            self.background_cost = self.rank
        super().save(*args, **kwargs)

    # ========================================
    # URLS
    # ========================================

    def get_absolute_url(self):
        return reverse("items:mummy:relic", args=[str(self.id)])

    def get_update_url(self):
        return reverse("items:mummy:update:relic", kwargs={"pk": self.pk})

    @classmethod
    def get_creation_url(cls):
        return reverse("items:mummy:create:relic")

    def get_heading(self):
        return "mtr_heading"

    class Meta:
        verbose_name = "Mummy Relic"
        verbose_name_plural = "Mummy Relics"


# Through model for Resonance
class RelicResonanceRating(BaseResonanceRating):
    relic = models.ForeignKey(MummyRelic, on_delete=models.CASCADE)
    resonance = models.ForeignKey("characters.Resonance", on_delete=models.CASCADE)
    # Override default to 1 for RelicResonanceRating
    rating = models.IntegerField(
        default=1, validators=[MinValueValidator(0), MaxValueValidator(10)]
    )

    class Meta:
        unique_together = ["relic", "resonance"]
