from django.db import models
from django.urls import reverse

from characters.models.core.human import Human


class HtRHuman(Human):
    """Base mortal with Hunter: the Reckoning-specific abilities"""

    type = "htr_human"
    gameline = "htr"
    freebie_step = 5

    # Standard WoD abilities (Hunters are primarily mortals)
    talents = [
        "alertness",
        "athletics",
        "brawl",
        "dodge",
        "empathy",
        "expression",
        "intimidation",
        "streetwise",
        "subterfuge",
        "awareness",
        "leadership",
    ]

    skills = [
        "crafts",
        "drive",
        "etiquette",
        "firearms",
        "melee",
        "stealth",
        "animal_ken",
        "larceny",
        "performance",
        "repair",
        "survival",
    ]

    knowledges = [
        "academics",
        "computer",
        "investigation",
        "medicine",
        "science",
        "finance",
        "law",
        "occult",
        "politics",
        "technology",
    ]

    primary_abilities = [
        "alertness",
        "athletics",
        "brawl",
        "dodge",
        "empathy",
        "expression",
        "intimidation",
        "streetwise",
        "subterfuge",
        "awareness",
        "leadership",
        "crafts",
        "drive",
        "etiquette",
        "firearms",
        "melee",
        "stealth",
        "animal_ken",
        "larceny",
        "performance",
        "repair",
        "survival",
        "academics",
        "computer",
        "investigation",
        "medicine",
        "science",
        "finance",
        "law",
        "occult",
        "politics",
        "technology",
    ]

    # Hunter-specific backgrounds (no supernatural backgrounds)
    allowed_backgrounds = [
        "allies",
        "contacts",
        "influence",
        "mentor",
        "resources",
        "status_background",
    ]

    # Hunter-specific abilities
    awareness = models.IntegerField(default=0)
    leadership = models.IntegerField(default=0)

    # Additional skills
    animal_ken = models.IntegerField(default=0)
    larceny = models.IntegerField(default=0)
    performance = models.IntegerField(default=0)
    repair = models.IntegerField(default=0)
    survival = models.IntegerField(default=0)

    # Additional knowledges
    finance = models.IntegerField(default=0)
    law = models.IntegerField(default=0)
    occult = models.IntegerField(default=0)
    politics = models.IntegerField(default=0)
    technology = models.IntegerField(default=0)

    # Backgrounds
    allies = models.IntegerField(default=0)
    influence = models.IntegerField(default=0)
    resources = models.IntegerField(default=0)
    status_background = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Human (Hunter)"
        verbose_name_plural = "Humans (Hunter)"

    def get_absolute_url(self):
        return reverse("characters:hunter:htrhuman", kwargs={"pk": self.pk})
