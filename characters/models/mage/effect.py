from core.models import Model
from django.db import models
from django.urls import reverse


class Effect(Model):
    type = "effect"
    gameline = "mta"

    correspondence = models.IntegerField(default=0)
    time = models.IntegerField(default=0)
    spirit = models.IntegerField(default=0)
    matter = models.IntegerField(default=0)
    life = models.IntegerField(default=0)
    forces = models.IntegerField(default=0)
    entropy = models.IntegerField(default=0)
    mind = models.IntegerField(default=0)
    prime = models.IntegerField(default=0)
    rote_cost = models.IntegerField(default=0)
    max_sphere = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Effect"
        verbose_name_plural = "Effects"
        ordering = ["max_sphere", "rote_cost", "name"]

    def __str__(self):
        dots = {
            "correspondence": self.correspondence,
            "time": self.time,
            "spirit": self.spirit,
            "matter": self.matter,
            "life": self.life,
            "forces": self.forces,
            "entropy": self.entropy,
            "mind": self.mind,
            "prime": self.prime,
        }
        filtered_dots = [f"{k.title()}: {v}" for k, v in dots.items() if v != 0]
        final_dots = ", ".join(filtered_dots)
        return f"{self.name} ({final_dots})"

    def get_absolute_url(self):
        return reverse("characters:mage:effect", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("characters:mage:update:effect", kwargs={"pk": self.pk})

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:mage:create:effect")

    def get_heading(self):
        return "mta_heading"

    def save(self, *args, **kwargs):
        self.rote_cost = self.cost()
        self.max_sphere = max(
            self.correspondence,
            self.time,
            self.spirit,
            self.matter,
            self.forces,
            self.life,
            self.entropy,
            self.mind,
            self.prime,
        )
        return super().save(*args, **kwargs)

    def spheres(self):
        dots = {
            "correspondence": self.correspondence,
            "time": self.time,
            "spirit": self.spirit,
            "matter": self.matter,
            "life": self.life,
            "forces": self.forces,
            "entropy": self.entropy,
            "mind": self.mind,
            "prime": self.prime,
        }
        filtered_dots = [f"{k.title()} {v * '●'}" for k, v in dots.items() if v != 0]
        final_dots = ", ".join(filtered_dots)
        return final_dots

    def cost(self):
        return (
            self.correspondence
            + self.time
            + self.spirit
            + self.forces
            + self.matter
            + self.life
            + self.prime
            + self.entropy
            + self.mind
        )

    def is_learnable(self, mage):
        for sphere in [
            "correspondence",
            "time",
            "spirit",
            "matter",
            "life",
            "forces",
            "entropy",
            "mind",
            "prime",
        ]:
            if getattr(self, sphere) > getattr(mage, sphere):
                return False
        return True
