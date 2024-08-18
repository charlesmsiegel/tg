from characters.models.core import Character
from django.db import models
from django.urls import reverse

from .location import LocationModel


# Create your models here.
class City(LocationModel):
    type = "city"

    population = models.IntegerField(default=0)
    characters = models.ManyToManyField(Character, blank=True)
    mood = models.TextField(blank=True, null=True)
    theme = models.TextField(blank=True, null=True)
    media = models.TextField(blank=True, null=True)
    politicians = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "City"
        verbose_name_plural = "Cities"

    def add_character(self, character):
        self.characters.add(character)
        self.save()

    def get_update_url(self):
        return reverse("locations:update:city", args=[str(self.id)])

    @classmethod
    def get_creation_url(cls):
        return reverse("locations:create:city")

    def get_heading(self):
        return "wod_heading"
