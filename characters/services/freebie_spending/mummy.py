"""
Mummy gameline Freebie Spending Services.

This module provides freebie spending services for Mummy: The Resurrection characters:
- MtRHumanFreebieSpendingService - base for Mummy gameline humans
- MummyFreebieSpendingService - Reborn mummies with Hekau, Sekhem, Balance
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


class MtRHumanFreebieSpendingService(HumanFreebieSpendingService):
    """
    Freebie spending service for Mummy gameline humans.

    Inherits all common human handlers. Currently no additional
    MtR-gameline-specific traits for mortals.
    """

    pass


class MummyFreebieSpendingService(MtRHumanFreebieSpendingService):
    """
    Freebie spending service for Mummy characters.

    Handles Mummy-specific freebie spending categories including
    Hekau paths, Sekhem, and Balance.
    """

    @handler("Hekau")
    def _handle_hekau(self, example, **kwargs) -> FreebieSpendResult:
        """Handle Hekau path freebie spending."""
        trait = example.name
        property_name = example.property_name
        current_value = getattr(self.character, property_name)
        new_value = current_value + 1
        cost = get_freebie_cost("hekau")

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
                error="Hekau at maximum",
            )

        # Apply the change
        setattr(self.character, property_name, new_value)
        self.character.save()

        # Record and deduct
        self._record_spending(trait, "hekau", new_value, cost)
        self._deduct_freebies(cost)

        return FreebieSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} freebies on {trait}",
        )

    @handler("Sekhem")
    def _handle_sekhem(self, **kwargs) -> FreebieSpendResult:
        """Handle Sekhem freebie spending."""
        trait = "Sekhem"
        cost = get_freebie_cost("sekhem")
        current_value = self.character.sekhem
        new_value = current_value + 1

        if cost > self.character.freebies:
            return FreebieSpendResult(
                success=False,
                trait=trait,
                cost=cost,
                message="",
                error="Not enough freebies",
            )

        if new_value > 10:
            return FreebieSpendResult(
                success=False,
                trait=trait,
                cost=cost,
                message="",
                error="Sekhem at maximum",
            )

        # Apply the change
        self.character.sekhem = new_value
        self.character.save()

        # Record and deduct
        self._record_spending(trait, "sekhem", new_value, cost)
        self._deduct_freebies(cost)

        return FreebieSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} freebies on Sekhem",
        )

    @handler("Balance")
    def _handle_balance(self, **kwargs) -> FreebieSpendResult:
        """Handle Balance freebie spending."""
        trait = "Balance"
        cost = get_freebie_cost("balance")
        current_value = self.character.balance
        new_value = current_value + 1

        if cost > self.character.freebies:
            return FreebieSpendResult(
                success=False,
                trait=trait,
                cost=cost,
                message="",
                error="Not enough freebies",
            )

        if new_value > 10:
            return FreebieSpendResult(
                success=False,
                trait=trait,
                cost=cost,
                message="",
                error="Balance at maximum",
            )

        # Apply the change
        self.character.balance = new_value
        self.character.save()

        # Record and deduct
        self._record_spending(trait, "balance", new_value, cost)
        self._deduct_freebies(cost)

        return FreebieSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} freebies on Balance",
        )

    # =========================================================================
    # APPLIERS - Apply/deny freebie spending requests
    # =========================================================================

    @applier("hekau")
    def _apply_hekau(self, freebie_request, approver, deny=False) -> FreebieApplyResult:
        """Apply or deny approved Hekau freebie spending."""
        if deny:
            from characters.models.mummy.hekau import Hekau

            hekau = Hekau.objects.filter(name=freebie_request.trait_name).first()
            if hekau:
                current_val = getattr(self.character, hekau.property_name, 0)
                if current_val > 0:
                    setattr(self.character, hekau.property_name, current_val - 1)
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

    @applier("sekhem")
    def _apply_sekhem(self, freebie_request, approver, deny=False) -> FreebieApplyResult:
        """Apply or deny approved Sekhem freebie spending."""
        if deny:
            if self.character.sekhem > 1:
                self.character.sekhem -= 1
                self.character.save()
            return FreebieApplyResult(
                success=True,
                trait="Sekhem",
                message="Denied and reverted Sekhem",
            )

        # Mark as approved
        freebie_request.approved = "Approved"
        freebie_request.approved_by = approver
        freebie_request.approved_at = timezone.now()
        freebie_request.save()
        return FreebieApplyResult(
            success=True,
            trait="Sekhem",
            message="Approved Sekhem",
        )

    @applier("balance")
    def _apply_balance(self, freebie_request, approver, deny=False) -> FreebieApplyResult:
        """Apply or deny approved Balance freebie spending."""
        if deny:
            if self.character.balance > 1:
                self.character.balance -= 1
                self.character.save()
            return FreebieApplyResult(
                success=True,
                trait="Balance",
                message="Denied and reverted Balance",
            )

        # Mark as approved
        freebie_request.approved = "Approved"
        freebie_request.approved_by = approver
        freebie_request.approved_at = timezone.now()
        freebie_request.save()
        return FreebieApplyResult(
            success=True,
            trait="Balance",
            message="Approved Balance",
        )


# Register Mummy gameline character types
FreebieSpendingServiceFactory.register("mtr_human", MtRHumanFreebieSpendingService)
FreebieSpendingServiceFactory.register("mummy", MummyFreebieSpendingService)
