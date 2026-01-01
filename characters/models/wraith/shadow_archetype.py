from core.models import Model
from django.db import models
from django.urls import reverse


class ShadowArchetype(Model):
    type = "shadow_archetype"
    gameline = "wto"

    point_cost = models.IntegerField(default=1)
    core_function = models.TextField(default="", blank=True)
    modus_operandi = models.TextField(default="", blank=True)
    dominance_behavior = models.TextField(default="", blank=True)
    effect_on_psyche = models.TextField(default="", blank=True)
    strengths = models.TextField(default="", blank=True)
    weaknesses = models.TextField(default="", blank=True)

    class Meta:
        verbose_name = "Shadow Archetype"
        verbose_name_plural = "Shadow Archetypes"

    def get_absolute_url(self):
        return reverse("characters:wraith:shadow_archetype", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("characters:wraith:update:shadow_archetype", kwargs={"pk": self.pk})

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:wraith:create:shadow_archetype")

    def get_heading(self):
        return "wto_heading"
