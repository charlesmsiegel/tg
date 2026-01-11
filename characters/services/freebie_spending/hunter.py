"""
Hunter gameline Freebie Spending Services.

This module provides freebie spending services for Hunter: The Reckoning characters:
- HtRHumanFreebieSpendingService - base for Hunter gameline humans (includes Virtues)
- HunterFreebieSpendingService - Imbued hunters with Edges
"""

from django.utils import timezone

from characters.costs import get_freebie_cost

from .base import (
    FreebieApplyResult,
    FreebieSpendingServiceFactory,
    FreebieSpendResult,
    HumanFreebieSpendingService,
    applier,
    handler,
)


class HtRHumanFreebieSpendingService(HumanFreebieSpendingService):
    """
    Freebie spending service for Hunter gameline humans.

    Adds Virtue handling for mortals in the HtR setting.
    Virtues: Conviction, Vision, Zeal
    """

    @handler("Virtue")
    def _handle_virtue(self, example, **kwargs) -> FreebieSpendResult:
        """Handle virtue freebie spending."""
        trait = example.name
        property_name = example.property_name
        current_value = getattr(self.character, property_name)
        new_value = current_value + 1
        cost = get_freebie_cost("virtue")

        if cost > self.character.freebies:
            return FreebieSpendResult(
                success=False,
                trait=trait,
                cost=cost,
                message="",
                error="Not enough freebies",
            )

        if new_value > 5:
            return FreebieSpendResult(
                success=False,
                trait=trait,
                cost=cost,
                message="",
                error="Virtue at maximum",
            )

        # Apply the change
        setattr(self.character, property_name, new_value)
        self.character.save()

        # Record and deduct
        self._record_spending(trait, "virtue", new_value, cost)
        self._deduct_freebies(cost)

        return FreebieSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} freebies on {trait}",
        )

    # =========================================================================
    # APPLIERS - Apply/deny freebie spending requests
    # =========================================================================

    @applier("virtue")
    def _apply_virtue(self, freebie_request, approver, deny=False) -> FreebieApplyResult:
        """Apply or deny approved virtue freebie spending."""
        if deny:
            from characters.models.core.virtue import Virtue

            virtue = Virtue.objects.filter(name=freebie_request.trait_name).first()
            if virtue:
                current_val = getattr(self.character, virtue.property_name, 1)
                if current_val > 1:
                    setattr(self.character, virtue.property_name, current_val - 1)
                    self.character.save()
            return FreebieApplyResult(
                success=True,
                trait=freebie_request.trait_name,
                message=f"Denied and reverted {freebie_request.trait_name}",
            )

        # Mark as approved
        freebie_request.approved = "Approved"
        freebie_request.approved_by = approver
        freebie_request.approved_at = timezone.now()
        freebie_request.save()
        return FreebieApplyResult(
            success=True,
            trait=freebie_request.trait_name,
            message=f"Approved {freebie_request.trait_name}",
        )


class HunterFreebieSpendingService(HtRHumanFreebieSpendingService):
    """
    Freebie spending service for Hunter (Imbued) characters.

    Handles Hunter-specific freebie spending categories including
    Edges.
    """

    @handler("Edge")
    def _handle_edge(self, example, **kwargs) -> FreebieSpendResult:
        """Handle Edge freebie spending."""
        trait = example.name
        edge_level = example.level if hasattr(example, "level") else 1
        cost = get_freebie_cost("edge") * edge_level

        if cost > self.character.freebies:
            return FreebieSpendResult(
                success=False,
                trait=trait,
                cost=cost,
                message="",
                error="Not enough freebies",
            )

        # Apply the change
        self.character.edges.add(example)
        self.character.save()

        # Record and deduct
        self._record_spending(trait, "edge", edge_level, cost)
        self._deduct_freebies(cost)

        return FreebieSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} freebies on Edge: {trait}",
        )

    # =========================================================================
    # APPLIERS - Apply/deny freebie spending requests
    # =========================================================================

    @applier("edge")
    def _apply_edge(self, freebie_request, approver, deny=False) -> FreebieApplyResult:
        """Apply or deny approved Edge freebie spending."""
        if deny:
            from characters.models.hunter.edge import Edge

            edge = Edge.objects.filter(name=freebie_request.trait_name).first()
            if edge:
                self.character.edges.remove(edge)
            return FreebieApplyResult(
                success=True,
                trait=freebie_request.trait_name,
                message=f"Denied and removed Edge {freebie_request.trait_name}",
            )

        # Mark as approved
        freebie_request.approved = "Approved"
        freebie_request.approved_by = approver
        freebie_request.approved_at = timezone.now()
        freebie_request.save()
        return FreebieApplyResult(
            success=True,
            trait=freebie_request.trait_name,
            message=f"Approved Edge: {freebie_request.trait_name}",
        )


# Register Hunter gameline character types
FreebieSpendingServiceFactory.register("htr_human", HtRHumanFreebieSpendingService)
FreebieSpendingServiceFactory.register("hunter", HunterFreebieSpendingService)
