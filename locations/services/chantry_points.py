"""M20 chantry point rules: the single source of chantry costs and caps.

Predicates (``can_*``, ``*_error``, ``has_affordable_purchase``) read the
chantry as passed. Mutations lock the chantry row with ``select_for_update``
inside ``transaction.atomic()``, re-check their preconditions against the
locked row and raise ``ValidationError`` when a rule is broken. Views, forms
and templates never compute costs themselves.
"""

from django.core.exceptions import ValidationError
from django.db import transaction

from characters.models.core.background_block import Background
from locations.models.mage.chantry import Chantry, ChantryBackgroundRating

MAX_BACKGROUND_RATING = 5
MAX_IE_SCORE = 10


def _lock(chantry):
    return Chantry.objects.select_for_update().get(pk=chantry.pk)


def _held_rating(chantry, bg):
    return chantry.backgrounds.filter(bg=bg).order_by("pk").first()


def next_dot_cost(chantry, bg, current_rating=None):
    """Point cost of the next dot of ``bg``; dots under the free floor cost 0."""
    if current_rating is None:
        held = _held_rating(chantry, bg)
        current_rating = held.rating if held is not None else 0
    if current_rating < chantry.free_dots(bg.property_name):
        return 0
    return chantry.trait_cost(bg.property_name)


def background_purchase_error(chantry, bg, *, points=None, current_rating=None):
    """Why one more dot of ``bg`` cannot be bought, or None when it can."""
    if bg.property_name not in Chantry.allowed_backgrounds:
        return f"{bg} is not a chantry background."
    if current_rating is None:
        held = _held_rating(chantry, bg)
        current_rating = held.rating if held is not None else 0
    if current_rating >= MAX_BACKGROUND_RATING:
        return f"{bg} is already at {MAX_BACKGROUND_RATING} dots."
    if points is None:
        points = chantry.points
    cost = next_dot_cost(chantry, bg, current_rating)
    if cost > points:
        return f"{bg} costs {cost} points; {points} remain."
    return None


def can_buy_background(chantry, bg):
    return background_purchase_error(chantry, bg) is None


def ie_purchase_error(chantry, *, points=None):
    """Why one more Integrated Effects dot cannot be bought, or None."""
    if chantry.integrated_effects_score >= MAX_IE_SCORE:
        return f"Integrated Effects is already at {MAX_IE_SCORE}."
    if points is None:
        points = chantry.points
    cost = chantry.trait_cost("integrated_effects")
    if cost > points:
        return f"Integrated Effects costs {cost} points; {points} remain."
    return None


def can_buy_ie(chantry):
    return ie_purchase_error(chantry) is None


def affordable_backgrounds(chantry):
    """(new, existing): allowed Backgrounds not yet held, and held ratings,
    each of which can take one more dot now."""
    points = chantry.points
    held = {}
    for rating in chantry.backgrounds.select_related("bg").order_by("pk"):
        held.setdefault(rating.bg_id, rating)
    new, existing = [], []
    allowed = Background.objects.filter(property_name__in=Chantry.allowed_backgrounds)
    for bg in allowed.order_by("name"):
        rating = held.get(bg.pk)
        current = rating.rating if rating is not None else 0
        if background_purchase_error(chantry, bg, points=points, current_rating=current):
            continue
        if rating is None:
            new.append(bg)
        else:
            existing.append(rating)
    return new, existing


def has_affordable_purchase(chantry):
    new, existing = affordable_backgrounds(chantry)
    return bool(new or existing) or can_buy_ie(chantry)


def buy_background_dot(chantry, bg, *, note="", display_alt_name=False):
    """Buy one dot of ``bg``: create its rating at 1 or raise the held one."""
    with transaction.atomic():
        locked = _lock(chantry)
        error = background_purchase_error(locked, bg)
        if error:
            raise ValidationError(error)
        rating = _held_rating(locked, bg)
        if rating is None:
            return ChantryBackgroundRating.objects.create(
                chantry=locked,
                bg=bg,
                rating=1,
                note=note,
                display_alt_name=display_alt_name,
            )
        rating.rating += 1
        rating.save(update_fields=["rating"])
        return rating


def buy_ie_dot(chantry):
    """Buy one Integrated Effects dot. Returns the new score."""
    with transaction.atomic():
        locked = _lock(chantry)
        error = ie_purchase_error(locked)
        if error:
            raise ValidationError(error)
        locked.integrated_effects_score += 1
        locked.save(update_fields=["integrated_effects_score"])
        chantry.integrated_effects_score = locked.integrated_effects_score
        return locked.integrated_effects_score
