from core.linked_stat import LinkedStat
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
    blood = LinkedStat("max_blood_pool", "blood_pool")

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

    # Virtue selection - determines which virtues are active
    has_conviction = models.BooleanField(
        default=False, help_text="If True, uses Conviction; if False, uses Conscience"
    )
    has_instinct = models.BooleanField(
        default=False, help_text="If True, uses Instinct; if False, uses Self-Control"
    )

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
            self.max_blood_pool, self.blood_per_turn = generation_table[self.generation_rating]

    def save(self, *args, **kwargs):
        """Override save to update generation-dependent values and handle path changes."""
        self.update_generation_values()

        # If a path is set, ensure virtues match the path's requirements
        if self.path:
            self.path.update_character_virtues(self)

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

    def freebie_cost(self, trait_type):
        """Return freebie point cost for vampire-specific traits."""
        vampire_costs = {
            "discipline": 7,  # In-clan disciplines
            "out_of_clan_discipline": 10,
            "virtue": 2,
            "humanity": 1,
            "path_rating": 1,
        }
        if trait_type in vampire_costs.keys():
            return vampire_costs[trait_type]
        return super().freebie_cost(trait_type)

    def is_clan_discipline(self, discipline):
        """Check if a discipline is in-clan."""
        if not self.clan:
            return False
        clan_disciplines = [d.property_name for d in self.clan.disciplines.all()]
        if isinstance(discipline, str):
            return discipline in clan_disciplines
        return discipline.property_name in clan_disciplines

    def discipline_freebies(self, form):
        """Spend freebies on disciplines."""
        discipline = form.cleaned_data["example"]
        is_clan = self.is_clan_discipline(discipline)
        cost = 7 if is_clan else 10

        # Get current rating and increment
        current_rating = getattr(self, discipline.property_name, 0)
        setattr(self, discipline.property_name, current_rating + 1)
        self.freebies -= cost

        trait = discipline.name
        value = current_rating + 1
        return trait, value, cost

    def virtue_freebies(self, form):
        """Spend freebies on virtues."""
        # Virtues cost 2 freebies per dot
        cost = 2
        virtue_name = form.cleaned_data["example"].lower()

        # Get current rating and increment
        current_rating = getattr(self, virtue_name, 1)
        setattr(self, virtue_name, current_rating + 1)
        self.freebies -= cost

        trait = virtue_name.title()
        value = current_rating + 1
        return trait, value, cost

    def humanity_freebies(self, form):
        """Spend freebies on Humanity."""
        cost = 1
        self.humanity += 1
        self.freebies -= cost
        return "Humanity", self.humanity, cost

    def path_rating_freebies(self, form):
        """Spend freebies on Path rating."""
        cost = 1
        self.path_rating += 1
        self.freebies -= cost
        return "Path Rating", self.path_rating, cost

    @property
    def active_virtue_1(self):
        """Return the rating of the first active virtue (Conviction or Conscience)."""
        return self.conviction if self.has_conviction else self.conscience

    @property
    def active_virtue_1_name(self):
        """Return the name of the first active virtue."""
        return "Conviction" if self.has_conviction else "Conscience"

    @property
    def active_virtue_2(self):
        """Return the rating of the second active virtue (Instinct or Self-Control)."""
        return self.instinct if self.has_instinct else self.self_control

    @property
    def active_virtue_2_name(self):
        """Return the name of the second active virtue."""
        return "Instinct" if self.has_instinct else "Self-Control"

    def get_active_virtues(self):
        """Return a dict of active virtues with their ratings."""
        return {
            self.active_virtue_1_name: self.active_virtue_1,
            self.active_virtue_2_name: self.active_virtue_2,
            "Courage": self.courage,
        }

    def set_virtue_by_name(self, virtue_name, value):
        """Set a virtue value by name (case-insensitive)."""
        virtue_name = virtue_name.lower()
        if virtue_name in [
            "conscience",
            "conviction",
            "self_control",
            "instinct",
            "courage",
        ]:
            setattr(self, virtue_name, value)
        else:
            raise ValueError(f"Unknown virtue: {virtue_name}")

    def xp_frequencies(self):
        """Return frequency distribution for XP spending (for random character generation)."""
        return {
            "attribute": 16,
            "ability": 20,
            "background": 13,
            "willpower": 1,
            "discipline": 35,
            "virtue": 3,
            "humanity": 1,
            "path_rating": 1,
        }

    def xp_cost(self, trait_type, trait_value=None):
        """Return XP cost for vampire-specific traits."""
        from collections import defaultdict

        costs = defaultdict(
            lambda: super().xp_cost(trait_type, trait_value) if trait_value is not None else 10000,
            {
                "new_discipline": 10,
                "clan_discipline": 5,
                "out_of_clan_discipline": 7,
                "virtue": 2,
                "humanity": 1,
                "path_rating": 1,
            },
        )

        # Handle discipline trait types
        if trait_type in ["discipline", "clan_discipline", "out_of_clan_discipline"]:
            if trait_value is not None:
                return costs[trait_type] * trait_value
            return costs[trait_type]

        # Handle virtue/morality traits
        if trait_type in ["virtue", "humanity", "path_rating"]:
            if trait_value is not None:
                return costs[trait_type] * trait_value
            return costs[trait_type]

        return costs[trait_type]

    def spend_xp(self, trait):
        """Spend XP on a trait."""
        output = super().spend_xp(trait)
        if output in [True, False]:
            return output

        # Check if trait is a discipline
        discipline_fields = [
            "celerity",
            "fortitude",
            "potence",
            "auspex",
            "dominate",
            "dementation",
            "presence",
            "animalism",
            "protean",
            "obfuscate",
            "chimerstry",
            "necromancy",
            "obtenebration",
            "quietus",
            "serpentis",
            "thaumaturgy",
            "vicissitude",
            "daimoinon",
            "melpominee",
            "mytherceria",
            "obeah",
            "temporis",
            "thanatosis",
            "valeren",
            "visceratika",
        ]

        if trait in discipline_fields:
            current_value = getattr(self, trait)

            # Determine if it's clan or out-of-clan
            from characters.models.vampire.discipline import Discipline

            try:
                discipline_obj = Discipline.objects.get(property_name=trait)
                is_clan = self.is_clan_discipline(discipline_obj)

                if current_value == 0:
                    cost = self.xp_cost("new_discipline")
                elif is_clan:
                    cost = self.xp_cost("clan_discipline", current_value + 1)
                else:
                    cost = self.xp_cost("out_of_clan_discipline", current_value + 1)

                if cost <= self.xp:
                    from core.utils import add_dot

                    if add_dot(self, trait, 5):
                        self.xp -= cost
                        self.add_to_spend(trait, getattr(self, trait), cost)
                        return True
                    return False
                return False
            except Discipline.DoesNotExist:
                return False

        # Handle virtues
        if trait in ["conscience", "conviction", "self_control", "instinct", "courage"]:
            current_value = getattr(self, trait)
            cost = self.xp_cost("virtue", current_value + 1)
            if cost <= self.xp:
                from core.utils import add_dot

                if add_dot(self, trait, 5):
                    self.xp -= cost
                    self.add_to_spend(trait, getattr(self, trait), cost)
                    return True
                return False
            return False

        # Handle humanity
        if trait == "humanity":
            cost = self.xp_cost("humanity", self.humanity + 1)
            if cost <= self.xp:
                from core.utils import add_dot

                if add_dot(self, "humanity", 10):
                    self.xp -= cost
                    self.add_to_spend(trait, self.humanity, cost)
                    return True
                return False
            return False

        # Handle path rating
        if trait == "path_rating":
            cost = self.xp_cost("path_rating", self.path_rating + 1)
            if cost <= self.xp:
                from core.utils import add_dot

                if add_dot(self, "path_rating", 10):
                    self.xp -= cost
                    self.add_to_spend(trait, self.path_rating, cost)
                    return True
                return False
            return False

        return trait

    def freebie_frequencies(self):
        """Return frequency distribution for freebie spending (for random character generation)."""
        return {
            "attribute": 15,
            "ability": 8,
            "background": 10,
            "willpower": 1,
            "meritflaw": 20,
            "discipline": 30,
            "virtue": 8,
            "humanity": 4,
            "path_rating": 4,
        }

    def freebie_costs(self):
        """Return a dictionary of freebie costs for vampire traits."""
        costs = super().freebie_costs()
        costs.update(
            {
                "discipline": 7,
                "out_of_clan_discipline": 10,
                "virtue": 2,
                "humanity": 1,
                "path_rating": 1,
            }
        )
        return costs

    def spend_freebies(self, trait):
        """Spend freebie points on a trait."""
        output = super().spend_freebies(trait)
        if output in [True, False]:
            return output

        # Check if trait is a discipline
        discipline_fields = [
            "celerity",
            "fortitude",
            "potence",
            "auspex",
            "dominate",
            "dementation",
            "presence",
            "animalism",
            "protean",
            "obfuscate",
            "chimerstry",
            "necromancy",
            "obtenebration",
            "quietus",
            "serpentis",
            "thaumaturgy",
            "vicissitude",
            "daimoinon",
            "melpominee",
            "mytherceria",
            "obeah",
            "temporis",
            "thanatosis",
            "valeren",
            "visceratika",
        ]

        if trait in discipline_fields:
            from characters.models.vampire.discipline import Discipline

            try:
                discipline_obj = Discipline.objects.get(property_name=trait)
                is_clan = self.is_clan_discipline(discipline_obj)
                cost = 7 if is_clan else 10

                if cost <= self.freebies:
                    from core.utils import add_dot

                    if add_dot(self, trait, 5):
                        self.freebies -= cost
                        return True
                    return False
                return False
            except Discipline.DoesNotExist:
                return False

        # Handle virtues
        if trait in ["conscience", "conviction", "self_control", "instinct", "courage"]:
            cost = self.freebie_cost("virtue")
            if cost <= self.freebies:
                from core.utils import add_dot

                if add_dot(self, trait, 5):
                    self.freebies -= cost
                    return True
                return False
            return False

        # Handle humanity
        if trait == "humanity":
            cost = self.freebie_cost("humanity")
            if cost <= self.freebies:
                from core.utils import add_dot

                if add_dot(self, "humanity", 10):
                    self.freebies -= cost
                    return True
                return False
            return False

        # Handle path rating
        if trait == "path_rating":
            cost = self.freebie_cost("path_rating")
            if cost <= self.freebies:
                from core.utils import add_dot

                if add_dot(self, "path_rating", 10):
                    self.freebies -= cost
                    return True
                return False
            return False

        return trait
