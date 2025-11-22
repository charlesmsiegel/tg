from core.models import Model
from django.db import models
from django.urls import reverse


class ShadowArchetype(Model):
    type = "shadow_archetype"

    point_cost = models.IntegerField(default=1)
    core_function = models.TextField(default="")
    modus_operandi = models.TextField(default="")
    dominance_behavior = models.TextField(default="")
    effect_on_psyche = models.TextField(default="")
    strengths = models.TextField(default="")
    weaknesses = models.TextField(default="")

    class Meta:
        verbose_name = "Shadow Archetype"
        verbose_name_plural = "Shadow Archetypes"

    def get_absolute_url(self):
        return reverse("characters:wraith:shadow_archetype", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse(
            "characters:wraith:update:shadow_archetype", kwargs={"pk": self.pk}
        )

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:wraith:create:shadow_archetype")

    def get_heading(self):
        return "wto_heading"
