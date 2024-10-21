from characters.models.core.human import Human
from django.db import models
from django.urls import reverse


class VtMHuman(Human):
    type = "vtm_human"
    gameline = "vtm"

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
        "performance",
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
        "finance",
        "law",
        "occult",
        "politics",
        "technology",
        "athletics",
        "animal_ken",
        "larceny",
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
        "alternate_identity",
        "black_hand_membership",
        "domain",
        "fame",
        "generation",
        "herd",
        "influence",
        "resources",
        "retainers",
        "rituals",
        "status_background",
    ]

    awareness = models.IntegerField(default=0)
    leadership = models.IntegerField(default=0)

    animal_ken = models.IntegerField(default=0)
    larceny = models.IntegerField(default=0)
    performance = models.IntegerField(default=0)
    survival = models.IntegerField(default=0)

    finance = models.IntegerField(default=0)
    law = models.IntegerField(default=0)
    occult = models.IntegerField(default=0)
    politics = models.IntegerField(default=0)
    technology = models.IntegerField(default=0)

    allies = models.IntegerField(default=0)
    alternate_identity = models.IntegerField(default=0)
    black_hand_membership = models.IntegerField(default=0)
    domain = models.IntegerField(default=0)
    fame = models.IntegerField(default=0)
    generation = models.IntegerField(default=0)
    herd = models.IntegerField(default=0)
    influence = models.IntegerField(default=0)
    resources = models.IntegerField(default=0)
    retainers = models.IntegerField(default=0)
    rituals = models.IntegerField(default=0)
    status_background = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Human (Vampire)"
        verbose_name_plural = "Humans (Vampire)"

    def get_update_url(self):
        return reverse("characters:vampire:update:vtm_human", kwargs={"pk": self.pk})

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:vampire:create:vtm_human")

    def get_heading(self):
        return "vtm_heading"
