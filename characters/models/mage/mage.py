from collections import defaultdict

from characters.models.core.ability_block import Ability
from characters.models.core.attribute_block import Attribute
from characters.models.mage.effect import Effect
from characters.models.mage.faction import MageFaction
from characters.models.mage.focus import (
    Instrument,
    Practice,
    SpecializedPractice,
    Tenet,
)
from characters.models.mage.mtahuman import MtAHuman
from characters.models.mage.resonance import Resonance
from characters.models.mage.rote import Rote
from characters.models.mage.sphere import Sphere
from core.utils import add_dot, weighted_choice
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models, transaction
from django.db.models import CheckConstraint, Q
from items.models.core.item import ItemModel
from locations.models.mage.library import Library
from locations.models.mage.node import Node


class Mage(MtAHuman):
    type = "mage"

    freebie_step = 7

    allowed_backgrounds = [
        "contacts",
        "mentor",
        "allies",
        "alternate_identity",
        "arcane",
        "avatar",
        "backup",
        "blessing",
        "certification",
        "chantry",
        "cult",
        "demesne",
        "destiny",
        "dream",
        "enhancement",
        "fame",
        "familiar",
        "influence",
        "legend",
        "library",
        "node",
        "past_lives",
        "patron",
        "rank",
        "requisitions",
        "resources",
        "retainers",
        "sanctum",
        "secret_weapons",
        "spies",
        "status_background",
        "totem",
        "wonder",
    ]

    affiliation = models.ForeignKey(
        MageFaction,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="affiliations",
    )
    faction = models.ForeignKey(
        MageFaction,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="factions",
    )
    subfaction = models.ForeignKey(
        MageFaction,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="subfactions",
    )

    essence = models.CharField(
        default="Dynamic",
        max_length=100,
        choices=[
            ("Dynamic", "Dynamic"),
            ("Pattern", "Pattern"),
            ("Primordial", "Primordial"),
            ("Questing", "Questing"),
        ],
    )

    correspondence = models.IntegerField(default=0)
    time = models.IntegerField(default=0)
    spirit = models.IntegerField(default=0)
    mind = models.IntegerField(default=0)
    entropy = models.IntegerField(default=0)
    prime = models.IntegerField(default=0)
    forces = models.IntegerField(default=0)
    matter = models.IntegerField(default=0)
    life = models.IntegerField(default=0)

    metaphysical_tenet = models.ForeignKey(
        Tenet,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="metaphysical_tenet_of",
    )
    personal_tenet = models.ForeignKey(
        Tenet,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="personal_tenet_of",
    )
    ascension_tenet = models.ForeignKey(
        Tenet,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ascension_tenet_of",
    )

    other_tenets = models.ManyToManyField(Tenet, blank=True)
    practices = models.ManyToManyField(Practice, blank=True, through="PracticeRating")
    instruments = models.ManyToManyField(Instrument, blank=True)

    arete = models.IntegerField(default=0)

    affinity_sphere = models.ForeignKey(
        Sphere,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    CORR_NAMES = [("correspondence", "Correspondence"), ("data", "Data")]
    PRIME_NAMES = [("prime", "Prime"), ("primal_utility", "Primal Utility")]
    SPIRIT_NAMES = [
        ("spirit", "Spirit"),
        ("dimensional_science", "Dimensional Science"),
    ]

    corr_name = models.CharField(
        default="correspondence",
        choices=CORR_NAMES,
        max_length=100,
    )
    prime_name = models.CharField(
        default="prime",
        choices=PRIME_NAMES,
        max_length=100,
    )
    spirit_name = models.CharField(
        default="spirit",
        choices=SPIRIT_NAMES,
        max_length=100,
    )

    age_of_awakening = models.IntegerField(default=0)
    avatar_description = models.TextField(default="", blank=True)

    resonance = models.ManyToManyField("Resonance", through="ResRating")

    rote_points = models.IntegerField(default=6)
    rotes = models.ManyToManyField(Rote, blank=True)

    quintessence = models.IntegerField(default=0)
    paradox = models.IntegerField(default=0)

    quiet = models.IntegerField(default=0)
    quiet_type = models.CharField(
        default="none",
        max_length=10,
        choices=[
            ("none", "None"),
            ("denial", "Denial"),
            ("madness", "Madness"),
            ("morbidity", "Morbidity"),
        ],
    )

    background_points = 7

    class Meta:
        verbose_name = "Mage"
        verbose_name_plural = "Mages"
        ordering = ["name"]

    def get_affinity_sphere_name(self):
        if self.affinity_sphere == Sphere.objects.get(name="Correspondence"):
            return self.get_corr_name_display()
        if self.affinity_sphere == Sphere.objects.get(name="Prime"):
            return self.get_prime_name_display()
        if self.affinity_sphere == Sphere.objects.get(name="Spirit"):
            return self.get_spirit_name_display()
        return self.affinity_sphere

    def get_items_owned(self):
        return ItemModel.objects.filter(owned_by=self)

    def add_ability(self, ability, maximum=5):
        return add_dot(self, ability, maximum)

    @staticmethod
    def get_paradox_wheel():
        return list(range(20))

    def get_inverted_paradox(self):
        return 19 - self.paradox

    def get_spheres(self):
        return {
            "correspondence": self.correspondence,
            "time": self.time,
            "spirit": self.spirit,
            "mind": self.mind,
            "entropy": self.entropy,
            "prime": self.prime,
            "forces": self.forces,
            "matter": self.matter,
            "life": self.life,
        }

    def has_faction(self):
        return self.faction is not None

    def set_faction(self, affiliation, faction, subfaction=None):
        if faction is not None:
            if faction.parent != affiliation:
                return False
        if subfaction is not None:
            if subfaction.parent != faction:
                return False
        self.affiliation = affiliation
        self.faction = faction
        self.subfaction = subfaction
        self.save()
        return True

    def get_affiliation_weights(self):
        affiliation_weights = defaultdict(int)
        for faction in MageFaction.objects.filter(parent=None):
            if faction.name == "Traditions":
                affiliation_weights[faction] = 40
            elif faction.name == "Technocratic Union":
                affiliation_weights[faction] = 40
            elif faction.name == "The Disparate Alliance":
                affiliation_weights[faction] = 10
            elif faction.name == "Nephandi":
                affiliation_weights[faction] = 5
            elif faction.name == "Marauders":
                affiliation_weights[faction] = 5
            else:
                affiliation_weights[faction] = 1
        return affiliation_weights

    def set_quiet_type(self, quiet_type):
        self.quiet_type = quiet_type
        return True

    def set_quiet_rating(self, quiet_rating):
        self.quiet = quiet_rating
        return True

    def has_focus(self):
        return (
            self.metaphysical_tenet
            and self.personal_tenet
            and self.ascension_tenet
            and self.total_practices() == self.arete
        )

    def set_focus(self, tenets, practices):
        for tenet in tenets:
            self.add_tenet(tenet)
        for prac in practices:
            self.add_practice(prac)
        return True

    def add_background(self, background, maximum=5):
        if background in ["requisitions", "secret_weapons"]:
            if self.affiliation is not None:
                if self.affiliation.name != "Technocratic Union":
                    return False
                return add_dot(self, background, maximum)
            return False
        return add_dot(self, background, maximum)

    def total_backgrounds(self):
        return (
            super().total_backgrounds() + self.enhancement + self.sanctum + self.totem
        )

    def add_sphere(self, sphere):
        if self.faction is not None:
            if self.faction.name == "Ahl-i-Batin" and sphere == "entropy":
                return False
        return add_dot(self, sphere, min(self.arete, 5))

    def filter_spheres(self, minimum=0, maximum=5):
        return {k: v for k, v in self.get_spheres().items() if minimum <= v <= maximum}

    def total_spheres(self):
        return sum(self.get_spheres().values())

    def has_spheres(self):
        if self.affinity_sphere is not None:
            aff_flag = getattr(self, self.affinity_sphere.property_name) > 0
        else:
            aff_flag = False
        total = self.total_spheres() == 6
        return aff_flag and total

    def set_affinity_sphere(self, affinity):
        self.affinity_sphere = Sphere.objects.get(property_name=affinity)
        self.add_sphere(affinity)
        return True

    def get_affinity_sphere_options(self):
        q = Sphere.objects.none()
        if self.affiliation is not None:
            q |= self.affiliation.affinities.all()
        if self.faction is not None:
            q |= self.faction.affinities.all()
        if self.subfaction is not None:
            q |= self.subfaction.affinities.all()
        q = q.distinct()
        if q.count() == 0:
            return Sphere.objects.all()
        return q

    def has_affinity_sphere(self):
        return self.affinity_sphere is not None

    def set_corr_name(self, name):
        if name not in [x[0] for x in self.CORR_NAMES]:
            raise ValueError("Unknown Sphere Name")
        self.corr_name = name
        self.save()
        return True

    def set_prime_name(self, name):
        if name not in [x[0] for x in self.PRIME_NAMES]:
            raise ValueError("Unknown Sphere Name")
        self.prime_name = name
        self.save()
        return True

    def set_spirit_name(self, name):
        if name not in [x[0] for x in self.SPIRIT_NAMES]:
            raise ValueError("Unknown Sphere Name")
        self.spirit_name = name
        self.save()
        return True

    def add_arete(self, freebies=False):
        if freebies:
            cap = 3
        else:
            cap = 10
        return add_dot(self, "arete", cap)

    def has_essence(self):
        return self.essence != ""

    def set_essence(self, essence):
        self.essence = essence
        return True

    def add_resonance(self, resonance):
        if isinstance(resonance, str):
            resonance, _ = Resonance.objects.get_or_create(name=resonance)
        r, _ = ResRating.objects.get_or_create(resonance=resonance, mage=self)
        if r.rating == 5:
            return False
        r.rating += 1
        r.save()
        return True

    def subtract_resonance(self, resonance):
        if isinstance(resonance, str):
            resonance, _ = Resonance.objects.get_or_create(name=resonance)
        r, _ = ResRating.objects.get_or_create(resonance=resonance, mage=self)
        if r.rating == 0:
            return False
        r.rating -= 1
        r.save()
        for rr in ResRating.objects.filter(mage=self):
            if rr.rating == 0:
                rr.delete()
        return True

    def total_resonance(self):
        return sum(x.rating for x in ResRating.objects.filter(mage=self))

    def resonance_rating(self, resonance):
        if resonance not in self.resonance.all():
            return 0
        return ResRating.objects.get(mage=self, resonance=resonance).rating

    def filter_resonance(self, minimum=0, maximum=5):
        if minimum > 0:
            all_res = Resonance.objects.filter(mage__name__contains=self.name)
        else:
            all_res = Resonance.objects.all()

        maxed_resonance = [
            x.id for x in ResRating.objects.filter(mage=self, rating__gt=maximum)
        ]
        mined_resonance = [
            x.id for x in ResRating.objects.filter(mage=self, rating__lt=minimum)
        ]
        all_res = all_res.exclude(pk__in=maxed_resonance)
        all_res = all_res.exclude(pk__in=mined_resonance)
        if minimum > 0:
            all_res = all_res.filter(
                pk__in=[
                    x.resonance.id
                    for x in ResRating.objects.filter(mage=self, rating__gt=0)
                ]
            )
        return all_res

    def add_effect(self, effect):
        if effect.is_learnable(self):
            r = Rote.objects.create(effect=effect)
            self.rote_points -= effect.cost()
            self.rotes.add(r)
            return True
        return False

    def has_effects(self):
        return self.rote_points == 0

    def filter_effects(self, max_cost=100):
        effects = Effect.objects.filter(rote_cost__lte=max_cost)
        effects = effects.exclude(
            id__in=self.rotes.all().values_list("effect", flat=True)
        )

        spheres = self.get_spheres()
        spheres = {k + "__lte": v for k, v in spheres.items()}
        q = Q(**spheres)
        return effects.filter(q)

    def total_effects(self):
        return sum(x.effect.cost() for x in self.rotes.all())

    def has_specialties(self):
        output = super().has_specialties()
        for sphere in self.filter_spheres(minimum=4):
            output = output and (self.specialties.filter(stat=sphere).count() > 0)
        return output

    def needs_specialties(self):
        return len(self.needed_specialties()) > 0

    def needed_specialties(self):
        stats = (
            list(Attribute.objects.all())
            + list(
                Ability.objects.filter(
                    property_name__in=self.talents + self.skills + self.knowledges
                )
            )
            + list(Sphere.objects.all())
        )

        stats4 = [x for x in stats if getattr(self, x.property_name, 0) >= 4]
        stats1 = [
            x
            for x in stats
            if getattr(self, x.property_name, 0) >= 1
            and x.property_name
            in [
                "arts",
                "athletics",
                "crafts",
                "firearms",
                "larceny",
                "melee",
                "academics",
                "esoterica",
                "lore",
                "politics",
                "science",
            ]
        ]

        stats = stats1 + stats4

        existing_specialties = [x.stat for x in self.specialties.all()]
        stats = [x.property_name for x in stats]
        return [x for x in stats if x not in existing_specialties]

    def has_mage_history(self):
        return self.age_of_awakening != 0 and self.avatar_description != ""

    def xp_frequencies(self):
        return {
            "attribute": 16,
            "ability": 20,
            "background": 13,
            "willpower": 1,
            "sphere": 37,
            "arete": 10,
            "rote points": 2,
        }

    @transaction.atomic
    def spend_xp(self, trait):
        """
        Spend XP on a trait atomically.

        All XP spending is wrapped in a transaction to prevent race conditions.
        """
        output = super().spend_xp(trait)
        if output in [True, False]:
            return output

        # Lock the row to prevent concurrent spending
        mage = Mage.objects.select_for_update().get(pk=self.pk)

        if trait == "arete":
            cost = mage.xp_cost("arete") * getattr(mage, trait)
            if cost <= mage.xp:
                if mage.add_arete():
                    mage.xp -= cost
                    mage.add_to_spend(trait, getattr(mage, trait), cost)
                    mage.save()
                    return True
                return False
            return False
        if trait in mage.get_spheres():
            if mage.affinity_sphere == trait:
                cost = mage.xp_cost("affinity sphere") * getattr(mage, trait)
            else:
                cost = mage.xp_cost("sphere") * getattr(mage, trait)
            if cost == 0:
                cost = 10
            if mage.merits_and_flaws.filter(
                name=f"Sphere Natural - {trait.title()}"
            ).exists():
                cost *= 0.7
                if cost % 1 != 0:
                    cost += 1
                cost = int(cost)
            if mage.merits_and_flaws.filter(
                name=f"Sphere Inept - {trait.title()}"
            ).exists():
                cost *= 1.3
                if cost % 1 != 0:
                    cost += 1
                cost = int(cost)
            if cost <= mage.xp:
                if mage.add_sphere(trait):
                    mage.xp -= cost
                    mage.add_to_spend(trait, getattr(mage, trait), cost)
                    mage.save()
                    return True
                return False
            return False
        if trait == "rote points":
            cost = mage.xp_cost("rote points")
            if cost <= mage.xp:
                mage.rote_points += 3
                mage.xp -= cost
                mage.add_to_spend(trait, getattr(mage, trait.replace(" ", "_")), cost)
                mage.save()
                return True
            return False
        return trait

    def xp_cost(self, trait):
        cost = super().xp_cost(trait)
        if cost != 10000:
            return cost
        costs = defaultdict(
            lambda: 10000,
            {
                "affinity sphere": 7,
                "new sphere": 10,
                "sphere": 8,
                "arete": 8,
                "rote points": 1,
            },
        )
        return costs[trait]

    def freebie_frequencies(self):
        return {
            "attribute": 15,
            "ability": 8,
            "background": 10,
            "willpower": 1,
            "meritflaw": 20,
            "sphere": 25,
            "arete": 5,
            "quintessence": 1,
            "rote points": 5,
            "resonance": 10,
        }

    def freebie_costs(self):
        costs = super().freebie_costs()
        costs.update(
            {
                "sphere": 7,
                "arete": 4,
                "quintessence": 1,
                "rote points": 1,
                "resonance": 3,
            }
        )
        return costs

    def spend_freebies(self, trait):
        output = super().spend_freebies(trait)
        if output in [True, False]:
            return output
        if trait in self.get_spheres():
            cost = self.freebie_cost("sphere")
            if cost <= self.freebies:
                if self.add_sphere(trait):
                    self.freebies -= cost
                    return True
                return False
            return False
        if trait == "arete":
            cost = self.freebie_cost("arete")
            if cost <= self.freebies:
                if self.add_arete(freebies=True):
                    self.freebies -= cost
                    return True
                return False
            return False
        if trait == "quintessence":
            cost = self.freebie_cost("quintessence")
            if cost <= self.freebies:
                if self.quintessence < 17:
                    self.quintessence += 4
                    self.freebies -= cost
                    return True
                return False
            return False
        if trait == "rote points":
            cost = self.freebie_cost("rote points")
            if cost <= self.freebies:
                self.rote_points += 4
                self.freebies -= cost
                return True
            return False
        if Resonance.objects.filter(name=trait).exists():
            cost = self.freebie_cost("resonance") * (self.total_resonance())
            if cost <= self.freebies:
                if self.add_resonance(trait):
                    self.freebies -= cost
                    return True
                return False
            return False
        return trait

    def has_library(self):
        return (
            sum([x.rank for x in Library.objects.filter(owned_by=self)]) == self.library
        )

    def has_node(self):
        return sum([x.rank for x in Node.objects.filter(owned_by=self)]) == self.node

    def freebie_cost(self, trait_type):
        mage_costs = {
            "sphere": 7,
            "arete": 4,
            "quintessence": 1,
            "tenet": 0,
            "practice": 1,
            "rotes": 1,
            "resonance": 3,
        }
        if trait_type in mage_costs.keys():
            return mage_costs[trait_type]
        return super().freebie_cost(trait_type)

    def sphere_to_trait_type(self, trait_name):
        if trait_name == self.affinity_sphere.property_name:
            return "affinity_sphere"
        return "sphere"

    def xp_cost(self, trait_type, trait_value):
        mage_costs = {
            "new_sphere": 10,
            "affinity_sphere": 7,
            "sphere": 8,
            "arete": 8,
            "tenet": 0,
            "remove tenet": 1,
            "new_practice": 3,
            "practice": 1,
            "rotes": 1,
            "resonance": 3,
            "new_resonance": 5,
        }
        if trait_type == "sphere" and trait_value == 0:
            return mage_costs["new_sphere"]
        if trait_type == "practice" and trait_value == 0:
            return mage_costs["new_practice"]
        if trait_type == "resonance" and trait_value == 0:
            return mage_costs["new_resonance"]
        elif trait_type in mage_costs.keys():
            return mage_costs[trait_type] * trait_value
        return super().xp_cost(trait_type, trait_value)

    def add_tenet(self, tenet):
        if tenet.tenet_type not in ["met", "asc", "per"]:
            self.other_tenets.add(tenet)
        if tenet.tenet_type == "met" and self.metaphysical_tenet is None:
            self.metaphysical_tenet = tenet
        elif tenet.tenet_type == "per" and self.personal_tenet is None:
            self.personal_tenet = tenet
        elif tenet.tenet_type == "asc" and self.ascension_tenet is None:
            self.ascension_tenet = tenet
        else:
            self.other_tenets.add(tenet)
        return True

    def add_practice(self, practice):
        pr = PracticeRating.objects.get_or_create(mage=self, practice=practice)[0]
        pr.rating += 1
        pr.save()
        return True

    def practice_rating(self, practice):
        prs = PracticeRating.objects.filter(mage=self)
        if practice not in [x.practice for x in prs]:
            return 0
        return PracticeRating.objects.get(mage=self, practice=practice).rating

    def total_practices(self):
        return sum([self.practice_rating(x) for x in Practice.objects.all()])

    def get_practices(self):
        return PracticeRating.objects.filter(mage=self, rating__gt=0)

    def get_resonance(self):
        return ResRating.objects.filter(mage=self, rating__gte=1).order_by(
            "resonance__name"
        )

    def sphere_freebies(self, form):
        cost = 7
        trait = form.cleaned_data["example"]
        value = getattr(self, trait.property_name) + 1
        self.add_sphere(trait.property_name)
        self.freebies -= cost
        trait = trait.name
        return trait, value, cost

    def rotes_freebies(self, form):
        trait = "Rote Points"
        cost = 1
        value = 4
        self.rote_points += 4
        self.freebies -= cost
        return trait, value, cost

    def resonance_freebies(self, form):
        trait = Resonance.objects.get(name=form.data["resonance"])
        value = self.object.resonance_rating(trait) + 1
        self.add_resonance(trait.name)
        cost = 3
        self.freebies -= cost
        trait = trait.name
        return trait, value, cost

    def tenet_freebies(self, form):
        cost = 0
        trait = form.cleaned_data["example"]
        value = ""
        self.add_tenet(trait)
        self.freebies -= cost
        trait = trait.name
        return trait, value, cost

    def practice_freebies(self, form):
        trait = form.cleaned_data["example"]
        cost = 1
        value = self.practice_rating(trait) + 1
        self.add_practice(trait)
        self.freebies -= cost
        trait = trait.name
        return trait, value, cost

    def arete_freebies(self, form):
        if self.arete >= 3 and self.total_freebies() != 45:
            form.add_error(None, "Arete Cannot Be Raised Above 3 At Character Creation")
            return super().form_invalid(form)
        if self.arete >= 4 and self.total_freebies() == 45:
            form.add_error(None, "Arete Cannot Be Raised Above 4 At Character Creation")
            return super().form_invalid(form)
        prac = form.cleaned_data["example"]
        trait = f"Arete ({prac.name})"
        cost = 4
        value = getattr(self, "arete") + 1
        self.add_practice(prac)
        self.add_arete()
        self.freebies -= cost
        return trait, value, cost

    def quintessence_freebies(self, form):
        trait = "Quintessence"
        value = 4
        cost = 1
        self.quintessence += 4
        self.freebies -= cost
        return trait, value, cost


class ResRating(models.Model):
    mage = models.ForeignKey("Mage", on_delete=models.SET_NULL, null=True)
    resonance = models.ForeignKey(Resonance, on_delete=models.SET_NULL, null=True)
    rating = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(10)]
    )

    class Meta:
        verbose_name = "Mage Resonance Rating"
        verbose_name_plural = "Mage Resonance Ratings"
        constraints = [
            CheckConstraint(
                check=Q(rating__gte=0, rating__lte=10),
                name="characters_mage_resrating_rating_range",
                violation_error_message="Resonance rating must be between 0 and 10",
            ),
        ]


class PracticeRating(models.Model):
    mage = models.ForeignKey(Mage, on_delete=models.SET_NULL, null=True)
    practice = models.ForeignKey(Practice, on_delete=models.SET_NULL, null=True)
    rating = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(10)]
    )

    class Meta:
        constraints = [
            CheckConstraint(
                check=Q(rating__gte=0, rating__lte=10),
                name="characters_mage_practicerating_rating_range",
                violation_error_message="Practice rating must be between 0 and 10",
            ),
        ]

    def __str__(self):
        mage_name = self.mage.name if self.mage else "No Mage"
        practice_name = str(self.practice) if self.practice else "No Practice"
        return f"{mage_name}: {practice_name}: {self.rating}"

    def get_tenet_bonus(self):
        """
        Calculate the net tenet bonus/penalty for this practice.
        Returns:
            -1 if the practice is ONLY limited by tenets
            +1 if the practice is ONLY associated to tenets
            0 otherwise
        """
        if not self.mage or not self.practice:
            return 0

        # Get all tenets for this mage
        all_tenets = []
        if self.mage.metaphysical_tenet:
            all_tenets.append(self.mage.metaphysical_tenet)
        if self.mage.personal_tenet:
            all_tenets.append(self.mage.personal_tenet)
        if self.mage.ascension_tenet:
            all_tenets.append(self.mage.ascension_tenet)
        all_tenets.extend(self.mage.other_tenets.all())

        # Check if practice is in associated or limited practices
        is_associated = False
        is_limited = False

        for tenet in all_tenets:
            if self.practice in tenet.associated_practices.all():
                is_associated = True
            if self.practice in tenet.limited_practices.all():
                is_limited = True

        # Calculate bonus
        if is_limited and not is_associated:
            return -1
        elif is_associated and not is_limited:
            return +1
        else:
            return 0
