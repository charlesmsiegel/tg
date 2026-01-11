"""
Demon gameline Freebie Spending Services.

This module provides freebie spending services for Demon: The Fallen characters:
- DtFHumanFreebieSpendingService - base for Demon gameline humans (includes Virtues)
- DemonFreebieSpendingService - Fallen angels with Lores, Faith, Torment
- ThrallFreebieSpendingService - Mortals bound to demons
- EarthboundFreebieSpendingService - Ancient demons bound to relics
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


class DtFHumanFreebieSpendingService(HumanFreebieSpendingService):
    """
    Freebie spending service for Demon gameline humans.

    Adds Virtue handling for mortals in the DtF setting.
    Virtues: Conscience, Conviction, Courage
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


class DemonFreebieSpendingService(DtFHumanFreebieSpendingService):
    """
    Freebie spending service for Demon (Fallen) characters.

    Handles Demon-specific freebie spending categories including
    Lores, Faith, and Torment reduction.
    """

    @handler("Lore")
    def _handle_lore(self, example, **kwargs) -> FreebieSpendResult:
        """Handle Lore freebie spending."""
        trait = example.name
        property_name = example.property_name
        current_value = getattr(self.character, property_name)
        new_value = current_value + 1
        cost = get_freebie_cost("lore")

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
                error="Lore at maximum",
            )

        # Apply the change
        setattr(self.character, property_name, new_value)
        self.character.save()

        # Record and deduct
        self._record_spending(trait, "lore", new_value, cost)
        self._deduct_freebies(cost)

        return FreebieSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} freebies on {trait}",
        )

    @handler("Faith")
    def _handle_faith(self, **kwargs) -> FreebieSpendResult:
        """Handle Faith freebie spending."""
        trait = "Faith"
        cost = get_freebie_cost("faith")
        current_value = self.character.faith
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
                error="Faith at maximum",
            )

        # Apply the change
        self.character.faith = new_value
        self.character.save()

        # Record and deduct
        self._record_spending(trait, "faith", new_value, cost)
        self._deduct_freebies(cost)

        return FreebieSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} freebies on Faith",
        )

    @handler("Torment Reduction")
    def _handle_torment_reduction(self, **kwargs) -> FreebieSpendResult:
        """Handle Torment reduction freebie spending."""
        trait = "Torment Reduction"
        cost = get_freebie_cost("torment_reduction")
        current_value = self.character.torment
        new_value = current_value - 1

        if cost > self.character.freebies:
            return FreebieSpendResult(
                success=False,
                trait=trait,
                cost=cost,
                message="",
                error="Not enough freebies",
            )

        if new_value < 0:
            return FreebieSpendResult(
                success=False,
                trait=trait,
                cost=cost,
                message="",
                error="Torment already at minimum",
            )

        # Apply the change
        self.character.torment = new_value
        self.character.save()

        # Record and deduct
        self._record_spending(trait, "torment_reduction", new_value, cost)
        self._deduct_freebies(cost)

        return FreebieSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} freebies to reduce Torment",
        )

    # =========================================================================
    # APPLIERS - Apply/deny freebie spending requests
    # =========================================================================

    @applier("lore")
    def _apply_lore(self, freebie_request, approver, deny=False) -> FreebieApplyResult:
        """Apply or deny approved Lore freebie spending."""
        if deny:
            from characters.models.demon.lore import Lore

            lore = Lore.objects.filter(name=freebie_request.trait_name).first()
            if lore:
                current_val = getattr(self.character, lore.property_name, 0)
                if current_val > 0:
                    setattr(self.character, lore.property_name, current_val - 1)
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

    @applier("faith")
    def _apply_faith(self, freebie_request, approver, deny=False) -> FreebieApplyResult:
        """Apply or deny approved Faith freebie spending."""
        if deny:
            if self.character.faith > 1:
                self.character.faith -= 1
                self.character.save()
            return FreebieApplyResult(
                success=True,
                trait="Faith",
                message="Denied and reverted Faith",
            )

        # Mark as approved
        freebie_request.approved = "Approved"
        freebie_request.approved_by = approver
        freebie_request.approved_at = timezone.now()
        freebie_request.save()
        return FreebieApplyResult(
            success=True,
            trait="Faith",
            message="Approved Faith",
        )

    @applier("torment_reduction")
    def _apply_torment_reduction(self, freebie_request, approver, deny=False) -> FreebieApplyResult:
        """Apply or deny approved Torment reduction freebie spending."""
        if deny:
            # Revert torment (increase it back)
            self.character.torment += 1
            self.character.save()
            return FreebieApplyResult(
                success=True,
                trait="Torment",
                message="Denied and reverted Torment reduction",
            )

        # Mark as approved
        freebie_request.approved = "Approved"
        freebie_request.approved_by = approver
        freebie_request.approved_at = timezone.now()
        freebie_request.save()
        return FreebieApplyResult(
            success=True,
            trait="Torment",
            message="Approved Torment reduction",
        )


class ThrallFreebieSpendingService(DtFHumanFreebieSpendingService):
    """
    Freebie spending service for Thrall characters.

    Thralls are mortals bound to demons. They may have access
    to Faith Potential but not Lores.
    """

    @handler("Faith Potential")
    def _handle_faith_potential(self, **kwargs) -> FreebieSpendResult:
        """Handle Faith Potential freebie spending."""
        trait = "Faith Potential"
        cost = get_freebie_cost("faith_potential")
        current_value = (
            self.character.faith_potential if hasattr(self.character, "faith_potential") else 0
        )
        new_value = current_value + 1

        if cost > self.character.freebies:
            return FreebieSpendResult(
                success=False,
                trait=trait,
                cost=cost,
                message="",
                error="Not enough freebies",
            )

        # Apply the change
        self.character.faith_potential = new_value
        self.character.save()

        # Record and deduct
        self._record_spending(trait, "faith_potential", new_value, cost)
        self._deduct_freebies(cost)

        return FreebieSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} freebies on Faith Potential",
        )

    # =========================================================================
    # APPLIERS - Apply/deny freebie spending requests
    # =========================================================================

    @applier("faith_potential")
    def _apply_faith_potential(self, freebie_request, approver, deny=False) -> FreebieApplyResult:
        """Apply or deny approved Faith Potential freebie spending."""
        if deny:
            if hasattr(self.character, "faith_potential") and self.character.faith_potential > 0:
                self.character.faith_potential -= 1
                self.character.save()
            return FreebieApplyResult(
                success=True,
                trait="Faith Potential",
                message="Denied and reverted Faith Potential",
            )

        # Mark as approved
        freebie_request.approved = "Approved"
        freebie_request.approved_by = approver
        freebie_request.approved_at = timezone.now()
        freebie_request.save()
        return FreebieApplyResult(
            success=True,
            trait="Faith Potential",
            message="Approved Faith Potential",
        )


class EarthboundFreebieSpendingService(DemonFreebieSpendingService):
    """
    Freebie spending service for Earthbound characters.

    Earthbound are ancient demons bound to relics. They share
    the same freebie categories as regular Demons.
    """

    pass


# Register Demon gameline character types
FreebieSpendingServiceFactory.register("dtf_human", DtFHumanFreebieSpendingService)
FreebieSpendingServiceFactory.register("demon", DemonFreebieSpendingService)
FreebieSpendingServiceFactory.register("thrall", ThrallFreebieSpendingService)
FreebieSpendingServiceFactory.register("earthbound", EarthboundFreebieSpendingService)
