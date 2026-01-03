"""
Demon gameline XP Spending Services.

This module provides XP spending services for Demon: The Fallen characters:
- DtFHumanXPSpendingService - base for Demon gameline humans (includes Virtues)
- DemonXPSpendingService - Fallen angels with Lores, Faith, Torment
- ThrallXPSpendingService - Mortals bound to demons
- EarthboundXPSpendingService - Ancient demons bound to relics
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


class DtFHumanXPSpendingService(HumanXPSpendingService):
    """
    XP spending service for Demon gameline humans.

    Adds Virtue handling for mortals in the DtF setting.
    Virtues: Conscience, Conviction, Courage
    """

    @handler("Virtue")
    def _handle_virtue(self, example, **kwargs) -> XPSpendResult:
        """Handle virtue XP spending."""
        trait = example.name
        property_name = example.property_name
        current_value = getattr(self.character, property_name)
        new_value = current_value + 1
        cost = self.character.xp_cost("virtue", current_value)

        self.character.spend_xp(
            trait_name=property_name,
            trait_display=trait,
            cost=cost,
            category="virtue",
            trait_value=new_value,
        )

        return XPSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} XP on {trait}",
        )

    # =========================================================================
    # APPLIERS - Apply approved XP spending requests
    # =========================================================================

    @applier("virtue")
    def _apply_virtue(self, xp_request, approver) -> XPApplyResult:
        """Apply approved virtue XP spending."""
        from characters.models.core.virtue import Virtue

        virtue = Virtue.objects.get(name=xp_request.trait_name)
        self.character.approve_xp_spend(
            xp_request.id, virtue.property_name, xp_request.trait_value, approver
        )
        return XPApplyResult(
            success=True,
            trait=xp_request.trait_name,
            message=f"Approved {xp_request.trait_name} increase to {xp_request.trait_value}",
        )


class DemonXPSpendingService(DtFHumanXPSpendingService):
    """
    XP spending service for Demon (Fallen) characters.

    Handles Demon-specific XP spending categories including
    Lores, Faith, and Torment reduction.
    """

    @handler("Lore")
    def _handle_lore(self, example, **kwargs) -> XPSpendResult:
        """Handle Lore XP spending."""
        trait = example.name
        property_name = example.property_name
        current_value = getattr(self.character, property_name)
        new_value = current_value + 1

        # Determine if this is a House lore or common lore
        is_house = (
            self.character.is_house_lore(example)
            if hasattr(self.character, "is_house_lore")
            else False
        )

        if current_value == 0:
            cost = self.character.xp_cost("new_lore", new_value)
        elif is_house:
            cost = self.character.xp_cost("house_lore", new_value)
        else:
            cost = self.character.xp_cost("lore", new_value)

        self.character.spend_xp(
            trait_name=property_name,
            trait_display=trait,
            cost=cost,
            category="lore",
            trait_value=new_value,
        )

        return XPSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} XP on {trait}",
        )

    @handler("Faith")
    def _handle_faith(self, **kwargs) -> XPSpendResult:
        """Handle Faith XP spending."""
        trait = "Faith"
        current_value = self.character.faith
        new_value = current_value + 1
        cost = self.character.xp_cost("faith", current_value)

        self.character.spend_xp(
            trait_name="faith",
            trait_display=trait,
            cost=cost,
            category="faith",
            trait_value=new_value,
        )

        return XPSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} XP on Faith",
        )

    @handler("Torment Reduction")
    def _handle_torment_reduction(self, **kwargs) -> XPSpendResult:
        """Handle Torment reduction XP spending."""
        trait = "Torment Reduction"
        current_value = self.character.torment
        new_value = current_value - 1
        cost = self.character.xp_cost("torment_reduction", current_value)

        self.character.spend_xp(
            trait_name="torment",
            trait_display=trait,
            cost=cost,
            category="torment_reduction",
            trait_value=new_value,
        )

        return XPSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} XP to reduce Torment",
        )

    # =========================================================================
    # APPLIERS - Apply approved XP spending requests
    # =========================================================================

    @applier("lore")
    def _apply_lore(self, xp_request, approver) -> XPApplyResult:
        """Apply approved Lore XP spending."""
        from characters.models.demon.lore import Lore

        lore = Lore.objects.get(name=xp_request.trait_name)
        self.character.approve_xp_spend(
            xp_request.id, lore.property_name, xp_request.trait_value, approver
        )
        return XPApplyResult(
            success=True,
            trait=xp_request.trait_name,
            message=f"Approved {xp_request.trait_name} increase to {xp_request.trait_value}",
        )

    @applier("faith")
    def _apply_faith(self, xp_request, approver) -> XPApplyResult:
        """Apply approved Faith XP spending."""
        self.character.approve_xp_spend(xp_request.id, "faith", xp_request.trait_value, approver)
        return XPApplyResult(
            success=True,
            trait="Faith",
            message=f"Approved Faith increase to {xp_request.trait_value}",
        )

    @applier("torment_reduction")
    def _apply_torment_reduction(self, xp_request, approver) -> XPApplyResult:
        """Apply approved Torment reduction XP spending."""
        self.character.approve_xp_spend(xp_request.id, "torment", xp_request.trait_value, approver)
        return XPApplyResult(
            success=True,
            trait="Torment",
            message=f"Approved Torment reduction to {xp_request.trait_value}",
        )


class ThrallXPSpendingService(DtFHumanXPSpendingService):
    """
    XP spending service for Thrall characters.

    Thralls are mortals bound to demons. They may have access
    to Faith Potential but not Lores.
    """

    @handler("Faith Potential")
    def _handle_faith_potential(self, **kwargs) -> XPSpendResult:
        """Handle Faith Potential XP spending."""
        trait = "Faith Potential"
        current_value = (
            self.character.faith_potential if hasattr(self.character, "faith_potential") else 0
        )
        new_value = current_value + 1
        cost = self.character.xp_cost("faith_potential", current_value)

        self.character.spend_xp(
            trait_name="faith_potential",
            trait_display=trait,
            cost=cost,
            category="faith_potential",
            trait_value=new_value,
        )

        return XPSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} XP on Faith Potential",
        )

    # =========================================================================
    # APPLIERS - Apply approved XP spending requests
    # =========================================================================

    @applier("faith_potential")
    def _apply_faith_potential(self, xp_request, approver) -> XPApplyResult:
        """Apply approved Faith Potential XP spending."""
        self.character.approve_xp_spend(
            xp_request.id, "faith_potential", xp_request.trait_value, approver
        )
        return XPApplyResult(
            success=True,
            trait="Faith Potential",
            message=f"Approved Faith Potential increase to {xp_request.trait_value}",
        )


class EarthboundXPSpendingService(DemonXPSpendingService):
    """
    XP spending service for Earthbound characters.

    Earthbound are ancient demons bound to relics. They share
    the same XP categories as regular Demons.
    """

    pass


# Register Demon gameline character types
XPSpendingServiceFactory.register("dtf_human", DtFHumanXPSpendingService)
XPSpendingServiceFactory.register("demon", DemonXPSpendingService)
XPSpendingServiceFactory.register("thrall", ThrallXPSpendingService)
XPSpendingServiceFactory.register("earthbound", EarthboundXPSpendingService)
