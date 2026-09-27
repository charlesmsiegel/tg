"""Specialties added from the character sheet."""

from characters.models.core.specialty import Specialty
from characters.services.result import ServiceResult


def record_specialties(character, cleaned_data):
    """Add a named specialty for each stat the form offered and the user filled.

    ``cleaned_data`` keys are limited to ``character.needed_specialties()`` by
    ``SpecialtiesForm``, so an unrequested stat cannot be stored.
    """
    added = 0
    for stat, name in cleaned_data.items():
        if name:
            specialty, _ = Specialty.objects.get_or_create(name=name, stat=stat)
            character.specialties.add(specialty)
            added += 1
    character.save()
    return ServiceResult.ok("Specialties added." if added else "", obj=character)
