"""
Hunter gameline XP Spending Services.

This module provides XP spending services for Hunter: The Reckoning characters:
- HtRHumanXPSpendingService - base for Hunter gameline humans (includes Virtues)
- HunterXPSpendingService - Imbued hunters with Edges
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


class HtRHumanXPSpendingService(HumanXPSpendingService):
    """
    XP spending service for Hunter gameline humans.

    Adds Virtue handling for mortals in the HtR setting.
    Virtues: Conviction, Vision, Zeal
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


class HunterXPSpendingService(HtRHumanXPSpendingService):
    """
    XP spending service for Hunter (Imbued) characters.

    Handles Hunter-specific XP spending categories including
    Edges.
    """

    @handler("Edge")
    def _handle_edge(self, example, **kwargs) -> XPSpendResult:
        """Handle Edge XP spending."""
        trait = example.name
        # Edge cost is based on the edge's level
        edge_level = example.level if hasattr(example, "level") else 1
        cost = self.character.xp_cost("edge", edge_level)

        self.character.spend_xp(
            trait_name="",
            trait_display=trait,
            cost=cost,
            category="edge",
            trait_value=edge_level,
        )

        return XPSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} XP on Edge: {trait}",
        )

    # =========================================================================
    # APPLIERS - Apply approved XP spending requests
    # =========================================================================

    @applier("edge")
    def _apply_edge(self, xp_request, approver) -> XPApplyResult:
        """Apply approved Edge XP spending."""
        from characters.models.hunter.edge import Edge

        edge = Edge.objects.get(name=xp_request.trait_name)
        self.character.edges.add(edge)

        # Mark as approved
        xp_request.approved = "Approved"
        xp_request.approved_by = approver
        xp_request.approved_at = timezone.now()
        xp_request.save()

        return XPApplyResult(
            success=True,
            trait=xp_request.trait_name,
            message=f"Approved Edge: {xp_request.trait_name}",
        )


# Register Hunter gameline character types
XPSpendingServiceFactory.register("htr_human", HtRHumanXPSpendingService)
XPSpendingServiceFactory.register("hunter", HunterXPSpendingService)
