"""
Wraith gameline XP Spending Services.

This module provides XP spending services for Wraith: The Oblivion characters:
- WtOHumanXPSpendingService - base for Wraith gameline humans
- WraithXPSpendingService - Wraiths with Arcanoi, Pathos, etc.
"""

from characters.costs import get_xp_cost
from django.utils import timezone

from .base import (
    HumanXPSpendingService,
    XPApplyResult,
    XPSpendingServiceFactory,
    XPSpendResult,
    applier,
    handler,
)


class WtOHumanXPSpendingService(HumanXPSpendingService):
    """
    XP spending service for Wraith gameline humans.

    Inherits all common human handlers. Currently no additional
    WtO-gameline-specific traits for mortals.
    """

    pass


class WraithXPSpendingService(WtOHumanXPSpendingService):
    """
    XP spending service for Wraith characters.

    Handles Wraith-specific XP spending categories including
    Arcanoi, Pathos, and Corpus.
    """

    @handler("Arcanos")
    def _handle_arcanos(self, example, **kwargs) -> XPSpendResult:
        """Handle Arcanos XP spending."""
        trait = example.name
        property_name = example.property_name
        current_value = getattr(self.character, property_name)
        new_value = current_value + 1

        # Calculate cost: 10 × current (new = 10)
        if current_value == 0:
            cost = 10  # New arcanos
        else:
            cost = get_xp_cost("arcanos") * current_value

        self.character.spend_xp(
            trait_name=property_name,
            trait_display=trait,
            cost=cost,
            category="arcanos",
            trait_value=new_value,
        )

        return XPSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} XP on {trait}",
        )

    @handler("Pathos")
    def _handle_pathos(self, **kwargs) -> XPSpendResult:
        """Handle Pathos XP spending."""
        trait = "Pathos"
        current_value = self.character.pathos
        new_value = current_value + 1

        # Calculate cost: 2 × current value
        cost = get_xp_cost("pathos") * current_value

        self.character.spend_xp(
            trait_name="pathos",
            trait_display=trait,
            cost=cost,
            category="pathos",
            trait_value=new_value,
        )

        return XPSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} XP on Pathos",
        )

    @handler("Corpus")
    def _handle_corpus(self, **kwargs) -> XPSpendResult:
        """Handle Corpus XP spending."""
        trait = "Corpus"
        current_value = self.character.corpus
        new_value = current_value + 1

        # Calculate cost: 1 × current value
        cost = get_xp_cost("corpus") * current_value

        self.character.spend_xp(
            trait_name="corpus",
            trait_display=trait,
            cost=cost,
            category="corpus",
            trait_value=new_value,
        )

        return XPSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} XP on Corpus",
        )

    # =========================================================================
    # APPLIERS - Apply approved XP spending requests
    # =========================================================================

    @applier("arcanos")
    def _apply_arcanos(self, xp_request, approver) -> XPApplyResult:
        """Apply approved Arcanos XP spending."""
        from characters.models.wraith.arcanos import Arcanos

        arcanos = Arcanos.objects.get(name=xp_request.trait_name)
        self.character.approve_xp_spend(
            xp_request.id, arcanos.property_name, xp_request.trait_value, approver
        )
        return XPApplyResult(
            success=True,
            trait=xp_request.trait_name,
            message=f"Approved {xp_request.trait_name} increase to {xp_request.trait_value}",
        )

    @applier("pathos")
    def _apply_pathos(self, xp_request, approver) -> XPApplyResult:
        """Apply approved Pathos XP spending."""
        self.character.approve_xp_spend(xp_request.id, "pathos", xp_request.trait_value, approver)
        return XPApplyResult(
            success=True,
            trait="Pathos",
            message=f"Approved Pathos increase to {xp_request.trait_value}",
        )

    @applier("corpus")
    def _apply_corpus(self, xp_request, approver) -> XPApplyResult:
        """Apply approved Corpus XP spending."""
        self.character.approve_xp_spend(xp_request.id, "corpus", xp_request.trait_value, approver)
        return XPApplyResult(
            success=True,
            trait="Corpus",
            message=f"Approved Corpus increase to {xp_request.trait_value}",
        )


# Register Wraith gameline character types
XPSpendingServiceFactory.register("wto_human", WtOHumanXPSpendingService)
XPSpendingServiceFactory.register("wraith", WraithXPSpendingService)
