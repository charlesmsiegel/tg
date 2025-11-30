from django.db import models
from django.urls import reverse


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

    def get_absolute_url(self):
        return reverse("characters:mummy:dynasty", args=[str(self.id)])

    def get_update_url(self):
        return reverse("characters:mummy:update:dynasty", kwargs={"pk": self.pk})

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:mummy:create:dynasty")
