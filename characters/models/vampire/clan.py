from core.models import Model
from django.db import models
from django.urls import reverse

from .discipline import Discipline


class VampireClan(Model):
    """
    Represents a Vampire Clan or Bloodline.
    Examples: Brujah, Ventrue, Malkavian, Tremere, etc.
    """

    type = "vampire_clan"
    gameline = "vtm"

    # Clan attributes
    nickname = models.CharField(max_length=100, blank=True)

    # Clan Disciplines (typically 3 in-clan Disciplines)
    disciplines = models.ManyToManyField(Discipline, blank=True, related_name="clans")

    # Clan weakness description
    weakness = models.TextField(blank=True)

    # Whether this is a bloodline (vs main clan)
    is_bloodline = models.BooleanField(default=False)

    # Parent clan (for bloodlines)
    parent_clan = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="bloodlines",
    )

    class Meta:
        verbose_name = "Vampire Clan"
        verbose_name_plural = "Vampire Clans"
        ordering = ["name"]

    def get_absolute_url(self):
        return reverse("characters:vampire:clan", args=[str(self.id)])

    def get_update_url(self):
        return reverse("characters:vampire:update:clan", kwargs={"pk": self.pk})

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:vampire:create:clan")

    def get_heading(self):
        return "vtm_heading"

    def get_all_disciplines(self):
        """Get all disciplines including parent clan disciplines for bloodlines."""
        if self.parent_clan:
            return (self.disciplines.all() | self.parent_clan.disciplines.all()).distinct()
        return self.disciplines.all()
