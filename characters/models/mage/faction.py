from characters.models.mage.sphere import Sphere
from core.models import Language, Model, ModelManager, ModelQuerySet
from django.db import models
from django.urls import reverse
from items.models.core.material import Material
from items.models.core.medium import Medium

from .focus import Paradigm, Practice


class MageFactionQuerySet(ModelQuerySet):
    """Custom queryset for MageFaction with chainable query patterns."""

    def top_level(self):
        """Top-level factions (no parent)."""
        return self.filter(parent=None)


MageFactionManager = ModelManager.from_queryset(MageFactionQuerySet)


class MageFaction(Model):
    type = "mage_faction"
    gameline = "mta"

    languages = models.ManyToManyField(Language, blank=True)
    affinities = models.ManyToManyField(Sphere, blank=True)
    paradigms = models.ManyToManyField(Paradigm, blank=True)
    practices = models.ManyToManyField(Practice, blank=True)
    media = models.ManyToManyField(Medium, blank=True)
    materials = models.ManyToManyField(Material, blank=True)
    founded = models.IntegerField(default=-5000)
    ended = models.IntegerField(default=5000)
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True)

    objects = MageFactionManager()

    class Meta:
        verbose_name = "Mage Faction"
        verbose_name_plural = "Mage Factions"

    def get_absolute_url(self):
        return reverse("characters:mage:mage_faction", args=[str(self.id)])

    def get_update_url(self):
        return reverse("characters:mage:update:mage_faction", kwargs={"pk": self.pk})

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:mage:create:mage_faction")

    def get_heading(self):
        return "mta_heading"

    def get_all_paradigms(self):
        factions = [self]
        while factions[-1].parent is not None:
            factions.append(factions[-1].parent)
        paradigms = Paradigm.objects.none()
        for faction in factions:
            paradigms |= faction.paradigms.all()
        return paradigms.distinct()

    def get_all_practices(self):
        factions = [self]
        while factions[-1].parent is not None:
            factions.append(factions[-1].parent)
        practices = Practice.objects.none()
        for faction in factions:
            practices |= faction.practices.all()
        return Practice.objects.filter(pk__in=practices.distinct())
