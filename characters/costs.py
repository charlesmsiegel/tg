"""
Master cost dictionaries for freebie and XP spending.

This module centralizes all trait costs across gamelines, providing uniform
access patterns. Handlers are responsible for applying any modifiers
(affinity spheres, in-clan disciplines, background multipliers, etc.).

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
    "arete": 4,  # Max 3 at chargen
    "quintessence": 0.25,  # 1 freebie per 4 dots
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
    "humanity": 2,
    "path_rating": 2,
    # -------------------------------------------------------------------------
    # Werewolf (Garou)
    # -------------------------------------------------------------------------
    "gift": 7,  # Level One only at chargen
    "rite": 1,
    "rage": 1,
    "gnosis": 2,
    "glory": 1,
    "honor": 1,
    "wisdom": 1,
    # -------------------------------------------------------------------------
    # Wraith
    # -------------------------------------------------------------------------
    "arcanos": 5,
    "pathos": 0.5,  # 1 freebie per 2 dots
    "passion": 2,
    "fetter": 1,
    # corpus: Cannot be increased with freebie points (not in dict)
    "wraith_willpower": 2,  # Wraith-specific willpower cost
    # -------------------------------------------------------------------------
    # Changeling
    # -------------------------------------------------------------------------
    "art": 5,
    "realm": 2,
    "glamour": 3,
    "banality": 2,
    # -------------------------------------------------------------------------
    # Demon (Fallen)
    # -------------------------------------------------------------------------
    "lore": 7,
    "faith": 6,
    "temporary_faith": 1,
    # -------------------------------------------------------------------------
    # Thrall
    # -------------------------------------------------------------------------
    "faith_potential": 7,
    # -------------------------------------------------------------------------
    # Hunter (Imbued)
    # -------------------------------------------------------------------------
    "edge": 7,
    "conviction": 1,  # Max starting score of 8
    # -------------------------------------------------------------------------
    # Mummy (Amenti)
    # -------------------------------------------------------------------------
    "hekau": 5,
    "sekhem": 1,
    "balance": 4,
    "ba": 1,
    "mummy_ritual": 1,
    "mummy_spell": 1,
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
    "new_ability": 3,  # Flat cost for new ability
    "background": 3,  # current × 3 (Handler applies multiplier)
    "new_background": 5,  # Flat cost for new background
    "willpower": 1,  # current × 1
    "meritflaw": 3,  # 3 × |new_rating - current_rating|
    # -------------------------------------------------------------------------
    # Mage (Awakened)
    # -------------------------------------------------------------------------
    "sphere": 8,  # current × 8 (other spheres)
    "affinity_sphere": 7,  # current × 7 (affinity sphere)
    "new_sphere": 10,  # Flat cost for new sphere
    "arete": 8,  # current × 8
    "resonance": 3,  # current × 3
    "new_resonance": 5,  # Flat cost for new resonance
    "practice": 1,  # current × 1
    "new_practice": 3,  # Flat cost for new practice
    "rotes": 1,  # Per rote
    "tenet": 0,  # Free
    # -------------------------------------------------------------------------
    # Sorcerer / Psychic
    # -------------------------------------------------------------------------
    "path": 7,  # current × 7
    "new_path": 10,  # Flat cost for new path
    "ritual": 2,  # Per ritual level
    # -------------------------------------------------------------------------
    # Vampire
    # -------------------------------------------------------------------------
    "discipline": 5,  # current × 5 (clan)
    "out_of_clan_discipline": 7,  # current × 7 (out-of-clan)
    "caitiff_discipline": 6,  # current × 6 (Caitiff - no clan)
    "new_discipline": 10,  # Flat cost for new discipline
    "secondary_path": 4,  # current × 4 (Necromancy/Thaumaturgy secondary)
    "new_secondary_path": 7,  # Flat cost for new Necromancy/Thaumaturgy path
    "virtue": 2,  # current × 2 (does not increase WP after chargen)
    "humanity": 2,  # current × 2
    "path_rating": 2,  # current × 2 (Path of Enlightenment)
    # -------------------------------------------------------------------------
    # Werewolf (Garou)
    # -------------------------------------------------------------------------
    "gift": 3,  # level × 3 (breed/auspice/tribe)
    "other_gift": 5,  # level × 5 (other breed/auspice/tribe)
    "rite": 1,  # level × 1
    "rage": 1,  # current × 1
    "gnosis": 2,  # current × 2
    "glory": 1,  # current × 1
    "honor": 1,  # current × 1
    "wisdom": 1,  # current × 1
    # -------------------------------------------------------------------------
    # Wraith
    # -------------------------------------------------------------------------
    "arcanos": 3,  # current × 3
    "new_arcanos": 7,  # Flat cost for new arcanos
    "pathos": 2,  # current × 2
    "corpus": 1,  # current × 1
    "angst": 1,  # current × 1
    # Passion, Fetter, Background: Special (ST permission required)
    # -------------------------------------------------------------------------
    # Changeling
    # -------------------------------------------------------------------------
    "art": 4,  # current × 4
    "new_art": 7,  # Flat cost for new art
    "realm": 3,  # current × 3
    "new_realm": 5,  # Flat cost for new realm
    "glamour": 3,  # current × 3
    "banality": 2,  # 2 × reduction
    "changeling_willpower": 2,  # current × 2 (Changeling-specific)
    # -------------------------------------------------------------------------
    # Demon (Fallen)
    # -------------------------------------------------------------------------
    "lore": 5,  # current × 5 (house lore)
    "other_lore": 7,  # Used as multiplier for non-house lores
    "new_lore": 7,  # Flat cost for new lore (own house)
    "new_other_lore": 10,  # Flat cost for new lore (other house)
    "faith": 7,  # current × 7
    "reduce_torment": 10,  # 10 per point (decreases Torment)
    # -------------------------------------------------------------------------
    # Thrall
    # -------------------------------------------------------------------------
    "faith_potential": 10,  # current × 10
    # -------------------------------------------------------------------------
    # Mummy (Amenti)
    # -------------------------------------------------------------------------
    "hekau": 5,  # Alias for favored_hekau (backward compat)
    "favored_hekau": 4,  # current × 4 (web-favored)
    "other_hekau": 6,  # current × 6 (other paths)
    "udjasen_hekau": 5,  # current × 5 (Udja-sen - no favored)
    "new_hekau": 7,  # Flat cost for new hekau path
    "sekhem": 10,  # current × 10
    "balance": 7,  # current × 7
    "mummy_new_spell": 1,  # spell level
    "mummy_new_ritual": 1,  # ritual level
    # -------------------------------------------------------------------------
    # Companion (Mage)
    # -------------------------------------------------------------------------
    "advantage": 3,  # 3 × |rating_difference|
    "charm": 5,  # Flat cost per charm
}


# =============================================================================
# COST LOOKUP FUNCTIONS
# =============================================================================


def get_freebie_cost(trait_type: str) -> int | float | str:
    """
    Get freebie point cost for a trait.

    Returns the raw cost - handlers apply any modifiers (background multiplier,
    affinity discounts, etc.) and handle new vs existing traits.

    Args:
        trait_type: The trait category (e.g., "ability", "sphere", "discipline")

    Returns:
        Cost as int/float, or "rating" for merit/flaws, or 10000 for unknown traits
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
