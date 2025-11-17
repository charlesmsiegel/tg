from characters.models.demon.dtf_human import DtFHuman
from core.utils import add_dot
from django.db import models


class Thrall(DtFHuman):
    """Mortal servant bound to a demon through a pact."""

    type = "thrall"

    freebie_step = 6

    # Faith Potential (1-5 dots, measures spiritual/emotional capacity)
    faith_potential = models.IntegerField(default=1)

    # Daily Faith offered to demon master
    daily_faith_offered = models.IntegerField(default=1)

    # Master demon
    master = models.ForeignKey(
        "Demon",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="thralls",
    )

    # Enhancements granted by pact
    enhancements = models.JSONField(default=list)

    # Virtues (same as demons)
    conviction = models.IntegerField(default=1)
    courage = models.IntegerField(default=1)
    conscience = models.IntegerField(default=1)

    background_points = 5

    class Meta:
        verbose_name = "Thrall"
        verbose_name_plural = "Thralls"
        ordering = ["name"]

    def add_faith_potential(self):
        """Add a dot of Faith Potential."""
        return add_dot(self, "faith_potential", 5)

    def has_faith_potential(self):
        """Check if thrall has at least 1 Faith Potential."""
        return self.faith_potential >= 1

    def calculate_daily_faith(self):
        """Calculate how much Faith the thrall can offer daily."""
        # Up to half Faith Potential (rounded up) = daily Faith
        self.daily_faith_offered = (self.faith_potential + 1) // 2
        self.save()
        return self.daily_faith_offered

    def has_virtues(self):
        """Check if virtues are properly set."""
        return (
            self.conviction >= 1
            and self.courage >= 1
            and self.conscience >= 1
            and (self.conviction + self.courage + self.conscience) == 6
        )

    def add_enhancement(self, enhancement):
        """Add an enhancement to the thrall."""
        if enhancement not in self.enhancements:
            self.enhancements.append(enhancement)
            self.save()
            return True
        return False

    def remove_enhancement(self, enhancement):
        """Remove an enhancement from the thrall."""
        if enhancement in self.enhancements:
            self.enhancements.remove(enhancement)
            self.save()
            return True
        return False

    def xp_frequencies(self):
        """XP spending frequencies for random spending."""
        return {
            "attribute": 20,
            "ability": 25,
            "background": 15,
            "willpower": 5,
            "faith_potential": 30,
            "virtue": 5,
        }

    def spend_xp(self, trait):
        """Spend XP on a trait."""
        output = super().spend_xp(trait)
        if output in [True, False]:
            return output

        # Faith Potential
        if trait == "faith_potential":
            cost = self.xp_cost("faith_potential") * self.faith_potential
            if cost <= self.xp:
                if self.add_faith_potential():
                    self.xp -= cost
                    self.calculate_daily_faith()
                    self.add_to_spend(trait, self.faith_potential, cost)
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

        return trait

    def xp_cost(self, trait):
        """Get XP cost for a specific trait."""
        cost = super().xp_cost(trait)
        if cost != 10000:
            return cost

        from collections import defaultdict

        costs = defaultdict(
            lambda: 10000,
            {
                "faith_potential": 10,
                "virtue": 2,
            },
        )
        return costs[trait]

    def freebie_frequencies(self):
        """Freebie spending frequencies for random spending."""
        return {
            "attribute": 20,
            "ability": 15,
            "background": 10,
            "willpower": 5,
            "meritflaw": 20,
            "faith_potential": 25,
            "virtue": 5,
        }

    def freebie_costs(self):
        """Get freebie costs for various traits."""
        costs = super().freebie_costs()
        costs.update(
            {
                "faith_potential": 7,
                "virtue": 2,
            }
        )
        return costs

    def spend_freebies(self, trait):
        """Spend freebie points on a trait."""
        output = super().spend_freebies(trait)
        if output in [True, False]:
            return output

        # Faith Potential
        if trait == "faith_potential":
            cost = self.freebie_cost("faith_potential")
            if cost <= self.freebies:
                if self.add_faith_potential():
                    self.freebies -= cost
                    self.calculate_daily_faith()
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
        thrall_costs = {
            "faith_potential": 7,
            "virtue": 2,
        }
        if trait_type in thrall_costs:
            return thrall_costs[trait_type]
        return super().freebie_cost(trait_type)
