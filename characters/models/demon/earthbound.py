from collections import defaultdict

from characters.models.core.lore_block import LoreBlock
from characters.models.demon.dtf_human import DtFHuman
from characters.models.demon.house import House
from characters.models.demon.lore import Lore
from core.utils import add_dot
from django.db import models


class Earthbound(LoreBlock, DtFHuman):
    """Ancient demon anchored to a physical reliquary."""

    type = "earthbound"

    freebie_step = 8

    # Always at Torment 10
    torment = models.IntegerField(default=10)

    # High starting Faith
    faith = models.IntegerField(default=4)
    temporary_faith = models.IntegerField(default=10)

    # House
    house = models.ForeignKey(
        House,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="earthbound",
    )

    # Urges instead of Virtues
    urge_flesh = models.IntegerField(default=1)  # Physical sensation/performance
    urge_thought = models.IntegerField(default=1)  # Intellectual stimulation
    urge_emotion = models.IntegerField(default=1)  # Emotional experience/manipulation

    # Lores inherited from LoreBlock (can only use destructive versions)

    # Earthbound-exclusive backgrounds
    codex = models.IntegerField(default=0)  # Knowledge of True Names (0-5)
    hoard = models.IntegerField(default=0)  # Reliquary Faith storage (0-5)
    mastery = models.IntegerField(default=0)  # Evocation enhancement (0-5)
    thralls = models.IntegerField(default=0)  # Powerful servants (0-5)
    cult = models.IntegerField(default=0)  # Ritual frequency (0-5)
    worship = models.IntegerField(default=0)  # Faith gain per ritual (0-5)

    # Reliquary information
    reliquary_type = models.CharField(
        max_length=100,
        default="improvised",
        choices=[
            ("perfect", "Perfect Reliquary"),
            ("improvised", "Improvised Reliquary"),
            ("location", "Location Reliquary"),
        ],
    )
    reliquary_description = models.TextField(default="")

    # Celestial names
    celestial_name = models.CharField(max_length=200, default="")
    true_name = models.CharField(max_length=200, default="")

    # History
    age_of_summoning = models.IntegerField(default=0)
    summoning_history = models.TextField(default="")

    background_points = 10  # Earthbound get 10 background dots

    class Meta:
        verbose_name = "Earthbound"
        verbose_name_plural = "Earthbound"
        ordering = ["name"]

    # Lore methods (get_lores, total_lores, add_lore, filter_lores) inherited from LoreBlock

    def has_lores(self):
        """Check if earthbound has spent starting 10 dots in lores."""
        return self.total_lores() >= 10

    def has_house(self):
        """Check if earthbound has selected a house."""
        return self.house is not None

    def set_house(self, house):
        """Set the earthbound's house."""
        self.house = house
        self.save()
        return True

    def add_faith(self):
        """Add a dot of permanent Faith."""
        return add_dot(self, "faith", 10)

    def has_urges(self):
        """Check if urges are properly set."""
        return (
            self.urge_flesh >= 1
            and self.urge_thought >= 1
            and self.urge_emotion >= 1
            and (self.urge_flesh + self.urge_thought + self.urge_emotion) >= 6
        )

    def calculate_willpower(self):
        """Calculate Willpower from two highest Urges."""
        urges = [self.urge_flesh, self.urge_thought, self.urge_emotion]
        urges.sort(reverse=True)
        self.willpower = urges[0] + urges[1]
        self.save()
        return self.willpower

    def has_reliquary(self):
        """Check if reliquary is defined."""
        return self.reliquary_description != ""

    def get_reliquary_capacity(self):
        """Calculate maximum Faith storage in reliquary."""
        base = 10
        if self.reliquary_type == "improvised":
            # Max hoard 3 for improvised
            hoard_bonus = min(self.hoard, 3) * 5
        else:
            hoard_bonus = self.hoard * 5
        return base + hoard_bonus

    def xp_frequencies(self):
        """XP spending frequencies for random spending."""
        return {
            "attribute": 15,
            "ability": 18,
            "background": 10,
            "willpower": 1,
            "lore": 40,
            "faith": 12,
            "urge": 4,
        }

    def spend_xp(self, trait):
        """Spend XP on a trait."""
        output = super().spend_xp(trait)
        if output in [True, False]:
            return output

        # Faith
        if trait == "faith":
            cost = self.xp_cost("faith") * self.faith
            if cost <= self.xp:
                if self.add_faith():
                    self.xp -= cost
                    self.add_to_spend(trait, self.faith, cost)
                    return True
            return False

        # Lores
        if trait in self.get_lores():
            current_rating = getattr(self, trait)
            if self.house and trait in [
                f"lore_of_{lore.property_name}" for lore in self.house.lores.all()
            ]:
                cost = self.xp_cost("house_lore") * (current_rating + 1)
            else:
                cost = self.xp_cost("other_lore") * (current_rating + 1)

            if cost <= self.xp:
                if self.add_lore(trait):
                    self.xp -= cost
                    self.add_to_spend(trait, getattr(self, trait), cost)
                    return True
            return False

        # Urges
        if trait in ["urge_flesh", "urge_thought", "urge_emotion"]:
            cost = self.xp_cost("urge") * getattr(self, trait)
            if cost <= self.xp:
                if add_dot(self, trait, 5):
                    self.xp -= cost
                    self.calculate_willpower()
                    self.add_to_spend(trait, getattr(self, trait), cost)
                    return True
            return False

        # Backgrounds
        if trait in ["codex", "hoard", "mastery", "thralls", "cult", "worship"]:
            cost = self.xp_cost("background") * getattr(self, trait)
            if cost <= self.xp:
                if add_dot(self, trait, 5):
                    self.xp -= cost
                    self.add_to_spend(trait, getattr(self, trait), cost)
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
                "attribute": 5,
                "ability": 3,
                "background": 4,
                "faith": 6,
                "house_lore": 4,
                "other_lore": 8,
                "urge": 2,
            },
        )
        return costs[trait]

    def freebie_frequencies(self):
        """Freebie spending frequencies for random spending."""
        return {
            "attribute": 15,
            "ability": 10,
            "background": 15,
            "willpower": 1,
            "lore": 35,
            "faith": 15,
            "urge": 9,
        }

    def freebie_costs(self):
        """Get freebie costs for various traits."""
        costs = super().freebie_costs()
        costs.update(
            {
                "attribute": 6,
                "ability": 2,
                "background": 1,
                "lore": 5,
                "other_lore": 8,
                "faith": 5,
                "urge": 3,
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

        # Urges
        if trait in ["urge_flesh", "urge_thought", "urge_emotion"]:
            cost = self.freebie_cost("urge")
            if cost <= self.freebies:
                if add_dot(self, trait, 5):
                    self.freebies -= cost
                    self.calculate_willpower()
                    return True
            return False

        # Backgrounds
        if trait in ["codex", "hoard", "mastery", "thralls", "cult", "worship"]:
            cost = self.freebie_cost("background")
            if cost <= self.freebies:
                if add_dot(self, trait, 5):
                    self.freebies -= cost
                    return True
            return False

        return trait

    def freebie_cost(self, trait_type):
        """Get freebie cost for a specific trait type."""
        earthbound_costs = {
            "attribute": 6,
            "ability": 2,
            "background": 1,
            "lore": 5,
            "other_lore": 8,
            "faith": 5,
            "urge": 3,
        }
        if trait_type in earthbound_costs:
            return earthbound_costs[trait_type]
        return super().freebie_cost(trait_type)
