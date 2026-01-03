"""
Changeling gameline XP Spending Services.

This module provides XP spending services for Changeling: The Dreaming characters:
- CtDHumanXPSpendingService - base for Changeling gameline humans
- ChangelingXPSpendingService - Changelings with Arts, Realms, Glamour
- InanimaeXPSpendingService - Inanimae (elemental fae)
- NunnehiXPSpendingService - Nunnehi (Native American fae)
"""

from django.utils import timezone

from .base import (
    HumanXPSpendingService,
    XPApplyResult,
    XPSpendingServiceFactory,
    XPSpendResult,
    applier,
    handler,
)


class CtDHumanXPSpendingService(HumanXPSpendingService):
    """
    XP spending service for Changeling gameline humans.

    Inherits all common human handlers. Currently no additional
    CtD-gameline-specific traits for mortals.
    """

    pass


class ChangelingXPSpendingService(CtDHumanXPSpendingService):
    """
    XP spending service for Changeling characters.

    Handles Changeling-specific XP spending categories including
    Arts, Realms, Glamour, and Banality reduction.
    """

    @handler("Art")
    def _handle_art(self, example, **kwargs) -> XPSpendResult:
        """Handle Art XP spending."""
        trait = example.name
        property_name = example.property_name
        current_value = getattr(self.character, property_name)
        new_value = current_value + 1

        # Determine if this is an affinity Art
        is_affinity = (
            self.character.is_affinity_art(example)
            if hasattr(self.character, "is_affinity_art")
            else False
        )

        if current_value == 0:
            cost = self.character.xp_cost("new_art", new_value)
        elif is_affinity:
            cost = self.character.xp_cost("affinity_art", new_value)
        else:
            cost = self.character.xp_cost("art", new_value)

        self.character.spend_xp(
            trait_name=property_name,
            trait_display=trait,
            cost=cost,
            category="art",
            trait_value=new_value,
        )

        return XPSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} XP on {trait}",
        )

    @handler("Realm")
    def _handle_realm(self, example, **kwargs) -> XPSpendResult:
        """Handle Realm XP spending."""
        trait = example.name
        property_name = example.property_name
        current_value = getattr(self.character, property_name)
        new_value = current_value + 1
        cost = self.character.xp_cost("realm", current_value)

        self.character.spend_xp(
            trait_name=property_name,
            trait_display=trait,
            cost=cost,
            category="realm",
            trait_value=new_value,
        )

        return XPSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} XP on {trait}",
        )

    @handler("Glamour")
    def _handle_glamour(self, **kwargs) -> XPSpendResult:
        """Handle Glamour XP spending."""
        trait = "Glamour"
        current_value = self.character.glamour
        new_value = current_value + 1
        cost = self.character.xp_cost("glamour", current_value)

        self.character.spend_xp(
            trait_name="glamour",
            trait_display=trait,
            cost=cost,
            category="glamour",
            trait_value=new_value,
        )

        return XPSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} XP on Glamour",
        )

    @handler("Banality Reduction")
    def _handle_banality_reduction(self, **kwargs) -> XPSpendResult:
        """Handle Banality reduction XP spending."""
        trait = "Banality Reduction"
        current_value = self.character.banality
        new_value = current_value - 1
        cost = self.character.xp_cost("banality_reduction", current_value)

        self.character.spend_xp(
            trait_name="banality",
            trait_display=trait,
            cost=cost,
            category="banality_reduction",
            trait_value=new_value,
        )

        return XPSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} XP to reduce Banality",
        )

    # =========================================================================
    # APPLIERS - Apply approved XP spending requests
    # =========================================================================

    @applier("art")
    def _apply_art(self, xp_request, approver) -> XPApplyResult:
        """Apply approved Art XP spending."""
        from characters.models.changeling.art import Art

        art = Art.objects.get(name=xp_request.trait_name)
        self.character.approve_xp_spend(
            xp_request.id, art.property_name, xp_request.trait_value, approver
        )
        return XPApplyResult(
            success=True,
            trait=xp_request.trait_name,
            message=f"Approved {xp_request.trait_name} increase to {xp_request.trait_value}",
        )

    @applier("realm")
    def _apply_realm(self, xp_request, approver) -> XPApplyResult:
        """Apply approved Realm XP spending."""
        from characters.models.changeling.realm import Realm

        realm = Realm.objects.get(name=xp_request.trait_name)
        self.character.approve_xp_spend(
            xp_request.id, realm.property_name, xp_request.trait_value, approver
        )
        return XPApplyResult(
            success=True,
            trait=xp_request.trait_name,
            message=f"Approved {xp_request.trait_name} increase to {xp_request.trait_value}",
        )

    @applier("glamour")
    def _apply_glamour(self, xp_request, approver) -> XPApplyResult:
        """Apply approved Glamour XP spending."""
        self.character.approve_xp_spend(xp_request.id, "glamour", xp_request.trait_value, approver)
        return XPApplyResult(
            success=True,
            trait="Glamour",
            message=f"Approved Glamour increase to {xp_request.trait_value}",
        )

    @applier("banality_reduction")
    def _apply_banality_reduction(self, xp_request, approver) -> XPApplyResult:
        """Apply approved Banality reduction XP spending."""
        self.character.approve_xp_spend(xp_request.id, "banality", xp_request.trait_value, approver)
        return XPApplyResult(
            success=True,
            trait="Banality",
            message=f"Approved Banality reduction to {xp_request.trait_value}",
        )


class InanimaeXPSpendingService(ChangelingXPSpendingService):
    """
    XP spending service for Inanimae characters.

    Inanimae are elemental fae with the same basic XP categories
    as regular Changelings.
    """

    pass


class NunnehiXPSpendingService(ChangelingXPSpendingService):
    """
    XP spending service for Nunnehi characters.

    Nunnehi are Native American fae with the same basic XP categories
    as regular Changelings.
    """

    pass


# Register Changeling gameline character types
XPSpendingServiceFactory.register("ctd_human", CtDHumanXPSpendingService)
XPSpendingServiceFactory.register("changeling", ChangelingXPSpendingService)
XPSpendingServiceFactory.register("inanimae", InanimaeXPSpendingService)
XPSpendingServiceFactory.register("nunnehi", NunnehiXPSpendingService)
