from django.db import models
from django.urls import reverse

from characters.costs import get_freebie_cost
from characters.models.demon.dtf_human import DtFHuman
from core.utils import add_dot


class Thrall(DtFHuman):
    """Mortal servant bound to a demon through a pact."""

    type = "thrall"
    gameline = "dtf"

    # Faith Potential (1-5 dots, measures spiritual/emotional capacity)
    faith_potential = models.IntegerField(default=1)

    # Daily Faith offered to demon master
    daily_faith_offered = models.IntegerField(default=1)

    # Master demon (primary, for convenience - can have multiple via pacts)
    master = models.ForeignKey(
        "Demon",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="primary_thralls",
    )

    # Enhancements granted by pact
    enhancements = models.JSONField(default=list, blank=True)  # list is callable - safe

    # Virtues (same as demons)
    conviction = models.IntegerField(default=1)
    courage = models.IntegerField(default=1)
    conscience = models.IntegerField(default=1)

    background_points = 5

    class Meta:
        verbose_name = "Thrall"
        verbose_name_plural = "Thralls"
        ordering = ["name"]

    def get_absolute_url(self):
        return reverse("characters:demon:thrall", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("characters:demon:update:thrall", kwargs={"pk": self.pk})

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:demon:create:thrall")

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

    def get_pacts(self):
        """Get all pacts this thrall has with demons."""
        from characters.models.demon.pact import Pact

        return Pact.objects.filter(thrall=self).select_related("demon", "thrall")

    def get_active_pacts(self):
        """Get all active pacts."""
        return self.get_pacts().filter(active=True)

    def total_pacts(self):
        """Get total number of active pacts."""
        return self.get_active_pacts().count()

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

    def spend_freebies(self, trait):
        """Spend freebie points on a trait."""
        output = super().spend_freebies(trait)
        if output in [True, False]:
            return output

        # Faith Potential
        if trait == "faith_potential":
            cost = get_freebie_cost("faith_potential")
            if cost <= self.freebies:
                if self.add_faith_potential():
                    self.freebies -= cost
                    self.calculate_daily_faith()
                    return True
            return False

        # Virtues
        if trait in ["conviction", "courage", "conscience"]:
            cost = get_freebie_cost("virtue")
            if cost <= self.freebies:
                if add_dot(self, trait, 5):
                    self.freebies -= cost
                    return True
            return False

        return trait

    def faith_potential_freebies(self, form):
        """Spend freebies on Faith Potential."""
        cost = 7
        if self.add_faith_potential():
            self.freebies -= cost
            self.calculate_daily_faith()
            return "Faith Potential", self.faith_potential, cost
        return None

    def virtue_freebies(self, form):
        """Spend freebies on virtues."""
        cost = 2
        virtue_name = form.cleaned_data["example"].lower()

        if add_dot(self, virtue_name, 5):
            self.freebies -= cost
            trait = virtue_name.title()
            value = getattr(self, virtue_name)
            return trait, value, cost
        return None
