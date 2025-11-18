from django.db import models
from django.urls import reverse

from .clan import VampireClan
from .discipline import Discipline
from .path import Path
from .sect import VampireSect
from .title import VampireTitle
from .vtmhuman import VtMHuman


class Vampire(VtMHuman):
    """
    Represents a Vampire character (embraced undead).
    """

    type = "vampire"
    freebie_step = 7

    allowed_backgrounds = [
        "contacts",
        "mentor",
        "allies",
        "alternate_identity",
        "black_hand_membership",
        "domain",
        "fame",
        "generation",
        "herd",
        "influence",
        "resources",
        "retainers",
        "rituals",
        "status_background",
    ]

    # Clan and Sect
    clan = models.ForeignKey(
        VampireClan,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="vampires",
    )

    sect = models.ForeignKey(
        VampireSect,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="vampires",
    )

    # Sire
    sire = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="childer",
    )

    # Generation (3rd - 15th typically)
    generation_rating = models.IntegerField(default=13)

    # Blood Pool
    blood_pool = models.IntegerField(default=10)
    max_blood_pool = models.IntegerField(default=10)
    blood_per_turn = models.IntegerField(default=1)

    # Physical Disciplines
    celerity = models.IntegerField(default=0)
    fortitude = models.IntegerField(default=0)
    potence = models.IntegerField(default=0)

    # Mental Disciplines
    auspex = models.IntegerField(default=0)
    dominate = models.IntegerField(default=0)
    dementation = models.IntegerField(default=0)

    # Social Disciplines
    presence = models.IntegerField(default=0)

    # Animalistic Disciplines
    animalism = models.IntegerField(default=0)
    protean = models.IntegerField(default=0)

    # Stealth Disciplines
    obfuscate = models.IntegerField(default=0)

    # Unique Clan Disciplines
    chimerstry = models.IntegerField(default=0)
    necromancy = models.IntegerField(default=0)
    obtenebration = models.IntegerField(default=0)
    quietus = models.IntegerField(default=0)
    serpentis = models.IntegerField(default=0)
    thaumaturgy = models.IntegerField(default=0)
    vicissitude = models.IntegerField(default=0)

    # Bloodline Unique Disciplines
    daimoinon = models.IntegerField(default=0)
    melpominee = models.IntegerField(default=0)
    mytherceria = models.IntegerField(default=0)
    obeah = models.IntegerField(default=0)
    temporis = models.IntegerField(default=0)
    thanatosis = models.IntegerField(default=0)
    valeren = models.IntegerField(default=0)
    visceratika = models.IntegerField(default=0)

    # Virtues (Camarilla)
    conscience = models.IntegerField(default=1)
    self_control = models.IntegerField(default=1)
    courage = models.IntegerField(default=1)

    # Virtues (Sabbat alternative)
    conviction = models.IntegerField(default=0)
    instinct = models.IntegerField(default=0)

    # Morality
    humanity = models.IntegerField(default=7)
    path = models.ForeignKey(
        Path,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="followers",
    )
    path_rating = models.IntegerField(default=0)

    # Willpower (may already be in Human, but including here for clarity)
    willpower = models.IntegerField(default=3)
    current_willpower = models.IntegerField(default=3)

    # Titles
    titles = models.ManyToManyField(VampireTitle, blank=True, related_name="holders")

    class Meta:
        verbose_name = "Vampire"
        verbose_name_plural = "Vampires"

    def get_absolute_url(self):
        return reverse("characters:vampire:vampire", args=[str(self.id)])

    def get_update_url(self):
        return reverse("characters:vampire:update:vampire", kwargs={"pk": self.pk})

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:vampire:create:vampire")

    def get_heading(self):
        return "vtm_heading"

    def update_generation_values(self):
        """Update max blood pool and blood per turn based on generation."""
        generation_table = {
            3: (50, 10),
            4: (50, 10),
            5: (40, 8),
            6: (30, 6),
            7: (20, 4),
            8: (15, 3),
            9: (14, 2),
            10: (13, 1),
            11: (12, 1),
            12: (11, 1),
            13: (10, 1),
            14: (10, 1),
            15: (10, 1),
        }
        if self.generation_rating in generation_table:
            self.max_blood_pool, self.blood_per_turn = generation_table[
                self.generation_rating
            ]

    def save(self, *args, **kwargs):
        """Override save to update generation-dependent values."""
        self.update_generation_values()
        super().save(*args, **kwargs)

    def get_disciplines(self):
        """Return a dictionary of all disciplines with their ratings."""
        disciplines = {
            "Celerity": self.celerity,
            "Fortitude": self.fortitude,
            "Potence": self.potence,
            "Auspex": self.auspex,
            "Dominate": self.dominate,
            "Dementation": self.dementation,
            "Presence": self.presence,
            "Animalism": self.animalism,
            "Protean": self.protean,
            "Obfuscate": self.obfuscate,
            "Chimerstry": self.chimerstry,
            "Necromancy": self.necromancy,
            "Obtenebration": self.obtenebration,
            "Quietus": self.quietus,
            "Serpentis": self.serpentis,
            "Thaumaturgy": self.thaumaturgy,
            "Vicissitude": self.vicissitude,
            "Daimoinon": self.daimoinon,
            "Melpominee": self.melpominee,
            "Mytherceria": self.mytherceria,
            "Obeah": self.obeah,
            "Temporis": self.temporis,
            "Thanatosis": self.thanatosis,
            "Valeren": self.valeren,
            "Visceratika": self.visceratika,
        }
        return {k: v for k, v in disciplines.items() if v > 0}

    def get_clan_disciplines(self):
        """Return list of in-clan disciplines."""
        if self.clan:
            return list(self.clan.disciplines.all())
        return []
