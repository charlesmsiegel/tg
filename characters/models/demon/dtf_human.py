from characters.models.core.human import Human
from django.db import models


class DtFHuman(Human):
    """Base class for Demon: The Fallen characters."""

    type = "dtf_human"

    freebie_step = 5

    allowed_backgrounds = [
        "contacts",
        "mentor",
        "allies",
        "alternate_identity",
        "cult",
        "eminence",
        "fame",
        "followers",
        "influence",
        "legacy",
        "pacts",
        "paragon",
        "resources",
        "retainers",
        "status_background",
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
        "search",
        "seduction",
        "style",
    ]

    skills = [
        "crafts",
        "drive",
        "etiquette",
        "firearms",
        "melee",
        "stealth",
        "larceny",
        "performance",
        "survival",
        "technology",
        "animal_ken",
        "demolitions",
        "disguise",
        "torture",
        "meditation",
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
        "area_knowledge",
        "belief_systems",
        "bureaucracy",
        "cryptography",
        "history_knowledge",
        "linguistics",
        "psychology",
        "theology",
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
        "crafts",
        "drive",
        "etiquette",
        "firearms",
        "melee",
        "stealth",
        "larceny",
        "performance",
        "survival",
        "technology",
        "academics",
        "computer",
        "investigation",
        "medicine",
        "science",
        "finance",
        "law",
        "occult",
        "politics",
    ]

    # Demon-specific ability fields
    awareness = models.IntegerField(default=0)
    intuition = models.IntegerField(default=0)
    leadership = models.IntegerField(default=0)
    search = models.IntegerField(default=0)
    seduction = models.IntegerField(default=0)
    style = models.IntegerField(default=0)

    larceny = models.IntegerField(default=0)
    performance = models.IntegerField(default=0)
    survival = models.IntegerField(default=0)
    technology = models.IntegerField(default=0)
    animal_ken = models.IntegerField(default=0)
    demolitions = models.IntegerField(default=0)
    disguise = models.IntegerField(default=0)
    torture = models.IntegerField(default=0)
    meditation = models.IntegerField(default=0)

    finance = models.IntegerField(default=0)
    law = models.IntegerField(default=0)
    occult = models.IntegerField(default=0)
    politics = models.IntegerField(default=0)
    area_knowledge = models.IntegerField(default=0)
    belief_systems = models.IntegerField(default=0)
    bureaucracy = models.IntegerField(default=0)
    cryptography = models.IntegerField(default=0)
    history_knowledge = models.IntegerField(default=0)
    linguistics = models.IntegerField(default=0)
    psychology = models.IntegerField(default=0)
    theology = models.IntegerField(default=0)

    background_points = 5

    class Meta:
        verbose_name = "Human (Demon)"
        verbose_name_plural = "Humans (Demon)"
        ordering = ["name"]
