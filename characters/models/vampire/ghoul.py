from django.db import models
from django.urls import reverse

from .clan import VampireClan
from .vtmhuman import VtMHuman


class Ghoul(VtMHuman):
    """
    Represents a Ghoul (mortal who has consumed vampire blood).
    """

    type = "ghoul"
    freebie_step = 6

    allowed_backgrounds = [
        "contacts",
        "mentor",
        "allies",
        "alternate_identity",
        "resources",
        "retainers",
        "status_background",
    ]

    # Domitor (vampire master)
    domitor = models.ForeignKey(
        "Vampire",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ghouls",
    )

    # Whether this is an independent ghoul
    is_independent = models.BooleanField(default=False)

    # Blood pool (limited for ghouls)
    blood_pool = models.IntegerField(default=0)
    max_blood_pool = models.IntegerField(default=2)

    # Potence (all ghouls get 1 dot of Potence automatically)
    potence = models.IntegerField(default=1)

    # Optional additional disciplines (learned from domitor)
    celerity = models.IntegerField(default=0)
    fortitude = models.IntegerField(default=0)
    auspex = models.IntegerField(default=0)
    dominate = models.IntegerField(default=0)
    obfuscate = models.IntegerField(default=0)
    presence = models.IntegerField(default=0)

    # Years as ghoul (affects aging)
    years_as_ghoul = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Ghoul"
        verbose_name_plural = "Ghouls"

    def get_absolute_url(self):
        return reverse("characters:vampire:ghoul", args=[str(self.id)])

    def get_update_url(self):
        return reverse("characters:vampire:update:ghoul", kwargs={"pk": self.pk})

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:vampire:create:ghoul")

    def get_heading(self):
        return "vtm_heading"

    def get_disciplines(self):
        """Return a dictionary of all disciplines with their ratings."""
        disciplines = {
            "Potence": self.potence,
            "Celerity": self.celerity,
            "Fortitude": self.fortitude,
            "Auspex": self.auspex,
            "Dominate": self.dominate,
            "Obfuscate": self.obfuscate,
            "Presence": self.presence,
        }
        return {k: v for k, v in disciplines.items() if v > 0}
