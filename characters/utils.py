"""
Character utilities.

This module contains utility functions used across the characters app.
"""


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
    from game.models import ObjectType

    # Normalize human types (vtm_human, mta_human, etc. all become "human")
    # Use endswith("_human") or exact match to avoid false positives with
    # strings like "inhuman" or "superhuman"
    if character_type.endswith("_human") or character_type == "human":
        character_type = "human"

    obj_type, _ = ObjectType.objects.get_or_create(
        name=character_type,
        defaults={"type": "char", "gameline": gameline}
    )
    return obj_type
