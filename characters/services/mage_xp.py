"""The Mage sheet's "Spend XP/Rote Points" form: one call per category."""

from characters.services.result import ServiceResult
from characters.services.rotes import learn_rote
from characters.services.xp_spending import XPSpendingServiceFactory


def spend_mage_xp(mage, cleaned_data, rote_data=None):
    """Dispatch a valid ``MageXPForm`` submission to the one operation it names.

    * ``Image`` stores the uploaded image, as the sheet always has.
    * ``Rote`` learns the rote described by a valid ``RoteCreationForm``.
    * Every other category is an XP spend through the locked XP service.
    """
    category = cleaned_data["category"]
    if category == "Image":
        mage.image = cleaned_data["image_field"]
        mage.save()
        return ServiceResult.ok()
    if category == "Rote":
        return learn_rote(mage, rote_data)
    with XPSpendingServiceFactory.locked(mage) as service:
        return service.spend(
            category=category,
            example=cleaned_data["example"],
            value=cleaned_data["value"],
            note=cleaned_data["note"],
            pooled=cleaned_data["pooled"],
            resonance=cleaned_data["resonance"],
        )
