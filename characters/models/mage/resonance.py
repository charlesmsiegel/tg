from core.models import Model
from django.db import models
from django.urls import reverse


class Resonance(Model):
    type = "resonance"
    gameline = "mta"

    correspondence = models.BooleanField(default=False)
    time = models.BooleanField(default=False)
    spirit = models.BooleanField(default=False)
    matter = models.BooleanField(default=False)
    life = models.BooleanField(default=False)
    forces = models.BooleanField(default=False)
    entropy = models.BooleanField(default=False)
    mind = models.BooleanField(default=False)
    prime = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Resonance"
        verbose_name_plural = "Resonances"

    def get_absolute_url(self):
        return reverse("characters:mage:resonance", args=[str(self.id)])

    def get_update_url(self):
        return reverse("characters:mage:update:resonance", kwargs={"pk": self.pk})

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:mage:create:resonance")

    def get_heading(self):
        return "mta_heading"

    def __str__(self):
        return self.name.title()

    def associated_spheres(self):
        all_spheres = {
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
        assoc_spheres = [k.title() for k, v in all_spheres.items() if v]
        return ", ".join(assoc_spheres)
