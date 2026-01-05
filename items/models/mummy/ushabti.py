from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from items.models.core.item import ItemModel


class Ushabti(ItemModel):
    """
    Animated servant statues created through Hekau: Effigy or Ushabti.
    Can be activated to perform tasks or serve as guardians.
    """

    type = "ushabti"
    gameline = "mtr"

    # ========================================
    # POWER LEVEL
    # ========================================

    rank = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Power/capability of the ushabti (1-5)",
    )

    # ========================================
    # ANIMATION PROPERTIES
    # ========================================

    is_currently_animated = models.BooleanField(
        default=False, help_text="Is this ushabti currently active/alive?"
    )

    ba_to_animate = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Ba required to animate (usually equals rank)",
    )

    ba_per_day = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Ba consumed per day while animated",
    )

    # Duration (hours or days)
    animation_duration_hours = models.IntegerField(
        default=24,
        validators=[MinValueValidator(1)],
        help_text="How long animation lasts before needing renewal",
    )

    # ========================================
    # CAPABILITIES
    # ========================================

    PURPOSE_CHOICES = [
        ("guardian", "Guardian/Warrior"),
        ("servant", "Servant/Butler"),
        ("laborer", "Laborer/Worker"),
        ("spy", "Spy/Scout"),
        ("messenger", "Messenger"),
        ("craftsman", "Craftsman/Artisan"),
        ("scribe", "Scribe/Scholar"),
    ]

    purpose = models.CharField(
        max_length=20,
        choices=PURPOSE_CHOICES,
        default="servant",
        help_text="What task was this ushabti designed for?",
    )

    # Physical capabilities (simplified attributes)
    physical_rating = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Physical strength/combat ability (1-5)",
    )

    mental_rating = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Intelligence/skill capability (1-5)",
    )

    # Special abilities
    special_abilities = models.TextField(
        blank=True, help_text="Any special powers or skills this ushabti has"
    )

    # ========================================
    # PHYSICAL FORM
    # ========================================

    MATERIAL_CHOICES = [
        ("clay", "Clay"),
        ("wood", "Wood"),
        ("stone", "Stone"),
        ("gold", "Gold/Precious Metal"),
        ("bone", "Bone"),
        ("wax", "Wax"),
    ]

    material = models.CharField(
        max_length=20,
        choices=MATERIAL_CHOICES,
        default="clay",
        help_text="Material the ushabti is made from",
    )

    size_description = models.CharField(
        max_length=100,
        default="Small statuette",
        help_text="Physical size: statuette, man-sized, etc.",
    )

    appearance = models.TextField(blank=True, help_text="Detailed appearance when animated")

    # ========================================
    # COMMANDS & CONTROL
    # ========================================

    command_word = models.CharField(
        max_length=100,
        blank=True,
        help_text="Word or phrase to activate/deactivate",
    )

    obeys_only_creator = models.BooleanField(
        default=True, help_text="Can only the creator command this ushabti?"
    )

    creator = models.ForeignKey(
        "characters.Mummy",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="created_ushabti",
        help_text="Mummy who created this ushabti",
    )

    # ========================================
    # HELPER METHODS
    # ========================================

    def animate(self, mummy):
        """Attempt to animate the ushabti"""
        if self.obeys_only_creator and self.creator != mummy:
            return False, "This ushabti only obeys its creator"

        if mummy.ba < self.ba_to_animate:
            return False, f"Requires {self.ba_to_animate} Ba to animate"

        mummy.spend_ba(self.ba_to_animate)
        self.is_currently_animated = True
        self.save()
        return True, "Ushabti animated successfully"

    def deactivate(self):
        """Deactivate the ushabti"""
        self.is_currently_animated = False
        self.save()

    def save(self, *args, **kwargs):
        """Auto-set costs based on rank"""
        self.ba_to_animate = self.rank
        self.ba_per_day = self.rank
        super().save(*args, **kwargs)

    # ========================================
    # URLS
    # ========================================

    def get_absolute_url(self):
        return reverse("items:mummy:ushabti", args=[str(self.id)])

    def get_update_url(self):
        return reverse("items:mummy:update:ushabti", kwargs={"pk": self.pk})

    @classmethod
    def get_creation_url(cls):
        return reverse("items:mummy:create:ushabti")

    class Meta:
        verbose_name = "Ushabti"
        verbose_name_plural = "Ushabti"
