from django.db import models

from characters.models.core.character import Character
from characters.models.core.human import Human
from items.models.mage.wonder import Wonder


class MtAHuman(Human):
    type = "mta_human"

    freebie_step = 5

    allowed_backgrounds = [
        "contacts",
        "mentor",
        "allies",
        "alternate_identity",
        "arcane",
        "backup",
        "blessing",
        "certification",
        "chantry",
        "cult",
        "demesne",
        "destiny",
        "dream",
        "enhancement",
        "fame",
        "familiar",
        "influence",
        "legend",
        "library",
        "node",
        "past_lives",
        "patron",
        "rank",
        "requisitions",
        "resources",
        "retainers",
        "sanctum",
        "secret_weapons",
        "spies",
        "status_background",
        "totem",
        "wonder",
    ]

    gameline = "mta"

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
        "art",
        "leadership",
        "animal_kinship",
        "blatancy",
        "carousing",
        "flying",
        "high_ritual",
        "lucid_dreaming",
        "search",
        "seduction",
        "cooking",
        "diplomacy",
        "instruction",
        "intrigue",
        "intuition",
        "mimicry",
        "negotiation",
        "newspeak",
        "scan",
        "scrounging",
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
        "meditation",
        "research",
        "survival",
        "technology",
        "acrobatics",
        "archery",
        "biotech",
        "energy_weapons",
        "jetpack",
        "riding",
        "torture",
        "blind_fighting",
        "climbing",
        "disguise",
        "elusion",
        "escapology",
        "fast_draw",
        "fast_talk",
        "fencing",
        "fortune_telling",
        "gambling",
        "gunsmith",
        "heavy_weapons",
        "hunting",
        "hypnotism",
        "jury_rigging",
        "microgravity_operations",
        "misdirection",
        "networking",
        "pilot",
        "psychology",
        "security",
        "speed_reading",
        "swimming",
    ]
    knowledges = [
        "academics",
        "computer",
        "investigation",
        "medicine",
        "science",
        "cosmology",
        "enigmas",
        "finance",
        "law",
        "occult",
        "politics",
        "area_knowledge",
        "belief_systems",
        "cryptography",
        "demolitions",
        "lore",
        "media",
        "pharmacopeia",
        "conspiracy_theory",
        "chantry_politics",
        "covert_culture",
        "cultural_savvy",
        "helmsman",
        "history_knowledge",
        "power_brokering",
        "propaganda",
        "theology",
        "unconventional_warface",
        "vice",
        "enochian",
        "umbrood_protocols",
    ]

    primary_abilities = [
        "awareness",
        "art",
        "leadership",
        "larceny",
        "meditation",
        "research",
        "survival",
        "technology",
        "cosmology",
        "enigmas",
        "finance",
        "law",
        "occult",
        "politics",
        "alertness",
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

    awareness = models.IntegerField(default=0)
    art = models.IntegerField(default=0)
    leadership = models.IntegerField(default=0)
    animal_kinship = models.IntegerField(default=0)
    blatancy = models.IntegerField(default=0)
    carousing = models.IntegerField(default=0)
    flying = models.IntegerField(default=0)
    high_ritual = models.IntegerField(default=0)
    lucid_dreaming = models.IntegerField(default=0)
    search = models.IntegerField(default=0)
    seduction = models.IntegerField(default=0)
    larceny = models.IntegerField(default=0)
    meditation = models.IntegerField(default=0)
    research = models.IntegerField(default=0)
    survival = models.IntegerField(default=0)
    technology = models.IntegerField(default=0)
    acrobatics = models.IntegerField(default=0)
    archery = models.IntegerField(default=0)
    biotech = models.IntegerField(default=0)
    energy_weapons = models.IntegerField(default=0)
    jetpack = models.IntegerField(default=0)
    riding = models.IntegerField(default=0)
    torture = models.IntegerField(default=0)
    cosmology = models.IntegerField(default=0)
    enigmas = models.IntegerField(default=0)
    finance = models.IntegerField(default=0)
    law = models.IntegerField(default=0)
    occult = models.IntegerField(default=0)
    politics = models.IntegerField(default=0)
    area_knowledge = models.IntegerField(default=0)
    belief_systems = models.IntegerField(default=0)
    cryptography = models.IntegerField(default=0)
    demolitions = models.IntegerField(default=0)
    lore = models.IntegerField(default=0)
    media = models.IntegerField(default=0)
    pharmacopeia = models.IntegerField(default=0)

    cooking = models.IntegerField(default=0)
    diplomacy = models.IntegerField(default=0)
    instruction = models.IntegerField(default=0)
    intrigue = models.IntegerField(default=0)
    intuition = models.IntegerField(default=0)
    mimicry = models.IntegerField(default=0)
    negotiation = models.IntegerField(default=0)
    newspeak = models.IntegerField(default=0)
    scan = models.IntegerField(default=0)
    scrounging = models.IntegerField(default=0)
    style = models.IntegerField(default=0)
    blind_fighting = models.IntegerField(default=0)
    climbing = models.IntegerField(default=0)
    disguise = models.IntegerField(default=0)
    elusion = models.IntegerField(default=0)
    escapology = models.IntegerField(default=0)
    fast_draw = models.IntegerField(default=0)
    fast_talk = models.IntegerField(default=0)
    fencing = models.IntegerField(default=0)
    fortune_telling = models.IntegerField(default=0)
    gambling = models.IntegerField(default=0)
    gunsmith = models.IntegerField(default=0)
    heavy_weapons = models.IntegerField(default=0)
    hunting = models.IntegerField(default=0)
    hypnotism = models.IntegerField(default=0)
    jury_rigging = models.IntegerField(default=0)
    microgravity_operations = models.IntegerField(default=0)
    misdirection = models.IntegerField(default=0)
    networking = models.IntegerField(default=0)
    pilot = models.IntegerField(default=0)
    psychology = models.IntegerField(default=0)
    security = models.IntegerField(default=0)
    speed_reading = models.IntegerField(default=0)
    swimming = models.IntegerField(default=0)
    conspiracy_theory = models.IntegerField(default=0)
    chantry_politics = models.IntegerField(default=0)
    covert_culture = models.IntegerField(default=0)
    cultural_savvy = models.IntegerField(default=0)
    helmsman = models.IntegerField(default=0)
    history_knowledge = models.IntegerField(default=0)
    power_brokering = models.IntegerField(default=0)
    propaganda = models.IntegerField(default=0)
    theology = models.IntegerField(default=0)
    unconventional_warface = models.IntegerField(default=0)
    vice = models.IntegerField(default=0)

    enochian = models.IntegerField(default=0)
    umbrood_protocols = models.IntegerField(default=0)

    allied_characters = models.ManyToManyField(Character, blank=True)
    enhancement_devices = models.ManyToManyField(Wonder, blank=True)

    background_points = 5

    class Meta:
        verbose_name = "Human (Mage)"
        verbose_name_plural = "Humans (Mage)"
        ordering = ["name"]
