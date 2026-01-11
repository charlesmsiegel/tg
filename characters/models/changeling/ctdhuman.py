from django.db import models

from characters.models.core.human import Human


class CtDHuman(Human):
    type = "ctd_human"

    freebie_step = 5

    gameline = "ctd"

    talents = [
        "alertness",
        "athletics",
        "brawl",
        "empathy",
        "expression",
        "intimidation",
        "streetwise",
        "subterfuge",
        "kenning",
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
        "survival",
    ]
    knowledges = [
        "academics",
        "computer",
        "investigation",
        "medicine",
        "science",
        "enigmas",
        "gremayre",
        "law",
        "politics",
        "technology",
    ]
    primary_abilities = [
        "alertness",
        "animal_ken",
        "larceny",
        "performance",
        "survival",
        "kenning",
        "leadership",
        "enigmas",
        "gremayre",
        "law",
        "politics",
        "technology",
        "athletics",
        "brawl",
        "empathy",
        "expression",
        "intimidation",
        "streetwise",
        "subterfuge",
        "crafts",
        "drive",
        "etiquette",
        "firearms",
        "melee",
        "stealth",
        "academics",
        "computer",
        "investigation",
        "medicine",
        "science",
    ]

    allowed_backgrounds = [
        "contacts",
        "mentor",
        "chimera",
        "dreamers",
        "holdings",
        "remembrance",
        "resources",
        "retinue",
        "title",
        "treasure",
    ]

    kenning = models.IntegerField(default=0)
    leadership = models.IntegerField(default=0)

    animal_ken = models.IntegerField(default=0)
    larceny = models.IntegerField(default=0)
    performance = models.IntegerField(default=0)
    survival = models.IntegerField(default=0)

    enigmas = models.IntegerField(default=0)
    gremayre = models.IntegerField(default=0)
    law = models.IntegerField(default=0)
    politics = models.IntegerField(default=0)
    technology = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Human (Changeling)"
        verbose_name_plural = "Humans (Changeling)"
