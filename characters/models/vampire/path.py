from core.models import Model
from django.db import models
from django.urls import reverse


class Path(Model):
    """
    Represents a Path of Enlightenment (alternative to Humanity).
    Examples: Path of Caine, Path of Death and the Soul, Path of Honorable Accord
    """

    type = "path"

    # Path attributes
    virtues_required = models.CharField(
        max_length=200,
        blank=True,
        help_text="E.g., 'Conviction and Instinct' or 'Conviction and Self-Control'"
    )

    # Path description and ethics
    ethics = models.TextField(blank=True, help_text="The moral code of this Path")

    class Meta:
        verbose_name = "Path of Enlightenment"
        verbose_name_plural = "Paths of Enlightenment"
        ordering = ["name"]

    def get_absolute_url(self):
        return reverse("characters:vampire:path", args=[str(self.id)])

    def get_update_url(self):
        return reverse("characters:vampire:update:path", kwargs={"pk": self.pk})

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:vampire:create:path")

    def get_heading(self):
        return "vtm_heading"
