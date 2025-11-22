from characters.models.core.statistic import Statistic
from django.db import models


class Discipline(Statistic):
    """
    Represents a Vampire Discipline (supernatural power).
    Examples: Celerity, Fortitude, Potence, Dominate, etc.
    """

    description = models.TextField(
        blank=True, help_text="Description of the Discipline and its powers."
    )

    type = "discipline"

    class Meta:
        verbose_name = "Discipline"
        verbose_name_plural = "Disciplines"
