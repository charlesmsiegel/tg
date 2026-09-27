"""Mage character-creation operations that write more than one form."""

from django.db import transaction

from characters.models.mage.mage import PracticeRating
from characters.services.result import ServiceResult


def set_starting_practices(focus_form):
    """Save the Focus step: tenets plus one PracticeRating per chosen practice.

    ``focus_form`` is a valid ``MageFocusForm`` whose practice formset is
    valid too. Everything is written in one transaction, or nothing is.
    """
    with transaction.atomic():
        mage = focus_form.save()
        for practice, rating in focus_form.practice_rows():
            if practice is not None:
                PracticeRating.objects.create(mage=mage, practice=practice, rating=rating)
    return ServiceResult.ok(obj=mage)
