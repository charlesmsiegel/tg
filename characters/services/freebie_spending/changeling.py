"""
Changeling gameline Freebie Spending Services.

This module provides freebie spending services for Changeling: The Dreaming characters:
- CtDHumanFreebieSpendingService - base for Changeling gameline humans
- ChangelingFreebieSpendingService - Changelings with Arts, Realms, Glamour
- InanimaeFreebieSpendingService - Inanimae (elemental fae)
- NunnehiFreebieSpendingService - Nunnehi (Native American fae)
"""

from django.utils import timezone

from .base import (
    FreebieApplyResult,
    FreebieSpendingServiceFactory,
    FreebieSpendResult,
    HumanFreebieSpendingService,
    applier,
    handler,
)


class CtDHumanFreebieSpendingService(HumanFreebieSpendingService):
    """
    Freebie spending service for Changeling gameline humans.

    Inherits all common human handlers. Currently no additional
    CtD-gameline-specific traits for mortals.
    """

    pass


class ChangelingFreebieSpendingService(CtDHumanFreebieSpendingService):
    """
    Freebie spending service for Changeling characters.

    Handles Changeling-specific freebie spending categories including
    Arts, Realms, Glamour, and Banality reduction.
    """

    @handler("Art")
    def _handle_art(self, example, **kwargs) -> FreebieSpendResult:
        """Handle Art freebie spending."""
        trait = example.name
        property_name = example.property_name
        current_value = getattr(self.character, property_name)
        new_value = current_value + 1
        cost = self.character.freebie_cost("art")

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
                error="Art at maximum",
            )

        # Apply the change
        setattr(self.character, property_name, new_value)
        self.character.save()

        # Record and deduct
        self._record_spending(trait, "art", new_value, cost)
        self._deduct_freebies(cost)

        return FreebieSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} freebies on {trait}",
        )

    @handler("Realm")
    def _handle_realm(self, example, **kwargs) -> FreebieSpendResult:
        """Handle Realm freebie spending."""
        trait = example.name
        property_name = example.property_name
        current_value = getattr(self.character, property_name)
        new_value = current_value + 1
        cost = self.character.freebie_cost("realm")

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
                error="Realm at maximum",
            )

        # Apply the change
        setattr(self.character, property_name, new_value)
        self.character.save()

        # Record and deduct
        self._record_spending(trait, "realm", new_value, cost)
        self._deduct_freebies(cost)

        return FreebieSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} freebies on {trait}",
        )

    @handler("Glamour")
    def _handle_glamour(self, **kwargs) -> FreebieSpendResult:
        """Handle Glamour freebie spending."""
        trait = "Glamour"
        cost = self.character.freebie_cost("glamour")
        current_value = self.character.glamour
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
                error="Glamour at maximum",
            )

        # Apply the change
        self.character.glamour = new_value
        self.character.temporary_glamour = new_value
        self.character.save()

        # Record and deduct
        self._record_spending(trait, "glamour", new_value, cost)
        self._deduct_freebies(cost)

        return FreebieSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} freebies on Glamour",
        )

    @handler("Banality Reduction")
    def _handle_banality_reduction(self, **kwargs) -> FreebieSpendResult:
        """Handle Banality reduction freebie spending."""
        trait = "Banality Reduction"
        cost = self.character.freebie_cost("banality_reduction")
        current_value = self.character.banality
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
                error="Banality already at minimum",
            )

        # Apply the change
        self.character.banality = new_value
        self.character.save()

        # Record and deduct
        self._record_spending(trait, "banality_reduction", new_value, cost)
        self._deduct_freebies(cost)

        return FreebieSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} freebies to reduce Banality",
        )

    # =========================================================================
    # APPLIERS - Apply/deny freebie spending requests
    # =========================================================================

    @applier("art")
    def _apply_art(self, freebie_request, approver, deny=False) -> FreebieApplyResult:
        """Apply or deny approved Art freebie spending."""
        if deny:
            from characters.models.changeling.art import Art

            art = Art.objects.filter(name=freebie_request.trait_name).first()
            if art:
                current_val = getattr(self.character, art.property_name, 0)
                if current_val > 0:
                    setattr(self.character, art.property_name, current_val - 1)
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

    @applier("realm")
    def _apply_realm(self, freebie_request, approver, deny=False) -> FreebieApplyResult:
        """Apply or deny approved Realm freebie spending."""
        if deny:
            from characters.models.changeling.realm import Realm

            realm = Realm.objects.filter(name=freebie_request.trait_name).first()
            if realm:
                current_val = getattr(self.character, realm.property_name, 0)
                if current_val > 0:
                    setattr(self.character, realm.property_name, current_val - 1)
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

    @applier("glamour")
    def _apply_glamour(self, freebie_request, approver, deny=False) -> FreebieApplyResult:
        """Apply or deny approved Glamour freebie spending."""
        if deny:
            if self.character.glamour > 1:
                self.character.glamour -= 1
                self.character.temporary_glamour = self.character.glamour
                self.character.save()
            return FreebieApplyResult(
                success=True,
                trait="Glamour",
                message="Denied and reverted Glamour",
            )

        # Mark as approved
        freebie_request.approved = "Approved"
        freebie_request.approved_by = approver
        freebie_request.approved_at = timezone.now()
        freebie_request.save()
        return FreebieApplyResult(
            success=True,
            trait="Glamour",
            message="Approved Glamour",
        )

    @applier("banality_reduction")
    def _apply_banality_reduction(
        self, freebie_request, approver, deny=False
    ) -> FreebieApplyResult:
        """Apply or deny approved Banality reduction freebie spending."""
        if deny:
            # Revert banality (increase it back)
            self.character.banality += 1
            self.character.save()
            return FreebieApplyResult(
                success=True,
                trait="Banality",
                message="Denied and reverted Banality reduction",
            )

        # Mark as approved
        freebie_request.approved = "Approved"
        freebie_request.approved_by = approver
        freebie_request.approved_at = timezone.now()
        freebie_request.save()
        return FreebieApplyResult(
            success=True,
            trait="Banality",
            message="Approved Banality reduction",
        )


class InanimaeFreebieSpendingService(ChangelingFreebieSpendingService):
    """
    Freebie spending service for Inanimae characters.

    Inanimae are elemental fae with the same basic freebie categories
    as regular Changelings.
    """

    pass


class NunnehiFreebieSpendingService(ChangelingFreebieSpendingService):
    """
    Freebie spending service for Nunnehi characters.

    Nunnehi are Native American fae with the same basic freebie categories
    as regular Changelings.
    """

    pass


# Register Changeling gameline character types
FreebieSpendingServiceFactory.register("ctd_human", CtDHumanFreebieSpendingService)
FreebieSpendingServiceFactory.register("changeling", ChangelingFreebieSpendingService)
FreebieSpendingServiceFactory.register("inanimae", InanimaeFreebieSpendingService)
FreebieSpendingServiceFactory.register("nunnehi", NunnehiFreebieSpendingService)
