"""
Mage gameline XP Spending Services.

This module provides XP spending services for Mage: The Ascension characters:
- MtAHumanXPSpendingService - base for Mage gameline humans
- MageXPSpendingService - Awakened mages with Spheres, Arete, etc.
- SorcererXPSpendingService - Linear magic users with Paths and Rituals
- CompanionXPSpendingService - Consors (unawakened helpers)
"""

from django.utils import timezone

from characters.costs import get_xp_cost

from .base import (
    HumanXPSpendingService,
    XPApplyResult,
    XPSpendingServiceFactory,
    XPSpendResult,
    applier,
    handler,
)


class MtAHumanXPSpendingService(HumanXPSpendingService):
    """
    XP spending service for Mage gameline humans.

    Inherits all common human handlers. Currently no additional
    Mage-gameline-specific traits for mortals.
    """

    pass


class MageXPSpendingService(MtAHumanXPSpendingService):
    """
    XP spending service for Mage characters.

    Handles all Mage-specific XP spending categories including
    Spheres, Arete, Practices, Tenets, Resonance, and Rote Points.
    """

    @handler("Sphere")
    def _handle_sphere(self, example, **kwargs) -> XPSpendResult:
        """Handle sphere XP spending."""
        trait = example.name
        current_value = getattr(self.character, example.property_name)
        new_value = current_value + 1

        # Check if sphere would exceed Arete
        if new_value > self.character.arete:
            return XPSpendResult(
                success=False,
                trait=trait,
                cost=0,
                message="",
                error=f"Sphere rating cannot exceed Arete ({self.character.arete})",
            )

        # Determine if affinity sphere (costs 7 instead of 8)
        is_affinity = (
            self.character.affinity_sphere
            and example.property_name == self.character.affinity_sphere.property_name
        )

        # Calculate cost: new=10, affinity=7×current, regular=8×current
        if current_value == 0:
            cost = get_xp_cost("new_sphere")
        elif is_affinity:
            cost = get_xp_cost("affinity_sphere") * current_value
        else:
            cost = get_xp_cost("sphere") * current_value  # Regular sphere (8×)

        self.character.spend_xp(
            trait_name=example.property_name,
            trait_display=trait,
            cost=cost,
            category="sphere",
            trait_value=new_value,
        )

        return XPSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} XP on {trait}",
        )

    @handler("Arete")
    def _handle_arete(self, **kwargs) -> XPSpendResult:
        """Handle Arete XP spending."""
        trait = "Arete"
        current_value = self.character.arete
        new_value = current_value + 1

        # Calculate cost: multiplier × current value
        cost = get_xp_cost("arete") * current_value

        self.character.spend_xp(
            trait_name="arete",
            trait_display=trait,
            cost=cost,
            category="arete",
            trait_value=new_value,
        )

        return XPSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} XP on Arete",
        )

    @handler("Practice")
    def _handle_practice(self, example, **kwargs) -> XPSpendResult:
        """Handle practice XP spending."""
        trait = example.name
        current_value = self.character.practice_rating(example)
        new_value = current_value + 1

        # Calculate cost: new=3, existing=1×current
        if current_value == 0:
            cost = get_xp_cost("new_practice")
        else:
            cost = get_xp_cost("practice") * current_value

        self.character.spend_xp(
            trait_name="",
            trait_display=trait,
            cost=cost,
            category="practice",
            trait_value=new_value,
        )

        return XPSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} XP on {trait}",
        )

    @handler("Tenet")
    def _handle_tenet(self, example, **kwargs) -> XPSpendResult:
        """Handle tenet XP spending."""
        trait = example.name
        cost = get_xp_cost("tenet")  # Free (0)

        self.character.spend_xp(
            trait_name="",
            trait_display=trait,
            cost=cost,
            category="tenet",
            trait_value=0,
        )

        return XPSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} XP on tenet {trait}",
        )

    @handler("Remove Tenet")
    def _handle_remove_tenet(self, example, **kwargs) -> XPSpendResult:
        """Handle tenet removal XP spending."""
        trait = "Remove " + example.name
        # Cost is 1 XP × (number of other tenets + 3)
        cost = 1 * (self.character.other_tenets.count() + 3)

        self.character.spend_xp(
            trait_name="",
            trait_display=trait,
            cost=cost,
            category="remove tenet",
            trait_value=0,
        )

        return XPSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} XP on removing tenet",
        )

    @handler("Resonance")
    def _handle_resonance(self, resonance="", **kwargs) -> XPSpendResult:
        """Handle resonance XP spending."""
        from characters.models.mage.resonance import Resonance

        trait = f"Resonance ({resonance})"
        r = Resonance.objects.get_or_create(name=resonance)[0]
        current_value = self.character.resonance_rating(r)

        # Calculate cost: new=5, existing=3×current
        if current_value == 0:
            cost = get_xp_cost("new_resonance")
        else:
            cost = get_xp_cost("resonance") * current_value

        self.character.spend_xp(
            trait_name="",
            trait_display=trait,
            cost=cost,
            category="resonance",
            trait_value=current_value + 1,
        )

        return XPSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} XP on {trait}",
        )

    @handler("Rote Points")
    def _handle_rote_points(self, **kwargs) -> XPSpendResult:
        """Handle rote points XP spending."""
        trait = "Rote Points"
        cost = get_xp_cost("rotes")  # 1 per point, buying 3 at a time
        new_value = self.character.total_effects() + self.character.rote_points + 3

        self.character.spend_xp(
            trait_name="",
            trait_display=trait,
            cost=cost,
            category="rotes",
            trait_value=new_value,
        )

        return XPSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} XP on Rote Points",
        )

    # =========================================================================
    # APPLIERS - Apply approved XP spending requests
    # =========================================================================

    @applier("sphere")
    def _apply_sphere(self, xp_request, approver) -> XPApplyResult:
        """Apply approved sphere XP spending."""
        from characters.models.mage.sphere import Sphere

        # Validate sphere rating doesn't exceed Arete
        if xp_request.trait_value > self.character.arete:
            return XPApplyResult(
                success=False,
                trait=xp_request.trait_name,
                message="",
                error=f"Sphere rating ({xp_request.trait_value}) cannot exceed Arete ({self.character.arete})",
            )

        s = Sphere.objects.get(name=xp_request.trait_name)
        setattr(self.character, s.property_name, xp_request.trait_value)
        self.character.save()

        # Mark as approved
        xp_request.approved = "Approved"
        xp_request.approved_by = approver
        xp_request.approved_at = timezone.now()
        xp_request.save()

        return XPApplyResult(
            success=True,
            trait=xp_request.trait_name,
            message=f"Approved {xp_request.trait_name} increase to {xp_request.trait_value}",
        )

    @applier("arete")
    def _apply_arete(self, xp_request, approver) -> XPApplyResult:
        """Apply approved Arete XP spending."""
        self.character.approve_xp_spend(xp_request.id, "arete", xp_request.trait_value, approver)
        return XPApplyResult(
            success=True,
            trait="Arete",
            message=f"Approved Arete increase to {xp_request.trait_value}",
        )

    @applier("practice")
    def _apply_practice(self, xp_request, approver) -> XPApplyResult:
        """Apply approved practice XP spending."""
        from characters.models.mage.focus import Practice

        practice = Practice.objects.get(name=xp_request.trait_name)
        self.character.add_practice(practice)

        # Mark as approved
        xp_request.approved = "Approved"
        xp_request.approved_by = approver
        xp_request.approved_at = timezone.now()
        xp_request.save()

        return XPApplyResult(
            success=True,
            trait=xp_request.trait_name,
            message=f"Approved practice {xp_request.trait_name}",
        )

    @applier("tenet")
    def _apply_tenet(self, xp_request, approver) -> XPApplyResult:
        """Apply approved tenet XP spending."""
        from characters.models.mage.focus import Tenet

        t = Tenet.objects.get(name=xp_request.trait_name)
        self.character.other_tenets.add(t)

        # Mark as approved
        xp_request.approved = "Approved"
        xp_request.approved_by = approver
        xp_request.approved_at = timezone.now()
        xp_request.save()

        return XPApplyResult(
            success=True,
            trait=xp_request.trait_name,
            message=f"Approved tenet {xp_request.trait_name}",
        )

    @applier("remove tenet")
    def _apply_remove_tenet(self, xp_request, approver) -> XPApplyResult:
        """Apply approved tenet removal XP spending."""
        from characters.models.mage.focus import Tenet

        # Remove "Remove " prefix if present
        tenet_name = xp_request.trait_name.replace("Remove ", "")
        tenet = Tenet.objects.get(name=tenet_name)

        if tenet in self.character.other_tenets.all():
            self.character.other_tenets.remove(tenet)
        else:
            # It's a primary tenet - find replacement from other_tenets
            replacement = self.character.other_tenets.filter(tenet_type=tenet.tenet_type).first()
            if replacement:
                if tenet.tenet_type == "met":
                    self.character.metaphysical_tenet = replacement
                elif tenet.tenet_type == "per":
                    self.character.personal_tenet = replacement
                elif tenet.tenet_type == "asc":
                    self.character.ascension_tenet = replacement
                self.character.other_tenets.remove(replacement)
        self.character.save()

        # Mark as approved
        xp_request.approved = "Approved"
        xp_request.approved_by = approver
        xp_request.approved_at = timezone.now()
        xp_request.save()

        return XPApplyResult(
            success=True,
            trait=xp_request.trait_name,
            message=f"Approved removal of tenet {tenet_name}",
        )

    @applier("resonance")
    def _apply_resonance(self, xp_request, approver) -> XPApplyResult:
        """Apply approved resonance XP spending."""
        # Parse resonance detail from trait_name like "Resonance (Dynamic)"
        trait_name = xp_request.trait_name
        if "(" in trait_name:
            resonance_detail = trait_name.split("(")[1].rstrip(")")
        else:
            resonance_detail = trait_name

        self.character.add_resonance(resonance_detail)

        # Mark as approved
        xp_request.approved = "Approved"
        xp_request.approved_by = approver
        xp_request.approved_at = timezone.now()
        xp_request.save()

        return XPApplyResult(
            success=True,
            trait=trait_name,
            message=f"Approved resonance {resonance_detail}",
        )

    @applier("rotes")
    def _apply_rotes(self, xp_request, approver) -> XPApplyResult:
        """Apply approved rote points XP spending."""
        self.character.rote_points += 3
        self.character.save()

        # Mark as approved
        xp_request.approved = "Approved"
        xp_request.approved_by = approver
        xp_request.approved_at = timezone.now()
        xp_request.save()

        return XPApplyResult(
            success=True,
            trait="Rote Points",
            message="Approved 3 rote points",
        )


class SorcererXPSpendingService(MtAHumanXPSpendingService):
    """
    XP spending service for Sorcerer characters.

    Sorcerers use linear magic with Paths and Rituals,
    NOT Spheres or Arete like Awakened mages.
    """

    @handler("Path")
    def _handle_path(self, example, **kwargs) -> XPSpendResult:
        """Handle sorcerer path XP spending."""
        trait = example.name
        current_value = self.character.path_rating(example)
        new_value = current_value + 1

        # Calculate cost: new=10, existing=7×current
        if current_value == 0:
            cost = get_xp_cost("new_path")
        else:
            cost = get_xp_cost("path") * current_value

        self.character.spend_xp(
            trait_name="",
            trait_display=trait,
            cost=cost,
            category="path",
            trait_value=new_value,
        )

        return XPSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} XP on {trait}",
        )

    @handler("Ritual")
    def _handle_ritual(self, example, **kwargs) -> XPSpendResult:
        """Handle sorcerer ritual XP spending."""
        trait = example.name
        # Cost is 2 × ritual level
        cost = get_xp_cost("ritual") * example.level

        self.character.spend_xp(
            trait_name="",
            trait_display=trait,
            cost=cost,
            category="ritual",
            trait_value=example.level,
        )

        return XPSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} XP on ritual {trait}",
        )

    # =========================================================================
    # APPLIERS - Apply approved XP spending requests
    # =========================================================================

    @applier("path")
    def _apply_path(self, xp_request, approver) -> XPApplyResult:
        """Apply approved sorcerer path XP spending."""
        from characters.models.mage.sorcerer import LinearMagicPath, PathRating

        path = LinearMagicPath.objects.get(name=xp_request.trait_name)
        pr, created = PathRating.objects.get_or_create(
            character=self.character,
            path=path,
            defaults={"rating": 0},
        )
        pr.rating = xp_request.trait_value
        pr.save()

        # Mark as approved
        xp_request.approved = "Approved"
        xp_request.approved_by = approver
        xp_request.approved_at = timezone.now()
        xp_request.save()

        return XPApplyResult(
            success=True,
            trait=xp_request.trait_name,
            message=f"Approved {xp_request.trait_name} increase to {xp_request.trait_value}",
        )

    @applier("ritual")
    def _apply_ritual(self, xp_request, approver) -> XPApplyResult:
        """Apply approved sorcerer ritual XP spending."""
        from characters.models.mage.sorcerer import LinearMagicRitual

        ritual = LinearMagicRitual.objects.get(name=xp_request.trait_name)
        self.character.rituals.add(ritual)

        # Mark as approved
        xp_request.approved = "Approved"
        xp_request.approved_by = approver
        xp_request.approved_at = timezone.now()
        xp_request.save()

        return XPApplyResult(
            success=True,
            trait=xp_request.trait_name,
            message=f"Approved ritual {xp_request.trait_name}",
        )


class CompanionXPSpendingService(MtAHumanXPSpendingService):
    """
    XP spending service for Companion (Consor) characters.

    Companions are unawakened helpers to mages. They have access
    to standard human traits plus Special Advantages and Charms.
    """

    @handler("Advantage")
    def _handle_advantage(self, example, value=None, **kwargs) -> XPSpendResult:
        """Handle Special Advantage XP spending."""
        trait = example.name
        current_value = self.character.advantage_rating(example)
        new_value = value if value is not None else current_value + 1

        # Advantage cost: 3 per rating difference
        cost = get_xp_cost("advantage") * abs(new_value - current_value)

        self.character.spend_xp(
            trait_name="",
            trait_display=trait,
            cost=cost,
            category="advantage",
            trait_value=new_value,
        )

        return XPSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} XP on {trait}",
        )

    @handler("Charm")
    def _handle_charm(self, example, **kwargs) -> XPSpendResult:
        """Handle Spirit Charm XP spending."""
        trait = example.name
        cost = get_xp_cost("charm")

        self.character.spend_xp(
            trait_name="",
            trait_display=trait,
            cost=cost,
            category="charm",
            trait_value=1,
        )

        return XPSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} XP on Charm: {trait}",
        )

    # =========================================================================
    # APPLIERS - Apply approved XP spending requests
    # =========================================================================

    @applier("advantage")
    def _apply_advantage(self, xp_request, approver) -> XPApplyResult:
        """Apply approved Special Advantage XP spending."""
        from characters.models.mage.companion import Advantage, AdvantageRating

        advantage = Advantage.objects.get(name=xp_request.trait_name)
        ar, created = AdvantageRating.objects.get_or_create(
            character=self.character,
            advantage=advantage,
            defaults={"rating": 0},
        )
        ar.rating = xp_request.trait_value
        ar.save()

        # Mark as approved
        xp_request.approved = "Approved"
        xp_request.approved_by = approver
        xp_request.approved_at = timezone.now()
        xp_request.save()

        return XPApplyResult(
            success=True,
            trait=xp_request.trait_name,
            message=f"Approved {xp_request.trait_name} increase to {xp_request.trait_value}",
        )

    @applier("charm")
    def _apply_charm(self, xp_request, approver) -> XPApplyResult:
        """Apply approved Spirit Charm XP spending."""
        from characters.models.werewolf.charm import SpiritCharm

        charm = SpiritCharm.objects.get(name=xp_request.trait_name)
        self.character.charms.add(charm)

        # Mark as approved
        xp_request.approved = "Approved"
        xp_request.approved_by = approver
        xp_request.approved_at = timezone.now()
        xp_request.save()

        return XPApplyResult(
            success=True,
            trait=xp_request.trait_name,
            message=f"Approved Charm: {xp_request.trait_name}",
        )


# Register Mage gameline character types
XPSpendingServiceFactory.register("mta_human", MtAHumanXPSpendingService)
XPSpendingServiceFactory.register("mage", MageXPSpendingService)
XPSpendingServiceFactory.register("sorcerer", SorcererXPSpendingService)
XPSpendingServiceFactory.register("companion", CompanionXPSpendingService)
