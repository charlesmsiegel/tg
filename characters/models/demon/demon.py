from collections import defaultdict

from characters.models.demon.dtf_human import DtFHuman
from characters.models.demon.faction import DemonFaction
from characters.models.demon.house import House
from characters.models.demon.lore import Lore
from characters.models.demon.visage import Visage
from core.utils import add_dot
from django.db import models


class Demon(DtFHuman):
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
        "status_background",
    ]

    # House and Faction
    house = models.ForeignKey(
        House,
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

    # Visage (apocalyptic form)
    visage = models.ForeignKey(
        Visage,
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

    # Lores (23 different lores, 0-5 rating each)
    lore_of_awakening = models.IntegerField(default=0)
    lore_of_the_beast = models.IntegerField(default=0)
    lore_of_the_celestials = models.IntegerField(default=0)
    lore_of_death = models.IntegerField(default=0)
    lore_of_the_earth = models.IntegerField(default=0)
    lore_of_flame = models.IntegerField(default=0)
    lore_of_the_firmament = models.IntegerField(default=0)
    lore_of_the_flesh = models.IntegerField(default=0)
    lore_of_the_forge = models.IntegerField(default=0)
    lore_of_the_fundament = models.IntegerField(default=0)
    lore_of_humanity = models.IntegerField(default=0)
    lore_of_light = models.IntegerField(default=0)
    lore_of_longing = models.IntegerField(default=0)
    lore_of_paths = models.IntegerField(default=0)
    lore_of_patterns = models.IntegerField(default=0)
    lore_of_portals = models.IntegerField(default=0)
    lore_of_radiance = models.IntegerField(default=0)
    lore_of_the_realms = models.IntegerField(default=0)
    lore_of_the_spirit = models.IntegerField(default=0)
    lore_of_storms = models.IntegerField(default=0)
    lore_of_transfiguration = models.IntegerField(default=0)
    lore_of_the_wild = models.IntegerField(default=0)
    lore_of_the_winds = models.IntegerField(default=0)

    # Apocalyptic form
    apocalyptic_form_abilities = models.JSONField(default=list)  # 8 abilities

    # Host information
    host_name = models.CharField(max_length=200, default="")
    days_until_consumption = models.IntegerField(default=30)

    # Celestial names
    celestial_name = models.CharField(max_length=200, default="")
    true_name = models.CharField(max_length=200, default="")

    # History
    age_of_fall = models.IntegerField(default=0)
    abyss_duration = models.TextField(default="")  # Time in the Abyss

    background_points = 5

    class Meta:
        verbose_name = "Demon"
        verbose_name_plural = "Demons"
        ordering = ["name"]

    def get_lores(self):
        """Return a dictionary of all lore ratings."""
        return {
            "lore_of_awakening": self.lore_of_awakening,
            "lore_of_the_beast": self.lore_of_the_beast,
            "lore_of_the_celestials": self.lore_of_the_celestials,
            "lore_of_death": self.lore_of_death,
            "lore_of_the_earth": self.lore_of_the_earth,
            "lore_of_flame": self.lore_of_flame,
            "lore_of_the_firmament": self.lore_of_the_firmament,
            "lore_of_the_flesh": self.lore_of_the_flesh,
            "lore_of_the_forge": self.lore_of_the_forge,
            "lore_of_the_fundament": self.lore_of_the_fundament,
            "lore_of_humanity": self.lore_of_humanity,
            "lore_of_light": self.lore_of_light,
            "lore_of_longing": self.lore_of_longing,
            "lore_of_paths": self.lore_of_paths,
            "lore_of_patterns": self.lore_of_patterns,
            "lore_of_portals": self.lore_of_portals,
            "lore_of_radiance": self.lore_of_radiance,
            "lore_of_the_realms": self.lore_of_the_realms,
            "lore_of_the_spirit": self.lore_of_the_spirit,
            "lore_of_storms": self.lore_of_storms,
            "lore_of_transfiguration": self.lore_of_transfiguration,
            "lore_of_the_wild": self.lore_of_the_wild,
            "lore_of_the_winds": self.lore_of_the_winds,
        }

    def total_lores(self):
        """Return total dots spent in lores."""
        return sum(self.get_lores().values())

    def add_lore(self, lore_name, maximum=5):
        """Add a dot to a specific lore."""
        return add_dot(self, lore_name, maximum)

    def filter_lores(self, minimum=0, maximum=5):
        """Return lores within a specific rating range."""
        return {k: v for k, v in self.get_lores().items() if minimum <= v <= maximum}

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

    def has_apocalyptic_form(self):
        """Check if apocalyptic form has 8 abilities."""
        return len(self.apocalyptic_form_abilities) == 8

    def has_demon_history(self):
        """Check if demon has celestial name and history."""
        return (
            self.celestial_name != ""
            and self.true_name != ""
            and self.age_of_fall != 0
        )

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

        # Virtues
        if trait in ["conviction", "courage", "conscience"]:
            cost = self.xp_cost("virtue") * getattr(self, trait)
            if cost <= self.xp:
                if add_dot(self, trait, 5):
                    self.xp -= cost
                    self.add_to_spend(trait, getattr(self, trait), cost)
                    return True
            return False

        # Torment reduction
        if trait == "reduce_torment":
            cost = self.xp_cost("reduce_torment")
            if cost <= self.xp:
                if self.reduce_torment():
                    self.xp -= cost
                    self.add_to_spend("torment reduction", self.torment, cost)
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


class LoreRating(models.Model):
    """Through table for Demon-Lore relationships with ratings."""

    demon = models.ForeignKey("Demon", on_delete=models.CASCADE, null=True)
    lore = models.ForeignKey(Lore, on_delete=models.CASCADE, null=True)
    rating = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Demon Lore Rating"
        verbose_name_plural = "Demon Lore Ratings"

    def __str__(self):
        demon_name = self.demon.name if self.demon else "No Demon"
        lore_name = str(self.lore) if self.lore else "No Lore"
        return f"{demon_name}: {lore_name}: {self.rating}"
