from collections import defaultdict

from characters.models.demon.dtf_human import DtFHuman
from characters.models.demon.faction import DemonFaction
from characters.models.demon.house import DemonHouse
from characters.models.demon.lore import Lore
from characters.models.demon.lore_block import LoreBlock
from characters.models.demon.visage import Visage
from core.utils import add_dot
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models, transaction
from django.db.models import CheckConstraint, Q
from django.urls import reverse


class Demon(LoreBlock, DtFHuman):
    """Main Demon character class."""

    type = "demon"

    freebie_step = 7

    allowed_backgrounds = [
        "contacts",
        "mentor",
        "allies",
        "alternate_identity",
        "cult",
        "eminence",
        "fame",
        "followers",
        "influence",
        "legacy",
        "pacts",
        "paragon",
        "resources",
        "retainers",
        "ritual_knowledge",
        "status_background",
    ]

    # House and Faction
    house = models.ForeignKey(
        DemonHouse,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="demons",
    )
    faction = models.ForeignKey(
        DemonFaction,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="members",
    )

    # Visage (descriptive aspect of apocalyptic form)
    visage = models.ForeignKey(
        Visage,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="demons",
    )

    # Apocalyptic Form (the actual traits)
    apocalyptic_form = models.ForeignKey(
        "ApocalypticForm",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="demons",
    )

    # Faith and Torment
    faith = models.IntegerField(default=3)  # Permanent Faith rating (1-10)
    temporary_faith = models.IntegerField(default=3)  # Temporary Faith pool
    torment = models.IntegerField(default=3)  # Permanent Torment rating (0-10)
    temporary_torment = models.IntegerField(default=0)  # Temporary Torment

    # Virtues (replaces some Human virtues with Demon-specific ones)
    conviction = models.IntegerField(default=1)  # 1-5
    courage = models.IntegerField(default=1)  # 1-5
    conscience = models.IntegerField(default=1)  # 1-5

    # Thralls (many-to-many through Pact)
    thralls = models.ManyToManyField("Thrall", blank=True, through="Pact", related_name="masters")

    # Lores inherited from LoreBlock

    # Learned rituals
    rituals = models.ManyToManyField("Ritual", blank=True, related_name="demons_who_know")

    # Host information
    days_until_consumption = models.IntegerField(default=30)

    # Celestial names
    celestial_name = models.CharField(max_length=200, default="", blank=True)

    # History
    age_of_fall = models.IntegerField(default=0)
    abyss_duration = models.TextField(default="", blank=True)  # Time in the Abyss

    background_points = 5
    apocalyptic_form_points = 16  # Point budget for apocalyptic form traits

    class Meta:
        verbose_name = "Demon"
        verbose_name_plural = "Demons"
        ordering = ["name"]

    def get_absolute_url(self):
        return reverse("characters:demon:demon", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("characters:demon:update:demon", kwargs={"pk": self.pk})

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:demon:create:demon")

    def get_heading(self):
        return "dtf_heading"

    # Lore methods (get_lores, total_lores, add_lore, filter_lores) inherited from LoreBlock

    def has_lores(self):
        """Check if demon has spent starting 3 dots in lores."""
        return self.total_lores() >= 3

    def has_house(self):
        """Check if demon has selected a house."""
        return self.house is not None

    def set_house(self, house):
        """Set the demon's house and starting torment."""
        self.house = house
        self.torment = house.starting_torment
        self.save()
        return True

    def has_faction(self):
        """Check if demon has selected a faction."""
        return self.faction is not None

    def set_faction(self, faction):
        """Set the demon's faction."""
        self.faction = faction
        self.save()
        return True

    def has_visage(self):
        """Check if demon has selected a visage."""
        return self.visage is not None

    def set_visage(self, visage):
        """Set the demon's visage."""
        self.visage = visage
        self.save()
        return True

    def add_faith(self):
        """Add a dot of permanent Faith."""
        return add_dot(self, "faith", 10)

    def add_torment(self):
        """Add a dot of permanent Torment (usually bad!)."""
        if self.torment >= 10:
            return False
        self.torment += 1
        self.save()
        return True

    def reduce_torment(self):
        """Reduce permanent Torment by 1 (costs 10 XP)."""
        if self.torment <= 0:
            return False
        self.torment -= 1
        self.save()
        return True

    def has_virtues(self):
        """Check if virtues are properly set."""
        return (
            self.conviction >= 1
            and self.courage >= 1
            and self.conscience >= 1
            and (self.conviction + self.courage + self.conscience) == 6
        )

    # Apocalyptic Form methods - delegate to ApocalypticForm object
    def has_apocalyptic_form(self):
        """Check if demon has a valid apocalyptic form."""
        return self.apocalyptic_form is not None and self.apocalyptic_form.is_valid()

    def get_low_torment_traits(self):
        """Get low torment apocalyptic form traits."""
        if self.apocalyptic_form:
            return self.apocalyptic_form.low_torment_traits.all()
        from characters.models.demon.apocalyptic_form import ApocalypticFormTrait

        return ApocalypticFormTrait.objects.none()

    def get_high_torment_traits(self):
        """Get high torment apocalyptic form traits."""
        if self.apocalyptic_form:
            return self.apocalyptic_form.high_torment_traits.all()
        from characters.models.demon.apocalyptic_form import ApocalypticFormTrait

        return ApocalypticFormTrait.objects.none()

    def apocalyptic_form_low_torment_count(self):
        """Count low torment traits in apocalyptic form."""
        if self.apocalyptic_form:
            return self.apocalyptic_form.low_torment_count()
        return 0

    def apocalyptic_form_high_torment_count(self):
        """Count high torment traits in apocalyptic form."""
        if self.apocalyptic_form:
            return self.apocalyptic_form.high_torment_count()
        return 0

    def apocalyptic_form_points_spent(self):
        """Calculate total points spent on apocalyptic form traits."""
        if self.apocalyptic_form:
            return self.apocalyptic_form.total_points()
        return 0

    def apocalyptic_form_points_remaining(self):
        """Calculate remaining points for apocalyptic form."""
        if self.apocalyptic_form:
            return self.apocalyptic_form.points_remaining()
        return 16

    # Ritual methods
    def get_rituals(self):
        """Get all rituals this demon knows."""
        return self.rituals.all().order_by("house__name", "name")

    def knows_ritual(self, ritual):
        """Check if demon knows a specific ritual."""
        return ritual in self.rituals.all()

    def add_ritual(self, ritual):
        """Learn a new ritual."""
        if ritual in self.rituals.all():
            return False
        self.rituals.add(ritual)
        return True

    def remove_ritual(self, ritual):
        """Forget a ritual."""
        if ritual in self.rituals.all():
            self.rituals.remove(ritual)
            return True
        return False

    def get_available_rituals(self):
        """
        Get rituals available to learn based on house and lore knowledge.
        Returns rituals not yet learned that the demon has the primary lore for.
        """
        from characters.models.demon.ritual import Ritual

        if not self.house:
            return Ritual.objects.none()

        # Get rituals demon doesn't know yet
        unknown_rituals = Ritual.objects.exclude(id__in=self.rituals.values_list("id", flat=True))

        # Filter to house rituals
        house_rituals = unknown_rituals.filter(house=self.house)

        # Filter to rituals where demon has sufficient primary lore
        available = []
        for ritual in house_rituals:
            if ritual.primary_lore:
                lore_attr = f"lore_of_{ritual.primary_lore.property_name}"
                if (
                    hasattr(self, lore_attr)
                    and getattr(self, lore_attr) >= ritual.primary_lore_rating
                ):
                    available.append(ritual.id)

        return house_rituals.filter(id__in=available)

    def ritual_knowledge_xp_cost(self):
        """Get starting rituals based on Ritual Knowledge background."""
        from characters.models.core.background_block import BackgroundRating

        ritual_knowledge_ratings = BackgroundRating.objects.filter(
            char=self, bg__property_name="ritual_knowledge"
        )
        total = sum(r.rating for r in ritual_knowledge_ratings)
        # Each dot provides 6 XP worth of rituals
        return total * 6

    def has_demon_history(self):
        """Check if demon has celestial name and history."""
        return self.celestial_name != "" and self.age_of_fall != 0

    def get_pacts(self):
        """Get all pacts this demon has with thralls."""
        from characters.models.demon.pact import Pact

        return Pact.objects.filter(demon=self)

    def add_pact(self, thrall, terms="", faith_payment=0, enhancements=None):
        """Create a new pact with a thrall."""
        from characters.models.demon.pact import Pact

        if enhancements is None:
            enhancements = []

        pact = Pact.objects.create(
            demon=self,
            thrall=thrall,
            terms=terms,
            faith_payment=faith_payment,
            enhancements=enhancements,
        )
        return pact

    def total_pacts(self):
        """Get total number of active pacts."""
        return self.get_pacts().filter(active=True).count()

    def xp_frequencies(self):
        """XP spending frequencies for random spending."""
        return {
            "attribute": 16,
            "ability": 20,
            "background": 10,
            "willpower": 1,
            "lore": 35,
            "faith": 15,
            "virtue": 3,
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
        demon = Demon.objects.select_for_update().get(pk=self.pk)

        # Faith
        if trait == "faith":
            cost = demon.xp_cost("faith") * demon.faith
            if cost <= demon.xp:
                if demon.add_faith():
                    demon.xp -= cost
                    demon.add_to_spend(trait, demon.faith, cost)
                    demon.save(update_fields=["xp", "faith", "spent_xp"])
                    return True
            return False

        # Lores
        if trait in demon.get_lores():
            current_rating = getattr(demon, trait)
            if demon.house and trait in [
                f"lore_of_{lore.property_name}" for lore in demon.house.lores.all()
            ]:
                cost = demon.xp_cost("house_lore") * (current_rating + 1)
            else:
                cost = demon.xp_cost("other_lore") * (current_rating + 1)

            if cost <= demon.xp:
                if demon.add_lore(trait):
                    demon.xp -= cost
                    demon.add_to_spend(trait, getattr(demon, trait), cost)
                    demon.save()
                    return True
            return False

        # Virtues
        if trait in ["conviction", "courage", "conscience"]:
            cost = demon.xp_cost("virtue") * getattr(demon, trait)
            if cost <= demon.xp:
                if add_dot(demon, trait, 5):
                    demon.xp -= cost
                    demon.add_to_spend(trait, getattr(demon, trait), cost)
                    demon.save()
                    return True
            return False

        # Torment reduction
        if trait == "reduce_torment":
            cost = demon.xp_cost("reduce_torment")
            if cost <= demon.xp:
                if demon.reduce_torment():
                    demon.xp -= cost
                    demon.add_to_spend("torment reduction", demon.torment, cost)
                    demon.save()
                    return True
            return False

        return trait

    def xp_cost(self, trait):
        """Get XP cost for a specific trait."""
        cost = super().xp_cost(trait)
        if cost != 10000:
            return cost

        costs = defaultdict(
            lambda: 10000,
            {
                "faith": 10,
                "house_lore": 5,
                "other_lore": 7,
                "virtue": 2,
                "reduce_torment": 10,
            },
        )
        return costs[trait]

    def freebie_frequencies(self):
        """Freebie spending frequencies for random spending."""
        return {
            "attribute": 15,
            "ability": 8,
            "background": 8,
            "willpower": 1,
            "meritflaw": 15,
            "lore": 25,
            "faith": 15,
            "virtue": 10,
            "temporary_faith": 3,
        }

    def freebie_costs(self):
        """Get freebie costs for various traits."""
        costs = super().freebie_costs()
        costs.update(
            {
                "lore": 7,
                "other_lore": 10,
                "faith": 7,
                "virtue": 2,
                "temporary_faith": 1,
            }
        )
        return costs

    def spend_freebies(self, trait):
        """Spend freebie points on a trait."""
        output = super().spend_freebies(trait)
        if output in [True, False]:
            return output

        # Lores
        if trait in self.get_lores():
            if self.house and trait in [
                f"lore_of_{lore.property_name}" for lore in self.house.lores.all()
            ]:
                cost = self.freebie_cost("lore")
            else:
                cost = self.freebie_cost("other_lore")

            if cost <= self.freebies:
                if self.add_lore(trait):
                    self.freebies -= cost
                    return True
            return False

        # Faith
        if trait == "faith":
            cost = self.freebie_cost("faith")
            if cost <= self.freebies:
                if self.add_faith():
                    self.freebies -= cost
                    return True
            return False

        # Temporary Faith pool
        if trait == "temporary_faith":
            cost = self.freebie_cost("temporary_faith")
            if cost <= self.freebies:
                self.temporary_faith += 1
                self.freebies -= cost
                self.save()
                return True
            return False

        # Virtues
        if trait in ["conviction", "courage", "conscience"]:
            cost = self.freebie_cost("virtue")
            if cost <= self.freebies:
                if add_dot(self, trait, 5):
                    self.freebies -= cost
                    return True
            return False

        return trait

    def freebie_cost(self, trait_type):
        """Get freebie cost for a specific trait type."""
        demon_costs = {
            "lore": 7,
            "other_lore": 10,
            "faith": 7,
            "virtue": 2,
            "temporary_faith": 1,
        }
        if trait_type in demon_costs:
            return demon_costs[trait_type]
        return super().freebie_cost(trait_type)

    def lore_freebies(self, form):
        """Spend freebies on lores."""
        lore = form.cleaned_data["example"]
        lore_property = f"lore_of_{lore.property_name}"

        # Check if this is a house lore
        is_house_lore = False
        if self.house and lore in self.house.lores.all():
            is_house_lore = True

        cost = 7 if is_house_lore else 10

        # Get current rating and increment
        current_rating = getattr(self, lore_property, 0)
        if self.add_lore(lore_property):
            self.freebies -= cost
            trait = lore.name
            value = getattr(self, lore_property)
            return trait, value, cost
        return None

    def faith_freebies(self, form):
        """Spend freebies on Faith."""
        cost = 7
        if self.add_faith():
            self.freebies -= cost
            return "Faith", self.faith, cost
        return None

    def virtue_freebies(self, form):
        """Spend freebies on virtues."""
        cost = 2
        virtue_name = form.cleaned_data["example"].lower()

        # Get current rating and increment
        if add_dot(self, virtue_name, 5):
            self.freebies -= cost
            trait = virtue_name.title()
            value = getattr(self, virtue_name)
            return trait, value, cost
        return None

    def temporary_faith_freebies(self, form):
        """Spend freebies on temporary Faith pool."""
        cost = 1
        self.temporary_faith += 1
        self.freebies -= cost
        self.save()
        return "Temporary Faith", self.temporary_faith, cost


class LoreRating(models.Model):
    """Through table for Demon-Lore relationships with ratings."""

    demon = models.ForeignKey(
        "Demon",
        on_delete=models.SET_NULL,
        null=True,
        related_name="lore_ratings",
    )
    lore = models.ForeignKey(
        Lore,
        on_delete=models.SET_NULL,
        null=True,
        related_name="demon_ratings",
    )
    rating = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(10)]
    )

    class Meta:
        verbose_name = "Demon Lore Rating"
        verbose_name_plural = "Demon Lore Ratings"
        constraints = [
            CheckConstraint(
                check=Q(rating__gte=0, rating__lte=10),
                name="characters_demon_lorerating_rating_range",
                violation_error_message="Lore rating must be between 0 and 10",
            ),
        ]

    def __str__(self):
        demon_name = self.demon.name if self.demon else "No Demon"
        lore_name = str(self.lore) if self.lore else "No Lore"
        return f"{demon_name}: {lore_name}: {self.rating}"
