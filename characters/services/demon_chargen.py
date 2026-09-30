"""Demon character-creation operations."""

from django.db import transaction

from characters.models.demon.apocalyptic_form import ApocalypticForm
from characters.services.result import ServiceResult


def apply_apocalyptic_form(demon, low_traits, high_traits):
    """Store a validated trait selection as the demon's Apocalyptic Form.

    A demon edits the form it already has only when no other demon, Earthbound
    or Visage uses it; otherwise it gets a new form named "<demon name>'s
    Apocalyptic Form". The caller advances and saves the demon.
    """
    with transaction.atomic():
        apocalyptic_form = demon.apocalyptic_form
        if apocalyptic_form is None or _is_shared(apocalyptic_form, demon):
            apocalyptic_form = ApocalypticForm.objects.create(
                name=f"{demon.name}'s Apocalyptic Form",
                description=f"Apocalyptic form for {demon.name}",
            )
        apocalyptic_form.low_torment_traits.set(low_traits)
        apocalyptic_form.high_torment_traits.set(high_traits)
        demon.apocalyptic_form = apocalyptic_form
    return ServiceResult.ok(obj=apocalyptic_form)


def _is_shared(apocalyptic_form, demon):
    return (
        apocalyptic_form.demons.exclude(pk=demon.pk).exists()
        or apocalyptic_form.earthbound.exists()
        or apocalyptic_form.visages_using_as_default.exists()
    )
