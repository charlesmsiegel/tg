from django.db import models
from django.urls import reverse

from characters.models.core.human import Human


class MtRHuman(Human):
    type = "mtr_human"
    gameline = "mtr"
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
        "meditation",
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
        "politics",
        "technology",
        "theology",
    ]
    primary_abilities = [
        "alertness",
        "enigmas",
        "law",
        "occult",
        "politics",
        "technology",
        "theology",
        "athletics",
        "animal_ken",
        "larceny",
        "meditation",
        "performance",
        "survival",
        "brawl",
        "awareness",
        "leadership",
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
        "resources",
        "retainers",
        "cult",
        "tomb",
        "rank",
        "remembrance",
        "vessel",
        "artifact",
        "ka",
        "amenti_companion",
    ]

    # Additional talents
    awareness = models.IntegerField(default=0)
    leadership = models.IntegerField(default=0)

    # Additional skills
    animal_ken = models.IntegerField(default=0)
    larceny = models.IntegerField(default=0)
    meditation = models.IntegerField(default=0)
    performance = models.IntegerField(default=0)
    survival = models.IntegerField(default=0)

    # Additional knowledges
    enigmas = models.IntegerField(default=0)
    law = models.IntegerField(default=0)
    occult = models.IntegerField(default=0)
    politics = models.IntegerField(default=0)
    technology = models.IntegerField(default=0)
    theology = models.IntegerField(default=0)

    # Mummy-specific backgrounds
    allies = models.IntegerField(default=0)
    resources = models.IntegerField(default=0)
    retainers = models.IntegerField(default=0)
    cult = models.IntegerField(default=0)
    tomb = models.IntegerField(default=0)
    rank = models.IntegerField(default=0)
    remembrance = models.IntegerField(default=0)
    vessel = models.IntegerField(default=0)
    artifact = models.IntegerField(default=0)
    ka = models.IntegerField(default=0)
    amenti_companion = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Human (Mummy)"
        verbose_name_plural = "Humans (Mummy)"

    def get_absolute_url(self):
        return reverse("characters:mummy:mtrhuman", args=[str(self.id)])

    def get_update_url(self):
        return reverse("characters:mummy:update:mtrhuman", kwargs={"pk": self.pk})

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:mummy:create:mtrhuman")

    def get_heading(self):
        return "mtr_heading"
