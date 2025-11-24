from core.models import Model
from django.db import models
from django.urls import reverse

from .sect import VampireSect


class VampireTitle(Model):
    """
    Represents a Vampire Title (position of authority).
    Examples: Prince, Primogen, Archbishop, Ductus, Baron, etc.
    """

    type = "vampire_title"
    gameline = "vtm"

    # Title attributes
    sect = models.ForeignKey(
        VampireSect,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="titles",
    )

    # Point value of title (for social interactions)
    value = models.IntegerField(default=0, help_text="Title value (0-7 points)")

    # Whether this is a negative title
    is_negative = models.BooleanField(
        default=False, help_text="Negative titles subtract from social dice pools"
    )

    # Title description and powers
    powers = models.TextField(blank=True, help_text="Powers and responsibilities")

    class Meta:
        verbose_name = "Vampire Title"
        verbose_name_plural = "Vampire Titles"
        ordering = ["-value", "name"]

    def get_absolute_url(self):
        return reverse("characters:vampire:title", args=[str(self.id)])

    def get_update_url(self):
        return reverse("characters:vampire:update:title", kwargs={"pk": self.pk})

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:vampire:create:title")

    def get_heading(self):
        return "vtm_heading"
