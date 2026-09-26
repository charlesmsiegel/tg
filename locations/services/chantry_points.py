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


def background_removal_error(rating):
    """Why ``rating`` cannot lose a dot, or None when it can."""
    floor = rating.chantry.free_dots(rating.bg.property_name)
    if rating.rating <= floor:
        return f"The first {floor} {rating.bg} dots are free and cannot be removed."
    return None


def _detach_linked_object(chantry, rating):
    linked_location_id = rating.linked_location_id
    if linked_location_id is not None:
        chantry.nodes.remove(linked_location_id)
        if chantry.chantry_library_id == linked_location_id:
            chantry.chantry_library.contained_within.remove(chantry)
            chantry.chantry_library = None
            chantry.save(update_fields=["chantry_library"])
    rating.linked_object = None
    rating.url = ""
    rating.note = ""
    rating.complete = False


def remove_background_dot(rating):
    """Refund one dot. A rating that reaches 0 is deleted.

    A linked Node or Library is detached from the chantry and the link, note
    and URL are cleared so the wizard asks for it again. The linked object
    itself is never deleted.
    """
    with transaction.atomic():
        locked = _lock(rating.chantry)
        rating = ChantryBackgroundRating.objects.select_related("bg").get(
            pk=rating.pk, chantry=locked
        )
        rating.chantry = locked
        error = background_removal_error(rating)
        if error:
            raise ValidationError(error)
        if rating.linked_location_id or rating.linked_character_id:
            _detach_linked_object(locked, rating)
        rating.rating -= 1
        if rating.rating == 0:
            rating.delete()
            return None
        rating.save()
        return rating


def ie_removal_error(chantry):
    """Why the Integrated Effects score cannot drop by one, or None."""
    score = chantry.integrated_effects_score
    if score <= 0:
        return "Integrated Effects is already at 0."
    allowance = Chantry.INTEGRATED_EFFECTS_NUMBERS[score - 1]
    spent = chantry.spent_integrated_effect_points()
    if spent > allowance:
        return (
            f"Chosen effects use {spent} points; Integrated Effects {score - 1} "
            f"allows {allowance}. Remove an effect first."
        )
    return None


def remove_ie_dot(chantry):
    """Refund one Integrated Effects dot. Returns the new score."""
    with transaction.atomic():
        locked = _lock(chantry)
        error = ie_removal_error(locked)
        if error:
            raise ValidationError(error)
        locked.integrated_effects_score -= 1
        locked.save(update_fields=["integrated_effects_score"])
        chantry.integrated_effects_score = locked.integrated_effects_score
        return locked.integrated_effects_score


def remove_effect(chantry, effect):
    """Remove a chosen integrated effect, freeing its IE points."""
    with transaction.atomic():
        locked = _lock(chantry)
        if not locked.integrated_effects.filter(pk=effect.pk).exists():
            raise ValidationError(f"{effect} is not one of this chantry's effects.")
        locked.integrated_effects.remove(effect)


def affordable_effects(chantry):
    """Effects the chantry can still integrate: within its rank and its remaining IE points."""
    from characters.models.mage.effect import Effect

    return Effect.objects.filter(
        rote_cost__gt=0,
        rote_cost__lte=chantry.current_ie_points(),
        max_sphere__lte=chantry.rank,
    ).exclude(pk__in=chantry.integrated_effects.values("pk"))


def has_affordable_effect(chantry):
    return affordable_effects(chantry).exists()


def apply_type_grants(chantry):
    """Give a library-type chantry its free Library dots.

    Creates the Library rating at the free floor or raises it to the floor.
    Does nothing for other types; dots already above the floor are kept.
    Returns the Library rating, or None when no grant applies.
    """
    with transaction.atomic():
        locked = _lock(chantry)
        floor = locked.free_dots("library")
        if floor == 0:
            return None
        library, _ = Background.objects.get_or_create(
            property_name="library", defaults={"name": "Library"}
        )
        rating = _held_rating(locked, library)
        if rating is None:
            return ChantryBackgroundRating.objects.create(chantry=locked, bg=library, rating=floor)
        if rating.rating < floor:
            rating.rating = floor
            rating.save(update_fields=["rating"])
        return rating
