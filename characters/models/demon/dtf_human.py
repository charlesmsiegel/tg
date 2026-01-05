from characters.models.core.human import Human
from django.db import models
from django.urls import reverse


class DtFHuman(Human):
    """Base class for Demon: The Fallen characters."""

    type = "dtf_human"

    freebie_step = 5

    allowed_backgrounds = [
        "contacts",
        "mentor",
        "allies",
        "eminence",
        "fame",
        "followers",
        "influence",
        "legacy",
        "pacts",
        "paragon",
        "resources",
    ]

    gameline = "dtf"

    # Demon-specific abilities
    talents = [
        "alertness",
        "athletics",
        "brawl",
        "empathy",
        "expression",
        "intimidation",
        "streetwise",
        "subterfuge",
        "awareness",
        "intuition",
        "leadership",
        "seduction",
    ]

    skills = [
        "crafts",
        "drive",
        "etiquette",
        "firearms",
        "melee",
        "stealth",
        "performance",
        "security",
        "survival",
        "technology",
        "animal_ken",
        "demolitions",
    ]

    knowledges = [
        "academics",
        "computer",
        "finance",
        "investigation",
        "law",
        "enigmas",
        "medicine",
        "occult",
        "politics",
        "religion",
        "research",
        "science",
    ]

    primary_abilities = [
        "alertness",
        "athletics",
        "brawl",
        "empathy",
        "expression",
        "intimidation",
        "streetwise",
        "subterfuge",
        "awareness",
        "intuition",
        "leadership",
        "seduction",
        "crafts",
        "drive",
        "etiquette",
        "firearms",
        "melee",
        "stealth",
        "performance",
        "security",
        "survival",
        "technology",
        "animal_ken",
        "demolitions",
        "academics",
        "computer",
        "finance",
        "investigation",
        "law",
        "enigmas",
        "medicine",
        "occult",
        "politics",
        "religion",
        "research",
        "science",
    ]

    awareness = models.IntegerField(default=0)
    intuition = models.IntegerField(default=0)
    leadership = models.IntegerField(default=0)
    seduction = models.IntegerField(default=0)
    performance = models.IntegerField(default=0)
    security = models.IntegerField(default=0)
    survival = models.IntegerField(default=0)
    technology = models.IntegerField(default=0)
    animal_ken = models.IntegerField(default=0)
    demolitions = models.IntegerField(default=0)
    finance = models.IntegerField(default=0)
    law = models.IntegerField(default=0)
    enigmas = models.IntegerField(default=0)
    occult = models.IntegerField(default=0)
    politics = models.IntegerField(default=0)
    religion = models.IntegerField(default=0)
    research = models.IntegerField(default=0)

    background_points = 5

    class Meta:
        verbose_name = "Human (Demon)"
        verbose_name_plural = "Humans (Demon)"
        ordering = ["name"]

    def get_absolute_url(self):
        return reverse("characters:demon:dtfhuman", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("characters:demon:update:dtfhuman", kwargs={"pk": self.pk})

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:demon:create:dtfhuman")
