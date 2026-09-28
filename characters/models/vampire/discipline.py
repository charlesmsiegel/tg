from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from characters.models.core.statistic import Statistic
from characters.rules.limits import VAMPIRE_DISCIPLINES


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

    def save(self, *args, **kwargs):
        # Reference data can omit this name, but chargen and spending use it
        # to address a concrete Vampire rating field.
        if not self.property_name:
            field_name = slugify(self.name).replace("-", "_")
            if field_name in VAMPIRE_DISCIPLINES.fields:
                self.property_name = field_name
                if kwargs.get("update_fields") is not None:
                    kwargs["update_fields"] = set(kwargs["update_fields"]) | {"property_name"}
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("characters:vampire:discipline", args=[str(self.id)])

    def get_update_url(self):
        return reverse("characters:vampire:update:discipline", args=[str(self.pk)])
