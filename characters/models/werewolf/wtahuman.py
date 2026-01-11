from django.db import models

from characters.models.core.human import Human


class WtAHuman(Human):
    type = "wta_human"

    gameline = "wta"

    freebie_step = 5

    talents = [
        "alertness",
        "athletics",
        "brawl",
        "empathy",
        "expression",
        "intimidation",
        "streetwise",
        "subterfuge",
        "leadership",
        "primal_urge",
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
        "law",
        "occult",
        "rituals",
        "technology",
    ]
    primary_abilities = [
        "alertness",
        "leadership",
        "primal_urge",
        "animal_ken",
        "larceny",
        "performance",
        "survival",
        "enigmas",
        "law",
        "occult",
        "rituals",
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
        "ancestors",
        "fate",
        "fetish",
        "kinfolk_rating",
        "pure_breed",
        "resources",
        "rites",
        "spirit_heritage",
        "totem",
    ]

    leadership = models.IntegerField(default=0)
    primal_urge = models.IntegerField(default=0)

    animal_ken = models.IntegerField(default=0)
    larceny = models.IntegerField(default=0)
    performance = models.IntegerField(default=0)
    survival = models.IntegerField(default=0)

    enigmas = models.IntegerField(default=0)
    law = models.IntegerField(default=0)
    occult = models.IntegerField(default=0)
    rituals = models.IntegerField(default=0)
    technology = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Human (Werewolf)"
        verbose_name_plural = "Humans (Werewolf)"
