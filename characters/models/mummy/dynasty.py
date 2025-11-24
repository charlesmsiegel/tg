from django.db import models


class Dynasty(models.Model):
    """
    Historical lineages of Amenti from different eras.
    Similar to Clans for Vampires - represents the era and culture
    from which the mummy originates.
    """

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    era = models.CharField(
        max_length=100,
        blank=True,
        help_text="Historical period (e.g., Old Kingdom, Middle Kingdom, etc.)",
    )
    favored_hekau = models.CharField(
        max_length=50, blank=True, help_text="Hekau path this dynasty traditionally favors"
    )

    class Meta:
        verbose_name = "Dynasty"
        verbose_name_plural = "Dynasties"

    def __str__(self):
        return self.name
