from django.db import models

from characters.models.core.human import Human


class WtOHuman(Human):
    type = "wto_human"

    gameline = "wto"

    freebie_step = 5

    talents = [
        "alertness",
        "athletics",
        "awareness",
        "brawl",
        "empathy",
        "expression",
        "intimidation",
        "persuasion",
        "streetwise",
        "subterfuge",
    ]
    skills = [
        "crafts",
        "drive",
        "etiquette",
        "firearms",
        "larceny",
        "leadership",
        "meditation",
        "melee",
        "performance",
        "stealth",
    ]
    knowledges = [
        "academics",
        "bureaucracy",
        "computer",
        "enigmas",
        "investigation",
        "medicine",
        "occult",
        "politics",
        "science",
        "technology",
    ]
    primary_abilities = [
        "alertness",
        "leadership",
        "awareness",
        "persuasion",
        "larceny",
        "meditation",
        "performance",
        "bureaucracy",
        "enigmas",
        "occult",
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
        "allies",
        "artifact",
        "eidolon",
        "haunt",
        "legacy",
        "memoriam",
        "notoriety",
        "relic",
        "status_background",
    ]

    awareness = models.IntegerField(default=0)
    persuasion = models.IntegerField(default=0)

    larceny = models.IntegerField(default=0)
    meditation = models.IntegerField(default=0)
    performance = models.IntegerField(default=0)
    leadership = models.IntegerField(default=0)

    bureaucracy = models.IntegerField(default=0)
    enigmas = models.IntegerField(default=0)
    occult = models.IntegerField(default=0)
    politics = models.IntegerField(default=0)
    technology = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Human (Wraith)"
        verbose_name_plural = "Humans (Wraith)"
