"""Learning a rote: the one place rote points are spent."""

from django.db import transaction

from characters.models.core.ability_block import Ability
from characters.models.mage.effect import Effect
from characters.models.mage.focus import Practice
from characters.models.mage.rote import Rote
from characters.services.result import ServiceResult

SPHERE_FIELDS = (
    "correspondence",
    "time",
    "spirit",
    "matter",
    "life",
    "forces",
    "entropy",
    "mind",
    "prime",
)

NOT_ENOUGH_ROTE_POINTS = "Not enough Rote Points"


def _locked_rote_points(mage):
    return (
        type(mage).objects.select_for_update().values_list("rote_points", flat=True).get(pk=mage.pk)
    )


def learn_rote(mage, cleaned_data):
    """Create or select a rote (and its effect) for ``mage`` and pay its cost.

    ``cleaned_data`` comes from a valid ``RoteCreationForm``. The mage row is
    locked and its rote points re-read, so concurrent submissions cannot spend
    the same points twice. New effects must be learnable by the mage.
    """
    with transaction.atomic():
        mage.rote_points = _locked_rote_points(mage)
        if cleaned_data["select_or_create_rote"]:
            if cleaned_data["select_or_create_effect"]:
                effect = Effect(
                    **{sphere: cleaned_data.get(sphere) or 0 for sphere in SPHERE_FIELDS},
                    description=cleaned_data.get("systems"),
                    name=cleaned_data.get("name"),
                    status="Sub",
                    owner=mage.owner,
                    chronicle=mage.chronicle,
                )
                if not effect.is_learnable(mage) or effect.cost() > mage.rote_points:
                    return ServiceResult.fail(NOT_ENOUGH_ROTE_POINTS)
                effect.save()
            else:
                effect = cleaned_data["effect_options"]
            practice_pk = cleaned_data.get("practice")
            ability_pk = cleaned_data.get("ability")
            rote = Rote.objects.create(
                name=cleaned_data.get("name"),
                practice=Practice.objects.get(pk=practice_pk) if practice_pk else None,
                attribute=cleaned_data.get("attribute"),
                ability=Ability.objects.get(pk=ability_pk) if ability_pk else None,
                description=cleaned_data.get("description"),
                effect=effect,
                status="Sub",
                chronicle=mage.chronicle,
                owner=mage.owner,
            )
        else:
            rote = cleaned_data["rote_options"]
            effect = rote.effect
        if effect.cost() > mage.rote_points:
            transaction.set_rollback(True)
            return ServiceResult.fail(NOT_ENOUGH_ROTE_POINTS)
        mage.rotes.add(rote)
        mage.rote_points -= effect.cost()
        mage.save()
    return ServiceResult.ok(f"Learned {rote.name}", rote)
