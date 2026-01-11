"""
Werewolf gameline XP Spending Services.

This module provides XP spending services for Werewolf: The Apocalypse characters:
- WtAHumanXPSpendingService - base for Werewolf gameline humans
- GarouXPSpendingService - Werewolves with Gifts, Rites, Rage, Gnosis
- KinfolkXPSpendingService - Werewolf kin (limited/no Gifts)
- FeraXPSpendingService - Base for all Changing Breeds
- Per-breed services for each Fera type
"""

from django.utils import timezone

from characters.costs import get_xp_cost

from .base import (
    HumanXPSpendingService,
    XPApplyResult,
    XPSpendingServiceFactory,
    XPSpendResult,
    applier,
    handler,
)


class WtAHumanXPSpendingService(HumanXPSpendingService):
    """
    XP spending service for Werewolf gameline humans.

    Inherits all common human handlers. Currently no additional
    WtA-gameline-specific traits for mortals.
    """

    pass


class GarouXPSpendingService(WtAHumanXPSpendingService):
    """
    XP spending service for Garou (Werewolf) characters.

    Handles Garou-specific XP spending categories including
    Gifts, Rites, Rage, and Gnosis.

    Note: Renown (Glory, Honor, Wisdom) cannot be bought with XP -
    it must be earned through roleplay.
    """

    @handler("Gift")
    def _handle_gift(self, example, **kwargs) -> XPSpendResult:
        """Handle gift XP spending."""
        trait = example.name
        # Gift cost is 3 × gift level (for breed/auspice/tribe gifts)
        gift_level = example.rank if hasattr(example, "rank") else 1
        cost = get_xp_cost("gift") * gift_level

        self.character.spend_xp(
            trait_name="",
            trait_display=trait,
            cost=cost,
            category="gift",
            trait_value=gift_level,
        )

        return XPSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} XP on Gift: {trait}",
        )

    @handler("Rite")
    def _handle_rite(self, example, **kwargs) -> XPSpendResult:
        """Handle rite XP spending."""
        trait = example.name
        # Rite cost is 1 × rite level
        rite_level = example.level if hasattr(example, "level") else 1
        cost = get_xp_cost("rite") * rite_level

        self.character.spend_xp(
            trait_name="",
            trait_display=trait,
            cost=cost,
            category="rite",
            trait_value=rite_level,
        )

        return XPSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} XP on Rite: {trait}",
        )

    @handler("Rage")
    def _handle_rage(self, **kwargs) -> XPSpendResult:
        """Handle Rage XP spending."""
        trait = "Rage"
        current_value = self.character.rage
        new_value = current_value + 1

        # Cost is 1 × current value
        cost = get_xp_cost("rage") * current_value

        self.character.spend_xp(
            trait_name="rage",
            trait_display=trait,
            cost=cost,
            category="rage",
            trait_value=new_value,
        )

        return XPSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} XP on Rage",
        )

    @handler("Gnosis")
    def _handle_gnosis(self, **kwargs) -> XPSpendResult:
        """Handle Gnosis XP spending."""
        trait = "Gnosis"
        current_value = self.character.gnosis
        new_value = current_value + 1

        # Cost is 2 × current value
        cost = get_xp_cost("gnosis") * current_value

        self.character.spend_xp(
            trait_name="gnosis",
            trait_display=trait,
            cost=cost,
            category="gnosis",
            trait_value=new_value,
        )

        return XPSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} XP on Gnosis",
        )

    # =========================================================================
    # APPLIERS - Apply approved XP spending requests
    # =========================================================================

    @applier("gift")
    def _apply_gift(self, xp_request, approver) -> XPApplyResult:
        """Apply approved gift XP spending."""
        from characters.models.werewolf.gift import Gift

        gift = Gift.objects.get(name=xp_request.trait_name)
        self.character.gifts.add(gift)

        # Mark as approved
        xp_request.approved = "Approved"
        xp_request.approved_by = approver
        xp_request.approved_at = timezone.now()
        xp_request.save()

        return XPApplyResult(
            success=True,
            trait=xp_request.trait_name,
            message=f"Approved Gift: {xp_request.trait_name}",
        )

    @applier("rite")
    def _apply_rite(self, xp_request, approver) -> XPApplyResult:
        """Apply approved rite XP spending."""
        from characters.models.werewolf.rite import Rite

        rite = Rite.objects.get(name=xp_request.trait_name)
        self.character.rites.add(rite)

        # Mark as approved
        xp_request.approved = "Approved"
        xp_request.approved_by = approver
        xp_request.approved_at = timezone.now()
        xp_request.save()

        return XPApplyResult(
            success=True,
            trait=xp_request.trait_name,
            message=f"Approved Rite: {xp_request.trait_name}",
        )

    @applier("rage")
    def _apply_rage(self, xp_request, approver) -> XPApplyResult:
        """Apply approved Rage XP spending."""
        self.character.approve_xp_spend(xp_request.id, "rage", xp_request.trait_value, approver)
        return XPApplyResult(
            success=True,
            trait="Rage",
            message=f"Approved Rage increase to {xp_request.trait_value}",
        )

    @applier("gnosis")
    def _apply_gnosis(self, xp_request, approver) -> XPApplyResult:
        """Apply approved Gnosis XP spending."""
        self.character.approve_xp_spend(xp_request.id, "gnosis", xp_request.trait_value, approver)
        return XPApplyResult(
            success=True,
            trait="Gnosis",
            message=f"Approved Gnosis increase to {xp_request.trait_value}",
        )


class KinfolkXPSpendingService(WtAHumanXPSpendingService):
    """
    XP spending service for Kinfolk characters.

    Kinfolk are human relatives of werewolves. They typically
    don't have access to Gifts, Rage, or Gnosis.
    """

    pass


class FeraXPSpendingService(GarouXPSpendingService):
    """
    Base XP spending service for Fera (Changing Breeds).

    Fera share the same basic XP categories as Garou:
    Gifts, Rites, Rage, Gnosis. Breed-specific variations
    can be added in subclasses.
    """

    pass


class BastetXPSpendingService(FeraXPSpendingService):
    """XP spending service for Bastet (Werecats)."""

    pass


class CoraxXPSpendingService(FeraXPSpendingService):
    """XP spending service for Corax (Wereravens)."""

    pass


class GurahlXPSpendingService(FeraXPSpendingService):
    """XP spending service for Gurahl (Werebears)."""

    pass


class MokoleXPSpendingService(FeraXPSpendingService):
    """XP spending service for Mokole (Werelizards)."""

    pass


class NuwishaXPSpendingService(FeraXPSpendingService):
    """XP spending service for Nuwisha (Werecoyotes)."""

    pass


class RatkinXPSpendingService(FeraXPSpendingService):
    """XP spending service for Ratkin (Wererats)."""

    pass


# Register Werewolf gameline character types
XPSpendingServiceFactory.register("wta_human", WtAHumanXPSpendingService)
XPSpendingServiceFactory.register("werewolf", GarouXPSpendingService)
XPSpendingServiceFactory.register("kinfolk", KinfolkXPSpendingService)
XPSpendingServiceFactory.register("fera", FeraXPSpendingService)
XPSpendingServiceFactory.register("bastet", BastetXPSpendingService)
XPSpendingServiceFactory.register("corax", CoraxXPSpendingService)
XPSpendingServiceFactory.register("gurahl", GurahlXPSpendingService)
XPSpendingServiceFactory.register("mokole", MokoleXPSpendingService)
XPSpendingServiceFactory.register("nuwisha", NuwishaXPSpendingService)
XPSpendingServiceFactory.register("ratkin", RatkinXPSpendingService)
