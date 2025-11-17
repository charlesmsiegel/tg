from django.db import models
from items.models.core import ItemModel


class Relic(ItemModel):
    """Demonic artifact or relic."""

    type = "relic"

    # Type of relic
    relic_type = models.CharField(
        max_length=100,
        default="enhanced",
        choices=[
            ("enhanced", "Enhanced Relic"),
            ("enchanted", "Enchanted Relic"),
            ("house_specific", "House-Specific Relic"),
        ],
    )

    # Complexity level for enhanced relics (1-10)
    complexity = models.IntegerField(default=1)

    # Lore used to create the relic
    lore_used = models.CharField(max_length=200, default="")

    # Power/effect description
    power = models.TextField(default="")

    # Material suitability
    material = models.TextField(default="")

    # House association (for house-specific relics)
    house = models.ForeignKey(
        "characters.House",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="relics",
    )

    # Whether the relic is permanent
    is_permanent = models.BooleanField(default=False)

    # Difficulty to create/use
    difficulty = models.IntegerField(default=6)

    # Dice pool for effects
    dice_pool = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Relic"
        verbose_name_plural = "Relics"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.get_relic_type_display()})"

    def set_complexity(self, complexity):
        """Set the complexity level (1-10)."""
        if 1 <= complexity <= 10:
            self.complexity = complexity
            self.save()
            return True
        return False

    def has_complexity(self):
        """Check if complexity is set."""
        return self.complexity > 0

    def set_difficulty(self, difficulty):
        """Set the difficulty rating."""
        if difficulty >= 2:
            self.difficulty = difficulty
            self.save()
            return True
        return False
