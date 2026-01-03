"""
Master cost dictionaries for freebie and XP spending.

This module centralizes all trait costs across gamelines, providing uniform
access patterns. Handlers are responsible for applying any modifiers
(affinity spheres, in-clan disciplines, background multipliers, new trait
costs, etc.).

Usage:
    from characters.costs import get_freebie_cost, get_xp_cost

    # Freebie cost (flat)
    cost = get_freebie_cost("sphere")  # Returns 7

    # XP cost (base multiplier - handler multiplies by current value)
    multiplier = get_xp_cost("ability")  # Returns 2
    cost = multiplier * current_value
"""

# =============================================================================
# FREEBIE COSTS - Flat costs during character creation
# =============================================================================

FREEBIE_COSTS = {
    # -------------------------------------------------------------------------
    # Universal (all characters)
    # -------------------------------------------------------------------------
    "attribute": 5,
    "ability": 2,
    "background": 1,  # Handler applies background.multiplier
    "willpower": 1,
    "meritflaw": "rating",  # Cost equals the merit/flaw rating
    # -------------------------------------------------------------------------
    # Mage (Awakened)
    # -------------------------------------------------------------------------
    "sphere": 7,
    "arete": 4,
    "quintessence": 1,
    "resonance": 3,
    "tenet": 0,
    "practice": 1,
    "rotes": 1,
    # -------------------------------------------------------------------------
    # Sorcerer / Psychic (Linear Magic)
    # -------------------------------------------------------------------------
    "path": 7,
    "ritual": 3,
    # -------------------------------------------------------------------------
    # Vampire
    # -------------------------------------------------------------------------
    "discipline": 7,
    "virtue": 2,
    "humanity": 1,
    "path_rating": 1,
    # -------------------------------------------------------------------------
    # Werewolf (Garou)
    # -------------------------------------------------------------------------
    "gift": 5,
    "rite": 1,
    "rage": 1,
    "gnosis": 2,
    "glory": 1,
    "honor": 1,
    "wisdom": 1,
    # -------------------------------------------------------------------------
    # Wraith
    # -------------------------------------------------------------------------
    "arcanos": 7,
    "pathos": 1,
    "passion": 2,
    "fetter": 1,
    "corpus": 1,
    # -------------------------------------------------------------------------
    # Changeling
    # -------------------------------------------------------------------------
    "art": 5,
    "realm": 3,
    "glamour": 3,
    "banality": 2,
    # -------------------------------------------------------------------------
    # Demon (Fallen)
    # -------------------------------------------------------------------------
    "lore": 7,
    "faith": 7,
    "temporary_faith": 1,
    # -------------------------------------------------------------------------
    # Thrall
    # -------------------------------------------------------------------------
    "faith_potential": 7,
    # -------------------------------------------------------------------------
    # Hunter (Imbued)
    # -------------------------------------------------------------------------
    "edge": 3,
    # -------------------------------------------------------------------------
    # Mummy (Amenti)
    # -------------------------------------------------------------------------
    "hekau": 5,
    "sekhem": 7,
    "balance": 2,
    "ba": 1,
}


# =============================================================================
# XP COSTS - Base multipliers for advancement during play
# Handlers multiply by current value and apply any modifiers (new/affinity/etc)
# =============================================================================

XP_COSTS = {
    # -------------------------------------------------------------------------
    # Universal (all characters)
    # -------------------------------------------------------------------------
    "attribute": 4,  # current × 4
    "ability": 2,  # current × 2
    "background": 3,  # current × 3 (Handler applies multiplier)
    "willpower": 1,  # current × 1
    "meritflaw": 3,  # 3 × |new_rating - current_rating|
    # -------------------------------------------------------------------------
    # Mage (Awakened)
    # -------------------------------------------------------------------------
    "sphere": 8,  # current × 8 (affinity = 7)
    "arete": 8,  # current × 8
    "resonance": 3,  # current × 3
    "practice": 1,  # current × 1
    "rotes": 1,  # Per rote
    "tenet": 0,  # Free
    # -------------------------------------------------------------------------
    # Sorcerer / Psychic
    # -------------------------------------------------------------------------
    "path": 7,  # current × 7
    "ritual": 2,  # Per ritual level
    # -------------------------------------------------------------------------
    # Vampire
    # -------------------------------------------------------------------------
    "discipline": 5,  # current × 5 (clan) or × 7 (out-of-clan)
    "virtue": 2,  # current × 2
    "humanity": 1,  # current × 1
    "path_rating": 1,  # current × 1
    # -------------------------------------------------------------------------
    # Werewolf (Garou)
    # -------------------------------------------------------------------------
    "gift": 3,  # level × 3 (breed/auspice/tribe)
    "rite": 1,  # level × 1
    "rage": 1,  # current × 1
    "gnosis": 2,  # current × 2
    "glory": 1,  # current × 1
    "honor": 1,  # current × 1
    "wisdom": 1,  # current × 1
    # -------------------------------------------------------------------------
    # Wraith
    # -------------------------------------------------------------------------
    "arcanos": 10,  # current × 10
    "pathos": 2,  # current × 2
    "corpus": 1,  # current × 1
    "angst": 1,  # current × 1
    # -------------------------------------------------------------------------
    # Changeling
    # -------------------------------------------------------------------------
    "art": 8,  # current × 8
    "realm": 5,  # current × 5
    "glamour": 3,  # current × 3
    "banality": 2,  # 2 × reduction
    # -------------------------------------------------------------------------
    # Demon (Fallen)
    # -------------------------------------------------------------------------
    "lore": 5,  # current × 5 (house) or × 7 (other)
    "faith": 10,  # current × 10
    "reduce_torment": 10,  # 10 per point
    # -------------------------------------------------------------------------
    # Thrall
    # -------------------------------------------------------------------------
    "faith_potential": 10,  # current × 10
    # -------------------------------------------------------------------------
    # Hunter (Imbued)
    # -------------------------------------------------------------------------
    "edge": 3,  # current × 3
    # -------------------------------------------------------------------------
    # Mummy (Amenti)
    # -------------------------------------------------------------------------
    "hekau": 5,  # current × 5 (web-favored) or × 7 (universal) or × 10 (other)
    "sekhem": 10,  # current × 10
    "balance": 2,  # current × 2
}


# =============================================================================
# COST LOOKUP FUNCTIONS
# =============================================================================


def get_freebie_cost(trait_type: str) -> int | str:
    """
    Get freebie point cost for a trait.

    Returns the raw cost - handlers apply any modifiers (background multiplier,
    affinity discounts, etc.) and handle new vs existing traits.

    Args:
        trait_type: The trait category (e.g., "ability", "sphere", "discipline")

    Returns:
        Cost as int, or "rating" for merit/flaws, or 10000 for unknown traits
    """
    trait_type = trait_type.lower().replace(" ", "_")
    return FREEBIE_COSTS.get(trait_type, 10000)


def get_xp_cost(trait_type: str) -> int:
    """
    Get XP cost multiplier for raising a trait.

    Returns the base multiplier - handlers multiply by current value and
    apply any modifiers (new trait costs, affinity/clan discounts, etc.).

    Args:
        trait_type: The trait category (e.g., "ability", "sphere", "discipline")

    Returns:
        Base multiplier as int, or 10000 for unknown traits
    """
    trait_type = trait_type.lower().replace(" ", "_")
    return XP_COSTS.get(trait_type, 10000)


def get_meritflaw_freebie_cost(rating: int) -> int:
    """
    Get freebie cost for a merit/flaw.

    Args:
        rating: The merit/flaw rating (positive for merits, negative for flaws)

    Returns:
        Absolute value of the rating as cost
    """
    return abs(rating)


def get_meritflaw_xp_cost(current_rating: int, new_rating: int) -> int:
    """
    Get XP cost for changing a merit/flaw rating.

    Args:
        current_rating: Current merit/flaw rating
        new_rating: Desired new rating

    Returns:
        3 × |new_rating - current_rating|
    """
    return 3 * abs(new_rating - current_rating)
