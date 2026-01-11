from django.db import models
from django.urls import reverse

from items.models.core import ItemModel


class WraithArtifact(ItemModel):
    type = "artifact"
    gameline = "wto"

    level = models.IntegerField(default=1)
    background_cost = models.IntegerField(default=0)

    ARTIFACT_TYPE_CHOICES = [
        ("soulforged", "Soulforged"),
        ("skin", "Skin Artifact"),
        ("spectre", "Spectre Artifact"),
        ("other", "Other"),
    ]

    artifact_type = models.CharField(
        max_length=20, choices=ARTIFACT_TYPE_CHOICES, default="soulforged"
    )

    # Soulforging materials
    MATERIAL_CHOICES = [
        ("soulsteel", "Soulsteel"),
        ("stygian_steel", "Stygian Steel"),
        ("necropolis_steel", "Necropolis Steel"),
        ("ash_iron", "Ash-Iron"),
        ("labyrinthine_adamas", "Labyrinthine Adamas"),
    ]

    material = models.CharField(max_length=30, choices=MATERIAL_CHOICES, default="soulsteel")

    # Properties
    corpus = models.IntegerField(default=0)
    pathos_cost = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Artifact"
        verbose_name_plural = "Artifacts"

    def get_absolute_url(self):
        return reverse("items:wraith:artifact", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("items:wraith:update:artifact", args=[str(self.id)])

    @classmethod
    def get_creation_url(cls):
        return reverse("items:wraith:create:artifact")

    def set_level(self, level):
        self.level = level
        self.background_cost = level
        return True

    def has_level(self):
        return self.level != 0

    def save(self, *args, **kwargs):
        self.background_cost = self.level
        return super().save(*args, **kwargs)
