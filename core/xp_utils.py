"""
XP awarding utilities.

This module contains utility functions for atomically awarding XP to characters.
"""

from django.db import transaction


@transaction.atomic
def award_xp_atomically(parent_model, parent_pk, character_xp_map):
    """Award XP to characters atomically with proper locking.

    This function handles the common pattern of:
    1. Locking the parent object (Story/Scene) to prevent concurrent awards
    2. Checking if XP has already been awarded
    3. Locking each character and updating their XP
    4. Marking the parent as complete

    Args:
        parent_model: The model class (Story or Scene) that owns the XP award
        parent_pk: The primary key of the parent instance
        character_xp_map: Dict mapping Character objects to XP amounts (int)

    Returns:
        int: Number of characters who received XP

    Raises:
        ValidationError: If XP has already been awarded for this parent

    Example:
        >>> from game.models import Story
        >>> from core.xp_utils import award_xp_atomically
        >>> xp_map = {char1: 3, char2: 2, char3: 0}
        >>> count = award_xp_atomically(Story, story.pk, xp_map)
    """
    from django.core.exceptions import ValidationError

    from characters.models import Character

    # Lock the parent to prevent concurrent awards
    parent = parent_model.objects.select_for_update().get(pk=parent_pk)

    if parent.xp_given:
        raise ValidationError(
            f"XP has already been awarded for this {parent_model.__name__.lower()}",
            code="xp_already_given"
        )

    # Award to all characters atomically
    awarded_count = 0
    for char, xp_amount in character_xp_map.items():
        if xp_amount > 0:
            # Lock each character row to prevent race conditions
            locked_char = Character.objects.select_for_update().get(pk=char.pk)
            locked_char.xp += xp_amount
            locked_char.save(update_fields=["xp"])
            awarded_count += 1

    # Mark parent as complete
    parent.xp_given = True
    parent.save(update_fields=["xp_given"])

    return awarded_count


def calculate_story_xp(xp_categories):
    """Calculate total XP from story XP categories.

    Args:
        xp_categories: Dict with keys 'success', 'danger', 'growth', 'drama' (bool)
                      and 'duration' (int)

    Returns:
        int: Total XP to award
    """
    total = xp_categories.get("duration", 0)
    if xp_categories.get("success", False):
        total += 1
    if xp_categories.get("danger", False):
        total += 1
    if xp_categories.get("growth", False):
        total += 1
    if xp_categories.get("drama", False):
        total += 1
    return total
