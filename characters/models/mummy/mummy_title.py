from django.db import models


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
