"""
Character utilities.

This module contains utility functions used across the characters app.
"""

from game.models import ObjectType


def trait_property_name(trait_name):
    """Property name of a built-in trait (a virtue, a Hekau path) from its display name.

    The chained freebie forms name these traits by property and show
    ``property_name.replace("_", " ").title()``; this is the inverse, used when a
    spending record stores only the display name.
    """
    return trait_name.strip().lower().replace(" ", "_")


def get_character_object_type(character_type, gameline="wod"):
    """Get or create an ObjectType for a character type.

    This function handles the common pattern of:
    1. Normalizing character type names (e.g., "vtm_human" -> "human")
    2. Getting or creating the ObjectType with standard defaults

    Args:
        character_type: The character type string (e.g., "vampire", "mage", "human")
        gameline: The gameline code (default: "wod")

    Returns:
        ObjectType instance for the given character type

    Example:
        >>> from characters.utils import get_character_object_type
        >>> obj_type = get_character_object_type("vtm_human")  # Returns "human" type
        >>> obj_type = get_character_object_type("vampire")
    """
    # Normalize human types (vtm_human, mta_human, etc. all become "human")
    # Use endswith("_human") or exact match to avoid false positives with
    # strings like "inhuman" or "superhuman"
    if character_type.endswith("_human") or character_type == "human":
        character_type = "human"

    obj_type, _ = ObjectType.objects.get_or_create(
        name=character_type, defaults={"type": "char", "gameline": gameline}
    )
    return obj_type
