"""
Mage gameline Freebie Spending Services.

This module provides freebie spending services for Mage: The Ascension characters:
- MtAHumanFreebieSpendingService - base for Mage gameline humans
- MageFreebieSpendingService - Awakened mages with Spheres, Arete, etc.
- SorcererFreebieSpendingService - Linear magic users with Paths and Rituals
- CompanionFreebieSpendingService - Consors (unawakened helpers)
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


class MtAHumanFreebieSpendingService(HumanFreebieSpendingService):
    """
    Freebie spending service for Mage gameline humans.

    Inherits all common human handlers. Currently no additional
    Mage-gameline-specific traits for mortals.
    """

    pass


class MageFreebieSpendingService(MtAHumanFreebieSpendingService):
    """
    Freebie spending service for Mage characters.

    Handles all Mage-specific freebie spending categories including
    Spheres, Arete, Practices, Tenets, Resonance, Rote Points, and Quintessence.
    """

    @handler("Sphere")
    def _handle_sphere(self, example, **kwargs) -> FreebieSpendResult:
        """Handle sphere freebie spending."""
        trait = example.name
        cost = self.character.freebie_cost("sphere")
        current_value = getattr(self.character, example.property_name)
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
        self.character.add_sphere(example.property_name)
        self.character.save()

        # Record and deduct
        self._record_spending(trait, "sphere", new_value, cost)
        self._deduct_freebies(cost)

        return FreebieSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} freebies on {trait}",
        )

    @handler("Arete")
    def _handle_arete(self, example=None, **kwargs) -> FreebieSpendResult:
        """Handle Arete freebie spending."""
        cost = self.character.freebie_cost("arete")
        current_value = self.character.arete
        new_value = current_value + 1

        # Validate Arete limits at character creation
        max_arete = 4 if self.character.total_freebies() == 45 else 3
        if current_value >= max_arete:
            return FreebieSpendResult(
                success=False,
                trait="Arete",
                cost=cost,
                message="",
                error=f"Arete cannot be raised above {max_arete} at character creation",
            )

        if cost > self.character.freebies:
            return FreebieSpendResult(
                success=False,
                trait="Arete",
                cost=cost,
                message="",
                error="Not enough freebies",
            )

        # Apply the change with optional practice
        if example:  # Practice for Arete increase
            trait = f"Arete ({example.name})"
            self.character.add_arete(example)
        else:
            trait = "Arete"
            self.character.arete = new_value

        self.character.save()

        # Record and deduct
        self._record_spending(trait, "arete", new_value, cost)
        self._deduct_freebies(cost)

        return FreebieSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} freebies on {trait}",
        )

    @handler("Resonance")
    def _handle_resonance(self, resonance="", **kwargs) -> FreebieSpendResult:
        """Handle resonance freebie spending."""
        from characters.models.mage.resonance import Resonance

        cost = self.character.freebie_cost("resonance")

        if cost > self.character.freebies:
            return FreebieSpendResult(
                success=False,
                trait=f"Resonance ({resonance})",
                cost=cost,
                message="",
                error="Not enough freebies",
            )

        # Get or create the resonance
        r = Resonance.objects.get_or_create(name=resonance)[0]
        current_value = self.character.resonance_rating(r)
        new_value = current_value + 1
        trait = f"Resonance ({resonance})"

        # Apply the change
        self.character.add_resonance(resonance)
        self.character.save()

        # Record and deduct
        self._record_spending(trait, "resonance", new_value, cost)
        self._deduct_freebies(cost)

        return FreebieSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} freebies on {trait}",
        )

    @handler("Tenet")
    def _handle_tenet(self, example, **kwargs) -> FreebieSpendResult:
        """Handle tenet freebie spending (free during character creation)."""
        trait = example.name
        cost = self.character.freebie_cost("tenet")  # Usually 0

        # Apply the change
        self.character.add_tenet(example)
        self.character.save()

        # Record (even though cost is 0) and deduct
        self._record_spending(trait, "tenet", 0, cost)
        if cost > 0:
            self._deduct_freebies(cost)

        return FreebieSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Added tenet {trait}",
        )

    @handler("Practice")
    def _handle_practice(self, example, **kwargs) -> FreebieSpendResult:
        """Handle practice freebie spending."""
        trait = example.name
        cost = self.character.freebie_cost("practice")
        current_value = self.character.practice_rating(example)
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
        self.character.add_practice(example)
        self.character.save()

        # Record and deduct
        self._record_spending(trait, "practice", new_value, cost)
        self._deduct_freebies(cost)

        return FreebieSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} freebies on {trait}",
        )

    @handler("Rote Points")
    def _handle_rote_points(self, **kwargs) -> FreebieSpendResult:
        """Handle rote points freebie spending."""
        trait = "Rote Points"
        cost = self.character.freebie_cost("rotes")
        new_value = self.character.rote_points + 4

        if cost > self.character.freebies:
            return FreebieSpendResult(
                success=False,
                trait=trait,
                cost=cost,
                message="",
                error="Not enough freebies",
            )

        # Apply the change
        self.character.rote_points += 4
        self.character.save()

        # Record and deduct
        self._record_spending(trait, "rotes", new_value, cost)
        self._deduct_freebies(cost)

        return FreebieSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} freebies on 4 Rote Points",
        )

    @handler("Quintessence")
    def _handle_quintessence(self, **kwargs) -> FreebieSpendResult:
        """Handle quintessence freebie spending."""
        trait = "Quintessence"
        cost = self.character.freebie_cost("quintessence")
        new_value = self.character.quintessence + 4

        if cost > self.character.freebies:
            return FreebieSpendResult(
                success=False,
                trait=trait,
                cost=cost,
                message="",
                error="Not enough freebies",
            )

        # Apply the change
        self.character.quintessence += 4
        self.character.save()

        # Record and deduct
        self._record_spending(trait, "quintessence", new_value, cost)
        self._deduct_freebies(cost)

        return FreebieSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} freebies on 4 Quintessence",
        )

    # =========================================================================
    # APPLIERS - Apply/deny freebie spending requests
    # =========================================================================

    @applier("sphere")
    def _apply_sphere(self, freebie_request, approver, deny=False) -> FreebieApplyResult:
        """Apply or deny approved sphere freebie spending."""
        if deny:
            # Revert the sphere
            from characters.models.mage.sphere import Sphere

            s = Sphere.objects.filter(name=freebie_request.trait_name).first()
            if s:
                current_val = getattr(self.character, s.property_name, 0)
                if current_val > 0:
                    setattr(self.character, s.property_name, current_val - 1)
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

    @applier("arete")
    def _apply_arete(self, freebie_request, approver, deny=False) -> FreebieApplyResult:
        """Apply or deny approved Arete freebie spending."""
        if deny:
            # Revert Arete
            if self.character.arete > 1:
                self.character.arete -= 1
                self.character.save()
            return FreebieApplyResult(
                success=True,
                trait="Arete",
                message="Denied and reverted Arete",
            )

        # Mark as approved
        freebie_request.approved = "Approved"
        freebie_request.approved_by = approver
        freebie_request.approved_at = timezone.now()
        freebie_request.save()
        return FreebieApplyResult(
            success=True,
            trait="Arete",
            message="Approved Arete increase",
        )

    @applier("resonance")
    def _apply_resonance(self, freebie_request, approver, deny=False) -> FreebieApplyResult:
        """Apply or deny approved resonance freebie spending."""
        if deny:
            # Parse resonance name from "Resonance (Dynamic)"
            trait_name = freebie_request.trait_name
            if "(" in trait_name:
                resonance_name = trait_name.split("(")[1].rstrip(")")
            else:
                resonance_name = trait_name

            # Remove resonance
            rr = self.character.resonance_ratings.filter(resonance__name=resonance_name).first()
            if rr:
                if rr.rating > 1:
                    rr.rating -= 1
                    rr.save()
                else:
                    rr.delete()

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

    @applier("tenet")
    def _apply_tenet(self, freebie_request, approver, deny=False) -> FreebieApplyResult:
        """Apply or deny approved tenet freebie spending."""
        if deny:
            from characters.models.mage.focus import Tenet

            tenet = Tenet.objects.filter(name=freebie_request.trait_name).first()
            if tenet and tenet in self.character.other_tenets.all():
                self.character.other_tenets.remove(tenet)
            return FreebieApplyResult(
                success=True,
                trait=freebie_request.trait_name,
                message=f"Denied and removed tenet {freebie_request.trait_name}",
            )

        # Mark as approved
        freebie_request.approved = "Approved"
        freebie_request.approved_by = approver
        freebie_request.approved_at = timezone.now()
        freebie_request.save()
        return FreebieApplyResult(
            success=True,
            trait=freebie_request.trait_name,
            message=f"Approved tenet {freebie_request.trait_name}",
        )

    @applier("practice")
    def _apply_practice(self, freebie_request, approver, deny=False) -> FreebieApplyResult:
        """Apply or deny approved practice freebie spending."""
        if deny:
            from characters.models.mage.focus import Practice

            practice = Practice.objects.filter(name=freebie_request.trait_name).first()
            if practice:
                pr = self.character.practice_ratings.filter(practice=practice).first()
                if pr:
                    if pr.rating > 1:
                        pr.rating -= 1
                        pr.save()
                    else:
                        pr.delete()
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
            message=f"Approved practice {freebie_request.trait_name}",
        )

    @applier("rotes")
    def _apply_rotes(self, freebie_request, approver, deny=False) -> FreebieApplyResult:
        """Apply or deny approved rote points freebie spending."""
        if deny:
            # Revert rote points
            self.character.rote_points = max(0, self.character.rote_points - 4)
            self.character.save()
            return FreebieApplyResult(
                success=True,
                trait="Rote Points",
                message="Denied and reverted Rote Points",
            )

        # Mark as approved
        freebie_request.approved = "Approved"
        freebie_request.approved_by = approver
        freebie_request.approved_at = timezone.now()
        freebie_request.save()
        return FreebieApplyResult(
            success=True,
            trait="Rote Points",
            message="Approved Rote Points",
        )

    @applier("quintessence")
    def _apply_quintessence(self, freebie_request, approver, deny=False) -> FreebieApplyResult:
        """Apply or deny approved quintessence freebie spending."""
        if deny:
            # Revert quintessence
            self.character.quintessence = max(0, self.character.quintessence - 4)
            self.character.save()
            return FreebieApplyResult(
                success=True,
                trait="Quintessence",
                message="Denied and reverted Quintessence",
            )

        # Mark as approved
        freebie_request.approved = "Approved"
        freebie_request.approved_by = approver
        freebie_request.approved_at = timezone.now()
        freebie_request.save()
        return FreebieApplyResult(
            success=True,
            trait="Quintessence",
            message="Approved Quintessence",
        )


class SorcererFreebieSpendingService(MtAHumanFreebieSpendingService):
    """
    Freebie spending service for Sorcerer characters.

    Sorcerers use linear magic with Paths and Rituals,
    NOT Spheres or Arete like Awakened mages.
    """

    @handler("Path")
    def _handle_path(self, example, **kwargs) -> FreebieSpendResult:
        """Handle sorcerer path freebie spending.

        Requires practice and ability kwargs for new paths.
        """
        practice = kwargs.get("practice")
        ability = kwargs.get("ability")

        trait = example.name
        cost = self.character.freebie_cost("path")
        current_value = self.character.path_rating(example)
        new_value = current_value + 1

        if cost > self.character.freebies:
            return FreebieSpendResult(
                success=False,
                trait=trait,
                cost=cost,
                message="",
                error="Not enough freebies",
            )

        # Apply the change - add_path requires practice and ability
        self.character.add_path(example, practice, ability)
        self.character.save()

        # Build trait name with practice/ability info
        if practice and ability:
            trait = f"{trait}({practice.name}, {ability.name})"

        # Record and deduct
        self._record_spending(trait, "path", new_value, cost)
        self._deduct_freebies(cost)

        return FreebieSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} freebies on {trait}",
        )

    @handler("Select Ritual")
    def _handle_select_ritual(self, example, **kwargs) -> FreebieSpendResult:
        """Handle selecting an existing sorcerer ritual."""
        trait = example.name
        cost = self.character.freebie_cost("ritual")

        if cost > self.character.freebies:
            return FreebieSpendResult(
                success=False,
                trait=trait,
                cost=cost,
                message="",
                error="Not enough freebies",
            )

        # Apply the change
        self.character.add_ritual(example)
        self.character.save()

        # Record and deduct
        self._record_spending(trait, "ritual", example.level, cost)
        self._deduct_freebies(cost)

        return FreebieSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} freebies on ritual {trait}",
        )

    @handler("Create Ritual")
    def _handle_create_ritual(self, example=None, **kwargs) -> FreebieSpendResult:
        """Handle creating a new sorcerer ritual.

        Requires name, path, level, description kwargs.
        """
        from characters.models.mage.sorcerer import LinearMagicRitual

        name = kwargs.get("ritual_name", "")
        path = kwargs.get("ritual_path")
        level = kwargs.get("ritual_level", 1)
        description = kwargs.get("ritual_description", "")

        if not name or not path:
            return FreebieSpendResult(
                success=False,
                trait="",
                cost=0,
                message="",
                error="Ritual name and path are required",
            )

        cost = self.character.freebie_cost("ritual")

        if cost > self.character.freebies:
            return FreebieSpendResult(
                success=False,
                trait=name,
                cost=cost,
                message="",
                error="Not enough freebies",
            )

        # Create the ritual
        ritual = LinearMagicRitual.objects.create(
            name=name, path=path, level=level, description=description
        )

        # Apply the change
        self.character.add_ritual(ritual)
        self.character.save()

        # Record and deduct
        self._record_spending(name, "ritual", cost, cost)
        self._deduct_freebies(cost)

        return FreebieSpendResult(
            success=True,
            trait=name,
            cost=cost,
            message=f"Spent {cost} freebies creating ritual {name}",
        )

    @handler("Ritual")
    def _handle_ritual(self, example, **kwargs) -> FreebieSpendResult:
        """Handle sorcerer ritual freebie spending (alias for Select Ritual)."""
        return self._handle_select_ritual(example, **kwargs)

    # =========================================================================
    # APPLIERS - Apply/deny freebie spending requests
    # =========================================================================

    @applier("path")
    def _apply_path(self, freebie_request, approver, deny=False) -> FreebieApplyResult:
        """Apply or deny approved sorcerer path freebie spending."""
        if deny:
            from characters.models.mage.sorcerer import LinearMagicPath

            path = LinearMagicPath.objects.filter(name=freebie_request.trait_name).first()
            if path:
                pr = self.character.path_ratings.filter(path=path).first()
                if pr:
                    if pr.rating > 1:
                        pr.rating -= 1
                        pr.save()
                    else:
                        pr.delete()
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

    @applier("ritual")
    def _apply_ritual(self, freebie_request, approver, deny=False) -> FreebieApplyResult:
        """Apply or deny approved sorcerer ritual freebie spending."""
        if deny:
            from characters.models.mage.sorcerer import LinearMagicRitual

            ritual = LinearMagicRitual.objects.filter(name=freebie_request.trait_name).first()
            if ritual:
                self.character.rituals.remove(ritual)
            return FreebieApplyResult(
                success=True,
                trait=freebie_request.trait_name,
                message=f"Denied and removed ritual {freebie_request.trait_name}",
            )

        # Mark as approved
        freebie_request.approved = "Approved"
        freebie_request.approved_by = approver
        freebie_request.approved_at = timezone.now()
        freebie_request.save()
        return FreebieApplyResult(
            success=True,
            trait=freebie_request.trait_name,
            message=f"Approved ritual {freebie_request.trait_name}",
        )


class CompanionFreebieSpendingService(MtAHumanFreebieSpendingService):
    """
    Freebie spending service for Companion (Consor) characters.

    Companions are unawakened helpers to mages. They have access
    to standard human traits plus Special Advantages and Charms.
    """

    @handler("Advantage")
    def _handle_advantage(self, example, value=None, **kwargs) -> FreebieSpendResult:
        """Handle Special Advantage freebie spending."""
        trait = example.name
        current_value = self.character.advantage_rating(example)
        new_value = value if value is not None else current_value + 1
        # Advantage cost is typically by rating
        cost = new_value - current_value

        if cost > self.character.freebies:
            return FreebieSpendResult(
                success=False,
                trait=trait,
                cost=cost,
                message="",
                error="Not enough freebies",
            )

        # Apply the change
        self.character.add_advantage(example, new_value)
        self.character.save()

        # Record and deduct
        self._record_spending(trait, "advantage", new_value, cost)
        self._deduct_freebies(cost)

        return FreebieSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} freebies on {trait}",
        )

    @handler("Charm")
    def _handle_charm(self, example, **kwargs) -> FreebieSpendResult:
        """Handle Spirit Charm freebie spending."""
        trait = example.name
        cost = self.character.freebie_cost("charms")

        if cost > self.character.freebies:
            return FreebieSpendResult(
                success=False,
                trait=trait,
                cost=cost,
                message="",
                error="Not enough freebies",
            )

        # Apply the change
        self.character.charms.add(example)
        self.character.save()

        # Record and deduct
        self._record_spending(trait, "charm", 1, cost)
        self._deduct_freebies(cost)

        return FreebieSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} freebies on Charm: {trait}",
        )

    # =========================================================================
    # APPLIERS - Apply/deny freebie spending requests
    # =========================================================================

    @applier("advantage")
    def _apply_advantage(self, freebie_request, approver, deny=False) -> FreebieApplyResult:
        """Apply or deny approved Special Advantage freebie spending."""
        if deny:
            from characters.models.mage.companion import Advantage

            advantage = Advantage.objects.filter(name=freebie_request.trait_name).first()
            if advantage:
                ar = self.character.advantage_ratings.filter(advantage=advantage).first()
                if ar:
                    if ar.rating > 1:
                        ar.rating -= 1
                        ar.save()
                    else:
                        ar.delete()
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

    @applier("charm")
    def _apply_charm(self, freebie_request, approver, deny=False) -> FreebieApplyResult:
        """Apply or deny approved Spirit Charm freebie spending."""
        if deny:
            from characters.models.werewolf.charm import SpiritCharm

            charm = SpiritCharm.objects.filter(name=freebie_request.trait_name).first()
            if charm:
                self.character.charms.remove(charm)
            return FreebieApplyResult(
                success=True,
                trait=freebie_request.trait_name,
                message=f"Denied and removed Charm {freebie_request.trait_name}",
            )

        # Mark as approved
        freebie_request.approved = "Approved"
        freebie_request.approved_by = approver
        freebie_request.approved_at = timezone.now()
        freebie_request.save()
        return FreebieApplyResult(
            success=True,
            trait=freebie_request.trait_name,
            message=f"Approved Charm: {freebie_request.trait_name}",
        )


# Register Mage gameline character types
FreebieSpendingServiceFactory.register("mta_human", MtAHumanFreebieSpendingService)
FreebieSpendingServiceFactory.register("mage", MageFreebieSpendingService)
FreebieSpendingServiceFactory.register("sorcerer", SorcererFreebieSpendingService)
FreebieSpendingServiceFactory.register("companion", CompanionFreebieSpendingService)
