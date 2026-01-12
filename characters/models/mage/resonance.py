from django.db import models

from core.models import Model, URLMethodsMixin


class Resonance(URLMethodsMixin, Model):
    type = "resonance"
    gameline = "mta"
    url_namespace = "characters:mage"
    url_name = "resonance"

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
