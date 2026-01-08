from core.linked_stat import LinkedStat
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
    blood = LinkedStat("max_blood_pool", "blood_pool")

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

    # Virtues (ghouls have standard mortal virtues)
    conscience = models.IntegerField(default=1)
    self_control = models.IntegerField(default=1)
    courage = models.IntegerField(default=1)

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

    def freebie_cost(self, trait_type):
        """Return freebie point cost for ghoul-specific traits."""
        ghoul_costs = {
            "discipline": 7,  # Physical disciplines easier for ghouls
        }
        if trait_type in ghoul_costs.keys():
            return ghoul_costs[trait_type]
        return super().freebie_cost(trait_type)

    def get_available_disciplines(self):
        """Return list of disciplines the ghoul can learn."""
        if self.domitor and self.domitor.clan:
            # Can learn domitor's clan disciplines
            return list(self.domitor.clan.disciplines.all())
        # Independent ghouls can learn physical disciplines
        from characters.models.vampire.discipline import Discipline

        physical = ["Potence", "Celerity", "Fortitude"]
        return list(Discipline.objects.filter(name__in=physical))

    def discipline_freebies(self, form):
        """Spend freebies on disciplines."""
        discipline = form.cleaned_data["example"]
        cost = 7

        # Get current rating and increment
        current_rating = getattr(self, discipline.property_name, 0)
        setattr(self, discipline.property_name, current_rating + 1)
        self.freebies -= cost

        trait = discipline.name
        value = current_rating + 1
        return trait, value, cost
