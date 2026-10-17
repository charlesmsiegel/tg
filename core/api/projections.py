"""Read-only projections: native IDs and relation identities are retained explicitly."""

from characters.models.core import Human
from characters.models.mage import Mage

ATTRIBUTES = (
    "strength",
    "dexterity",
    "stamina",
    "charisma",
    "manipulation",
    "appearance",
    "perception",
    "intelligence",
    "wits",
)
ABILITIES = (
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
)
SPHERES = (
    "correspondence",
    "time",
    "spirit",
    "mind",
    "entropy",
    "prime",
    "forces",
    "matter",
    "life",
)


def character_summary(character):
    return {
        "id": character.pk,
        "type": character.type,
        "gameline": character.gameline,
        "name": character.name,
        "owner_id": character.owner_id,
        "chronicle_id": character.chronicle_id,
        "status": character.status,
    }


def character_detail(character):
    result = character_summary(character) | {
        # A projection is not an archive: unlisted subtype fields are not exportable here.
        "projection": "tg-character-v1",
        "complete": False,
        "concept": character.concept,
        "notes": character.notes,
        "description": character.description,
        "public_info": character.public_info,
        "visibility": character.visibility,
        "npc": character.npc,
        "xp": character.xp,
    }
    if isinstance(character, Human):
        result["human"] = {
            "attributes": {key: getattr(character, key) for key in ATTRIBUTES},
            "abilities": {key: getattr(character, key) for key in ABILITIES},
            "nature_id": character.nature_id,
            "demeanor_id": character.demeanor_id,
            "willpower": character.willpower,
            "temporary_willpower": character.temporary_willpower,
            "history": character.history,
            "goals": character.goals,
            "current_health_levels": character.current_health_levels,
            "max_health_levels": character.max_health_levels,
            "backgrounds": list(
                character.backgrounds.order_by("pk").values(
                    "id", "bg_id", "rating", "note", "url", "complete", "pooled", "display_alt_name"
                )
            ),
            "merits_flaws": list(
                character.merit_flaw_ratings.order_by("pk").values("id", "mf_id", "rating")
            ),
        }
    if isinstance(character, Mage):
        result["mage"] = {
            "arete": character.arete,
            "spheres": {key: getattr(character, key) for key in SPHERES},
            "essence": character.essence,
            "affiliation_id": character.affiliation_id,
            "faction_id": character.faction_id,
            "subfaction_id": character.subfaction_id,
            "affinity_sphere_id": character.affinity_sphere_id,
            "quintessence": character.quintessence,
            "paradox": character.paradox,
            "metaphysical_tenet_id": character.metaphysical_tenet_id,
            "personal_tenet_id": character.personal_tenet_id,
            "ascension_tenet_id": character.ascension_tenet_id,
            "other_tenet_ids": list(
                character.other_tenets.order_by("pk").values_list("pk", flat=True)
            ),
            "instruments": list(character.instruments.order_by("pk").values("id", "name")),
            "practices": list(
                character.practicerating_set.order_by("pk").values("id", "practice_id", "rating")
            ),
        }
    return result


def chronicle_detail(chronicle):
    return {
        "id": chronicle.pk,
        "name": chronicle.name,
        "theme": chronicle.theme,
        "mood": chronicle.mood,
        "year": chronicle.year,
        "headings": chronicle.headings,
        "head_st_id": chronicle.head_st_id,
        "game_storyteller_ids": list(
            chronicle.game_storytellers.order_by("pk").values_list("pk", flat=True)
        ),
        "storytellers": list(
            chronicle.st_relationships.order_by("pk").values("user_id", "gameline_id")
        ),
    }
