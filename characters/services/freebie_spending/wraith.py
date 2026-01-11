"""
Wraith gameline Freebie Spending Services.

This module provides freebie spending services for Wraith: The Oblivion characters:
- WtOHumanFreebieSpendingService - base for Wraith gameline humans
- WraithFreebieSpendingService - Wraiths with Arcanoi, Pathos, etc.
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


class WtOHumanFreebieSpendingService(HumanFreebieSpendingService):
    """
    Freebie spending service for Wraith gameline humans.

    Inherits all common human handlers. Currently no additional
    WtO-gameline-specific traits for mortals.
    """

    pass


class WraithFreebieSpendingService(WtOHumanFreebieSpendingService):
    """
    Freebie spending service for Wraith characters.

    Handles Wraith-specific freebie spending categories including
    Arcanoi, Pathos, and Corpus.
    """

    @handler("Arcanos")
    def _handle_arcanos(self, example, **kwargs) -> FreebieSpendResult:
        """Handle Arcanos freebie spending."""
        trait = example.name
        property_name = example.property_name
        current_value = getattr(self.character, property_name)
        new_value = current_value + 1

        # Arcanos cost varies - guild arcanos are typically cheaper
        is_guild = (
            self.character.is_guild_arcanos(example)
            if hasattr(self.character, "is_guild_arcanos")
            else False
        )
        cost = get_freebie_cost("guild_arcanos" if is_guild else "arcanos")

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
                error="Arcanos at maximum",
            )

        # Apply the change
        setattr(self.character, property_name, new_value)
        self.character.save()

        # Record and deduct
        self._record_spending(trait, "arcanos", new_value, cost)
        self._deduct_freebies(cost)

        return FreebieSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} freebies on {trait}",
        )

    @handler("Pathos")
    def _handle_pathos(self, **kwargs) -> FreebieSpendResult:
        """Handle Pathos freebie spending."""
        trait = "Pathos"
        cost = get_freebie_cost("pathos")
        current_value = self.character.pathos
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
                error="Pathos at maximum",
            )

        # Apply the change
        self.character.pathos = new_value
        self.character.save()

        # Record and deduct
        self._record_spending(trait, "pathos", new_value, cost)
        self._deduct_freebies(cost)

        return FreebieSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} freebies on Pathos",
        )

    @handler("Corpus")
    def _handle_corpus(self, **kwargs) -> FreebieSpendResult:
        """Handle Corpus freebie spending."""
        trait = "Corpus"
        cost = get_freebie_cost("corpus")
        current_value = self.character.corpus
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
                error="Corpus at maximum",
            )

        # Apply the change
        self.character.corpus = new_value
        self.character.save()

        # Record and deduct
        self._record_spending(trait, "corpus", new_value, cost)
        self._deduct_freebies(cost)

        return FreebieSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} freebies on Corpus",
        )

    # =========================================================================
    # APPLIERS - Apply/deny freebie spending requests
    # =========================================================================

    @applier("arcanos")
    def _apply_arcanos(self, freebie_request, approver, deny=False) -> FreebieApplyResult:
        """Apply or deny approved Arcanos freebie spending."""
        if deny:
            from characters.models.wraith.arcanos import Arcanos

            arcanos = Arcanos.objects.filter(name=freebie_request.trait_name).first()
            if arcanos:
                current_val = getattr(self.character, arcanos.property_name, 0)
                if current_val > 0:
                    setattr(self.character, arcanos.property_name, current_val - 1)
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

    @applier("pathos")
    def _apply_pathos(self, freebie_request, approver, deny=False) -> FreebieApplyResult:
        """Apply or deny approved Pathos freebie spending."""
        if deny:
            if self.character.pathos > 1:
                self.character.pathos -= 1
                self.character.save()
            return FreebieApplyResult(
                success=True,
                trait="Pathos",
                message="Denied and reverted Pathos",
            )

        # Mark as approved
        freebie_request.approved = "Approved"
        freebie_request.approved_by = approver
        freebie_request.approved_at = timezone.now()
        freebie_request.save()
        return FreebieApplyResult(
            success=True,
            trait="Pathos",
            message="Approved Pathos",
        )

    @applier("corpus")
    def _apply_corpus(self, freebie_request, approver, deny=False) -> FreebieApplyResult:
        """Apply or deny approved Corpus freebie spending."""
        if deny:
            if self.character.corpus > 1:
                self.character.corpus -= 1
                self.character.save()
            return FreebieApplyResult(
                success=True,
                trait="Corpus",
                message="Denied and reverted Corpus",
            )

        # Mark as approved
        freebie_request.approved = "Approved"
        freebie_request.approved_by = approver
        freebie_request.approved_at = timezone.now()
        freebie_request.save()
        return FreebieApplyResult(
            success=True,
            trait="Corpus",
            message="Approved Corpus",
        )


# Register Wraith gameline character types
FreebieSpendingServiceFactory.register("wto_human", WtOHumanFreebieSpendingService)
FreebieSpendingServiceFactory.register("wraith", WraithFreebieSpendingService)
