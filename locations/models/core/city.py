from django.db import models

from characters.models.core import Character

from .location import LocationModel


class City(LocationModel):
    type = "city"
    gameline = "wod"

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
