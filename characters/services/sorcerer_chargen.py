"""Sorcerer character-creation operations."""

from django.db import transaction

from characters.models.mage.sorcerer import PathRating
from characters.services.result import ServiceResult

STARTING_WILLPOWER = 5
STARTING_FREEBIES = 21


def set_starting_numina(sorcerer, rows, *, with_practice):
    """Record the starting numina and the sorcerer's starting pools.

    ``rows`` are cleaned numina rows (path, rating, practice, ability) from a
    valid starting-numina formset. Psychic phenomena have no practice or
    ability (``with_practice=False``). The caller advances and saves.
    """
    with transaction.atomic():
        for row in rows:
            PathRating.objects.create(
                character=sorcerer,
                path=row["path"],
                rating=row["rating"],
                practice=row.get("practice") if with_practice else None,
                ability=row.get("ability") if with_practice else None,
            )
        sorcerer.willpower = STARTING_WILLPOWER
        sorcerer.freebies = STARTING_FREEBIES
        sorcerer.save()
    return ServiceResult.ok(obj=sorcerer)
