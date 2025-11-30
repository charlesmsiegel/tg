from django.db import models
from django.urls import reverse


class MummyTitle(models.Model):
    """
    Ranks and titles within Amenti society.
    Similar to Vampire titles - represents status and position.
    """

    name = models.CharField(max_length=100, unique=True)
    rank_level = models.IntegerField(
        default=0, help_text="Numerical rank (higher = more prestigious)"
    )
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Mummy Title"
        verbose_name_plural = "Mummy Titles"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("characters:mummy:title", args=[str(self.id)])

    def get_update_url(self):
        return reverse("characters:mummy:update:title", kwargs={"pk": self.pk})

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:mummy:create:title")
