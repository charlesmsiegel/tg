"""
Mummy gameline XP Spending Services.

This module provides XP spending services for Mummy: The Resurrection characters:
- MtRHumanXPSpendingService - base for Mummy gameline humans
- MummyXPSpendingService - Reborn mummies with Hekau, Sekhem, Balance
"""


from characters.costs import get_xp_cost

from .base import (
    HumanXPSpendingService,
    XPApplyResult,
    XPSpendingServiceFactory,
    XPSpendResult,
    applier,
    handler,
)


class MtRHumanXPSpendingService(HumanXPSpendingService):
    """
    XP spending service for Mummy gameline humans.

    Inherits all common human handlers. Currently no additional
    MtR-gameline-specific traits for mortals.
    """

    pass


class MummyXPSpendingService(MtRHumanXPSpendingService):
    """
    XP spending service for Mummy characters.

    Handles Mummy-specific XP spending categories including
    Hekau paths, Sekhem, and Balance.
    """

    @handler("Hekau")
    def _handle_hekau(self, example, **kwargs) -> XPSpendResult:
        """Handle Hekau path XP spending."""
        trait = example.name
        property_name = example.property_name
        current_value = getattr(self.character, property_name)
        new_value = current_value + 1

        # Calculate cost: new=7, favored=4×current, other=6×current
        # TODO: Add favored hekau detection based on character's tem-akh
        if current_value == 0:
            cost = get_xp_cost("new_hekau")
        else:
            # Default to favored_hekau cost; should check character.is_favored_hekau()
            cost = get_xp_cost("favored_hekau") * current_value

        self.character.spend_xp(
            trait_name=property_name,
            trait_display=trait,
            cost=cost,
            category="hekau",
            trait_value=new_value,
        )

        return XPSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} XP on {trait}",
        )

    @handler("Sekhem")
    def _handle_sekhem(self, **kwargs) -> XPSpendResult:
        """Handle Sekhem XP spending."""
        trait = "Sekhem"
        current_value = self.character.sekhem
        new_value = current_value + 1

        # Calculate cost: 10 × current value
        cost = get_xp_cost("sekhem") * current_value

        self.character.spend_xp(
            trait_name="sekhem",
            trait_display=trait,
            cost=cost,
            category="sekhem",
            trait_value=new_value,
        )

        return XPSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} XP on Sekhem",
        )

    @handler("Balance")
    def _handle_balance(self, **kwargs) -> XPSpendResult:
        """Handle Balance XP spending."""
        trait = "Balance"
        current_value = self.character.balance
        new_value = current_value + 1

        # Calculate cost: 2 × current value
        cost = get_xp_cost("balance") * current_value

        self.character.spend_xp(
            trait_name="balance",
            trait_display=trait,
            cost=cost,
            category="balance",
            trait_value=new_value,
        )

        return XPSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} XP on Balance",
        )

    # =========================================================================
    # APPLIERS - Apply approved XP spending requests
    # =========================================================================

    @applier("hekau")
    def _apply_hekau(self, xp_request, approver) -> XPApplyResult:
        """Apply approved Hekau XP spending."""
        from characters.models.mummy.hekau import Hekau

        hekau = Hekau.objects.get(name=xp_request.trait_name)
        self.character.approve_xp_spend(
            xp_request.id, hekau.property_name, xp_request.trait_value, approver
        )
        return XPApplyResult(
            success=True,
            trait=xp_request.trait_name,
            message=f"Approved {xp_request.trait_name} increase to {xp_request.trait_value}",
        )

    @applier("sekhem")
    def _apply_sekhem(self, xp_request, approver) -> XPApplyResult:
        """Apply approved Sekhem XP spending."""
        self.character.approve_xp_spend(xp_request.id, "sekhem", xp_request.trait_value, approver)
        return XPApplyResult(
            success=True,
            trait="Sekhem",
            message=f"Approved Sekhem increase to {xp_request.trait_value}",
        )

    @applier("balance")
    def _apply_balance(self, xp_request, approver) -> XPApplyResult:
        """Apply approved Balance XP spending."""
        self.character.approve_xp_spend(xp_request.id, "balance", xp_request.trait_value, approver)
        return XPApplyResult(
            success=True,
            trait="Balance",
            message=f"Approved Balance increase to {xp_request.trait_value}",
        )


# Register Mummy gameline character types
XPSpendingServiceFactory.register("mtr_human", MtRHumanXPSpendingService)
XPSpendingServiceFactory.register("mummy", MummyXPSpendingService)
