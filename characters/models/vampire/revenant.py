from core.linked_stat import LinkedStat
from django.db import models
from django.urls import reverse

from .vtmhuman import VtMHuman


class RevenantFamily(models.Model):
    """
    Represents a Revenant family bloodline.
    """

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    weakness = models.TextField(blank=True, help_text="Family curse or inherent weakness")

    # Family disciplines (typically 2-3)
    disciplines = models.ManyToManyField("Discipline", blank=True, related_name="revenant_families")

    class Meta:
        verbose_name = "Revenant Family"
        verbose_name_plural = "Revenant Families"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("characters:vampire:revenant_family", args=[str(self.id)])

    def get_update_url(self):
        return reverse("characters:vampire:update:revenant_family", kwargs={"pk": self.pk})

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:vampire:create:revenant_family")


class Revenant(VtMHuman):
    """
    Represents a Revenant (born ghoul from special families).
    Revenants are humans born with the ability to produce vitae naturally.
    """

    type = "revenant"
    freebie_step = 6

    allowed_backgrounds = [
        "contacts",
        "mentor",
        "allies",
        "alternate_identity",
        "resources",
        "retainers",
        "status_background",
        "generation",  # Revenants have pseudo-generation
    ]

    # Revenant family
    family = models.ForeignKey(
        RevenantFamily,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="revenants",
    )

    # Blood pool (revenants produce vitae naturally)
    blood_pool = models.IntegerField(default=10)
    max_blood_pool = models.IntegerField(default=10)
    blood = LinkedStat("max_blood_pool", "blood_pool", cap_temporary=False)

    # Pseudo-generation (typically 10-12)
    pseudo_generation = models.IntegerField(
        default=10,
        help_text="Effective generation for blood pool and discipline costs (typically 10-12)",
    )

    # Family disciplines (inherit from family)
    # Physical disciplines (common among revenants)
    potence = models.IntegerField(default=0)
    celerity = models.IntegerField(default=0)
    fortitude = models.IntegerField(default=0)

    # Mental/social disciplines (some families have these)
    auspex = models.IntegerField(default=0)
    dominate = models.IntegerField(default=0)
    obfuscate = models.IntegerField(default=0)
    presence = models.IntegerField(default=0)
    animalism = models.IntegerField(default=0)

    # Necromancy (Obertus family specialty)
    necromancy = models.IntegerField(default=0)

    # Vicissitude (Bratovich family specialty)
    vicissitude = models.IntegerField(default=0)

    # Family derangement or flaw
    family_flaw = models.TextField(
        blank=True, help_text="Inherited mental instability or physical flaw"
    )

    # Age tracking (revenants age slowly)
    actual_age = models.IntegerField(default=0, help_text="Actual chronological age in years")
    # apparent_age is inherited from Human

    class Meta:
        verbose_name = "Revenant"
        verbose_name_plural = "Revenants"

    def get_absolute_url(self):
        return reverse("characters:vampire:revenant", args=[str(self.id)])

    def get_update_url(self):
        return reverse("characters:vampire:update:revenant", kwargs={"pk": self.pk})

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:vampire:create:revenant")

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
            "Animalism": self.animalism,
            "Necromancy": self.necromancy,
            "Vicissitude": self.vicissitude,
        }
        return {k: v for k, v in disciplines.items() if v > 0}

    def get_family_disciplines(self):
        """Return list of disciplines from the revenant's family."""
        if self.family:
            return list(self.family.disciplines.all())
        return []

    def get_available_disciplines(self):
        """Return list of disciplines the revenant can learn."""
        if self.family:
            # Can learn family disciplines
            return list(self.family.disciplines.all())
        # Without a family, can only learn physical disciplines
        from characters.models.vampire.discipline import Discipline

        physical = ["Potence", "Celerity", "Fortitude"]
        return list(Discipline.objects.filter(name__in=physical))
