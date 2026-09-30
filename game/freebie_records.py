"""Freebie spending records filed by hand (the ``game:freebie_spending_record`` pages).

A pending record means its cost has left the character's freebie pool: character
creation deducts as it records a spend, and a denial refunds exactly ``cost``. A record
filed by hand keeps the same bargain, so it is paid for when it is filed.
"""

from django.core.exceptions import ValidationError
from django.db import transaction

from game.models import FreebieSpendingRecord


def file_freebie_record(character, *, trait_name, trait_type, trait_value, cost):
    """Deduct ``cost`` from ``character``'s freebies and file a pending record for it.

    Raises ``ValidationError`` (keyed by field) for a negative cost, a cost the pool
    can't cover, or a character without a freebie pool.
    """
    if cost < 0:
        raise ValidationError({"cost": "Cost cannot be negative."})
    with transaction.atomic():
        # Locked and re-read so concurrent spends see each other's deduction.
        locked = type(character).objects.select_for_update().get(pk=character.pk)
        if not hasattr(locked, "freebies"):
            raise ValidationError("This character has no freebie points.")
        if cost > locked.freebies:
            raise ValidationError({"cost": f"Only {locked.freebies} freebie points left to spend."})
        locked.freebies -= cost
        locked.save(update_fields=["freebies"])
        return FreebieSpendingRecord.objects.create(
            character=locked,
            trait_name=trait_name,
            trait_type=trait_type,
            trait_value=trait_value,
            cost=cost,
        )
