"""Demon character-creation operations."""

from django.db import transaction

from characters.models.demon.apocalyptic_form import ApocalypticForm
from characters.services.result import ServiceResult


def apply_apocalyptic_form(demon, low_traits, high_traits):
    """Store a validated trait selection as the demon's Apocalyptic Form.

    The form is found by the name "<demon name>'s Apocalyptic Form" (see the
    Step 4 spec, defect D7). The caller advances and saves the demon.
    """
    with transaction.atomic():
        apocalyptic_form, _ = ApocalypticForm.objects.get_or_create(
            name=f"{demon.name}'s Apocalyptic Form",
            defaults={"description": f"Apocalyptic form for {demon.name}"},
        )
        apocalyptic_form.low_torment_traits.set(low_traits)
        apocalyptic_form.high_torment_traits.set(high_traits)
        demon.apocalyptic_form = apocalyptic_form
    return ServiceResult.ok(obj=apocalyptic_form)
