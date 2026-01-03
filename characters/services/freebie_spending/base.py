"""
Freebie Spending Service base classes and infrastructure.

This module provides the core architecture for freebie spending operations,
including the metaclass for handler inheritance, factory pattern, and
the base HumanFreebieSpendingService with common handlers.

Mirrors the XP spending service architecture but for freebie point spending
during character creation.
"""

from dataclasses import dataclass
from typing import Any, Optional

from django.core.exceptions import ValidationError
from django.utils import timezone


@dataclass
class FreebieSpendResult:
    """Result of a freebie spending operation."""

    success: bool
    trait: str
    cost: int
    message: str
    error: Optional[str] = None


@dataclass
class FreebieApplyResult:
    """Result of applying or denying a freebie spending request."""

    success: bool
    trait: str
    message: str
    error: Optional[str] = None


def handler(category: str):
    """
    Decorator to register a method as a freebie spending handler for a category.

    Works with FreebieSpendingServiceMeta to properly register handlers per-class
    while supporting inheritance.

    Args:
        category: The category name this handler processes (e.g., "Attribute", "Ability")

    Returns:
        Decorator function that marks the method with its category
    """

    def decorator(func):
        func._freebie_handler_category = category
        return func

    return decorator


def applier(category: str):
    """
    Decorator to register a method as a freebie apply handler for a trait type.

    Works with FreebieSpendingServiceMeta to properly register appliers per-class
    while supporting inheritance. Used when approving/denying freebie spending requests.

    Args:
        category: The trait_type this applier processes (e.g., "attribute", "ability")
                  Must match the trait_type stored in FreebieSpendingRecord

    Returns:
        Decorator function that marks the method with its category
    """

    def decorator(func):
        func._freebie_applier_category = category
        return func

    return decorator


class FreebieSpendingServiceMeta(type):
    """
    Metaclass that ensures each subclass gets its own handler and applier registries
    with parent handlers/appliers inherited.

    This fixes the broken decorator pattern where decorators modified the base
    class dict instead of the subclass.
    """

    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)

        # Start with empty dicts for this class
        handlers = {}
        appliers = {}

        # Inherit handlers and appliers from parent classes
        for base in bases:
            if hasattr(base, "_handlers") and isinstance(base._handlers, dict):
                handlers.update(base._handlers)
            if hasattr(base, "_appliers") and isinstance(base._appliers, dict):
                appliers.update(base._appliers)

        # Register any methods decorated with @handler or @applier in this class
        for attr_name, attr_value in namespace.items():
            if hasattr(attr_value, "_freebie_handler_category"):
                handlers[attr_value._freebie_handler_category] = attr_name
            if hasattr(attr_value, "_freebie_applier_category"):
                appliers[attr_value._freebie_applier_category] = attr_name

        # Also check for handlers/appliers defined in the class after creation
        for attr_name in dir(cls):
            if attr_name.startswith("_"):
                try:
                    attr_value = getattr(cls, attr_name)
                    if hasattr(attr_value, "_freebie_handler_category"):
                        if attr_value._freebie_handler_category not in handlers:
                            handlers[attr_value._freebie_handler_category] = attr_name
                    if hasattr(attr_value, "_freebie_applier_category"):
                        if attr_value._freebie_applier_category not in appliers:
                            appliers[attr_value._freebie_applier_category] = attr_name
                except AttributeError:
                    pass

        cls._handlers = handlers
        cls._appliers = appliers
        return cls


class FreebieSpendingService(metaclass=FreebieSpendingServiceMeta):
    """
    Abstract base service class for freebie spending operations.

    Uses a handler registry pattern with proper inheritance support
    via the FreebieSpendingServiceMeta metaclass.

    Provides:
    - spend(): Create pending freebie spending records (trait applied immediately)
    - apply(): Approve freebie spending requests
    - deny(): Deny and refund freebie spending requests (reverts trait)
    """

    _handlers: dict[str, str] = {}
    _appliers: dict[str, str] = {}

    def __init__(self, character):
        """
        Initialize the service with a character.

        Args:
            character: The character spending freebies
        """
        self.character = character

    def spend(
        self,
        category: str,
        example: Any = None,
        value: Optional[int] = None,
        note: str = "",
        pooled: bool = False,
        **kwargs,
    ) -> FreebieSpendResult:
        """
        Spend freebies on a trait.

        Unlike XP spending, freebie spending applies the trait immediately
        (pending ST approval which can revert it).

        Args:
            category: The category of spending (e.g., "Attribute", "Ability")
            example: The trait object (Attribute, Ability, Sphere, etc.)
            value: Optional explicit value for the trait
            note: Optional note for backgrounds
            pooled: Whether background is pooled
            **kwargs: Additional arguments passed to handler

        Returns:
            FreebieSpendResult with success/failure info
        """
        handler_name = self._handlers.get(category)
        if handler_name is None:
            return FreebieSpendResult(
                success=False,
                trait="",
                cost=0,
                message="",
                error=f"Unknown freebie category: {category}",
            )

        handler_method = getattr(self, handler_name, None)
        if handler_method is None:
            return FreebieSpendResult(
                success=False,
                trait="",
                cost=0,
                message="",
                error=f"Handler not implemented: {handler_name}",
            )

        try:
            return handler_method(example=example, value=value, note=note, pooled=pooled, **kwargs)
        except ValidationError as e:
            return FreebieSpendResult(
                success=False,
                trait="",
                cost=0,
                message="",
                error=str(e),
            )

    def apply(self, freebie_request, approver) -> FreebieApplyResult:
        """
        Apply (approve) a freebie spending request.

        Since the trait is already applied during spend(), this just marks
        the record as approved.

        Args:
            freebie_request: FreebieSpendingRecord instance to approve
            approver: User approving the request

        Returns:
            FreebieApplyResult with success/failure info
        """
        trait_type = freebie_request.trait_type
        applier_name = self._appliers.get(trait_type)

        if applier_name is None:
            # Default approval - just mark as approved
            freebie_request.approved = "Approved"
            freebie_request.approved_by = approver
            freebie_request.approved_at = timezone.now()
            freebie_request.save()
            return FreebieApplyResult(
                success=True,
                trait=freebie_request.trait_name,
                message=f"Approved {freebie_request.trait_name}",
            )

        applier_method = getattr(self, applier_name, None)
        if applier_method is None:
            return FreebieApplyResult(
                success=False,
                trait=freebie_request.trait_name,
                message="",
                error=f"Applier not implemented: {applier_name}",
            )

        try:
            return applier_method(freebie_request=freebie_request, approver=approver)
        except Exception as e:
            return FreebieApplyResult(
                success=False,
                trait=freebie_request.trait_name,
                message="",
                error=str(e),
            )

    def deny(self, freebie_request, denier) -> FreebieApplyResult:
        """
        Deny a freebie spending request, refund freebies, and revert the trait.

        Args:
            freebie_request: FreebieSpendingRecord instance to deny
            denier: User denying the request

        Returns:
            FreebieApplyResult with success/failure info
        """
        trait_type = freebie_request.trait_type

        # Refund the freebie cost
        self.character.freebies += freebie_request.cost
        self.character.save()

        # Try to revert the trait using the applier's revert logic
        applier_name = self._appliers.get(trait_type)
        if applier_name:
            applier_method = getattr(self, applier_name, None)
            if applier_method:
                try:
                    # Call with deny=True to trigger revert logic
                    applier_method(freebie_request=freebie_request, approver=denier, deny=True)
                except Exception:
                    pass  # Best effort revert

        # Mark as denied
        freebie_request.approved = "Denied"
        freebie_request.approved_by = denier
        freebie_request.approved_at = timezone.now()
        freebie_request.save()

        return FreebieApplyResult(
            success=True,
            trait=freebie_request.trait_name,
            message=f"Denied and refunded {freebie_request.cost} freebies for {freebie_request.trait_name}",
        )

    def _record_spending(
        self,
        trait_name: str,
        trait_type: str,
        trait_value: int,
        cost: int,
    ):
        """
        Record freebie spending using the FreebieSpendingRecord model.

        Args:
            trait_name: Display name of the trait
            trait_type: Category type (attribute, ability, etc.)
            trait_value: Value gained
            cost: Freebie cost
        """
        from game.models import FreebieSpendingRecord

        FreebieSpendingRecord.objects.create(
            character=self.character,
            trait_name=trait_name,
            trait_type=trait_type,
            trait_value=trait_value,
            cost=cost,
        )

    def _deduct_freebies(self, cost: int):
        """Deduct freebies from character and save."""
        self.character.freebies -= cost
        self.character.save()

    @property
    def available_categories(self) -> list[str]:
        """Return list of freebie categories this service supports."""
        return list(self._handlers.keys())

    @property
    def available_appliers(self) -> list[str]:
        """Return list of trait types this service can apply."""
        return list(self._appliers.keys())


class FreebieSpendingServiceFactory:
    """
    Factory to get the correct freebie spending service for any character instance.

    Uses character.type to determine which service class to instantiate.
    """

    _service_map: dict[str, type[FreebieSpendingService]] = {}

    @classmethod
    def register(cls, character_type: str, service_class: type[FreebieSpendingService]):
        """
        Register a service class for a character type.

        Args:
            character_type: The character.type string (e.g., "mage", "vampire")
            service_class: The FreebieSpendingService subclass to use
        """
        cls._service_map[character_type] = service_class

    @classmethod
    def get_service(cls, character) -> FreebieSpendingService:
        """
        Get the appropriate freebie spending service for a character.

        Args:
            character: Any Character instance

        Returns:
            Appropriate FreebieSpendingService subclass instance
        """
        char_type = character.type
        service_class = cls._service_map.get(char_type, HumanFreebieSpendingService)
        return service_class(character)

    @classmethod
    def get_categories_for_character(cls, character) -> list[str]:
        """Get available freebie categories for a character type."""
        service = cls.get_service(character)
        return service.available_categories


class HumanFreebieSpendingService(FreebieSpendingService):
    """
    Freebie spending service for Human characters.

    Provides common handlers that all character types share:
    - Attribute
    - Ability
    - New Background
    - Existing Background
    - Willpower
    - MeritFlaw
    """

    @handler("Attribute")
    def _handle_attribute(self, example, **kwargs) -> FreebieSpendResult:
        """Handle attribute freebie spending."""
        trait = example.name
        property_name = example.property_name
        current_value = getattr(self.character, property_name)
        new_value = current_value + 1
        cost = self.character.freebie_cost("attribute")

        # Validate
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
                error="Attribute at maximum",
            )

        # Apply the change
        setattr(self.character, property_name, new_value)
        self.character.save()

        # Record and deduct
        self._record_spending(trait, "attribute", new_value, cost)
        self._deduct_freebies(cost)

        return FreebieSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} freebies on {trait}",
        )

    @handler("Ability")
    def _handle_ability(self, example, **kwargs) -> FreebieSpendResult:
        """Handle ability freebie spending."""
        trait = example.name
        property_name = example.property_name
        current_value = getattr(self.character, property_name)
        new_value = current_value + 1
        cost = self.character.freebie_cost("ability")

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
                error="Ability at maximum",
            )

        # Apply the change
        setattr(self.character, property_name, new_value)
        self.character.save()

        # Record and deduct
        self._record_spending(trait, "ability", new_value, cost)
        self._deduct_freebies(cost)

        return FreebieSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} freebies on {trait}",
        )

    @handler("New Background")
    def _handle_new_background(
        self, example, note="", pooled=False, **kwargs
    ) -> FreebieSpendResult:
        """Handle new background freebie spending."""
        from characters.models.core.background_block import BackgroundRating

        trait = example.name + (f" ({note})" if note else "")
        new_value = 1
        cost = example.multiplier if hasattr(example, "multiplier") else 1

        if cost > self.character.freebies:
            return FreebieSpendResult(
                success=False,
                trait=trait,
                cost=cost,
                message="",
                error="Not enough freebies",
            )

        # Create the background rating
        BackgroundRating.objects.create(
            char=self.character,
            bg=example,
            rating=new_value,
            note=note,
            pooled=pooled,
        )

        # Record and deduct
        self._record_spending(trait, "new-background", new_value, cost)
        self._deduct_freebies(cost)

        return FreebieSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} freebies on new background {trait}",
        )

    @handler("Existing Background")
    def _handle_existing_background(self, example, **kwargs) -> FreebieSpendResult:
        """Handle existing background freebie spending."""
        trait = example.bg.name + (f" ({example.note})" if example.note else "")
        current_value = example.rating
        new_value = current_value + 1
        cost = example.bg.multiplier if hasattr(example.bg, "multiplier") else 1

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
                error="Background at maximum",
            )

        # Apply the change
        example.rating = new_value
        example.save()

        # Record and deduct
        self._record_spending(trait, "background", new_value, cost)
        self._deduct_freebies(cost)

        return FreebieSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} freebies on {trait}",
        )

    @handler("Willpower")
    def _handle_willpower(self, **kwargs) -> FreebieSpendResult:
        """Handle willpower freebie spending."""
        trait = "Willpower"
        current_value = self.character.willpower
        new_value = current_value + 1
        cost = self.character.freebie_cost("willpower")

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
                error="Willpower at maximum",
            )

        # Apply the change
        self.character.willpower = new_value
        self.character.temporary_willpower = new_value
        self.character.save()

        # Record and deduct
        self._record_spending(trait, "willpower", new_value, cost)
        self._deduct_freebies(cost)

        return FreebieSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Spent {cost} freebies on Willpower",
        )

    @handler("MeritFlaw")
    def _handle_merit_flaw(self, example, value=None, **kwargs) -> FreebieSpendResult:
        """Handle merit/flaw freebie spending."""
        trait = example.name
        cost = value if value is not None else example.max_rating

        # Validate flaw limit
        if cost < 0:
            current_flaws = self.character.total_flaws()
            if current_flaws + cost < -7:
                return FreebieSpendResult(
                    success=False,
                    trait=trait,
                    cost=cost,
                    message="",
                    error="Would exceed maximum flaw limit of 7",
                )
            # Flaws give freebies (negative cost means gain)
        elif cost > self.character.freebies:
            return FreebieSpendResult(
                success=False,
                trait=trait,
                cost=cost,
                message="",
                error="Not enough freebies",
            )

        # Add the merit/flaw
        self.character.add_mf(example, cost)

        # Record and deduct
        self._record_spending(trait, "meritflaw", cost, cost)
        self._deduct_freebies(cost)

        return FreebieSpendResult(
            success=True,
            trait=trait,
            cost=cost,
            message=f"Added {trait} ({cost})",
        )

    # =========================================================================
    # APPLIERS - Apply/deny freebie spending requests
    # =========================================================================

    @applier("attribute")
    def _apply_attribute(self, freebie_request, approver, deny=False) -> FreebieApplyResult:
        """Apply or deny approved attribute freebie spending."""
        if deny:
            # Revert the attribute
            from characters.models.core.attribute_block import Attribute

            att = Attribute.objects.filter(name=freebie_request.trait_name).first()
            if att:
                current_val = getattr(self.character, att.property_name, 1)
                if current_val > 1:
                    setattr(self.character, att.property_name, current_val - 1)
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

    @applier("ability")
    def _apply_ability(self, freebie_request, approver, deny=False) -> FreebieApplyResult:
        """Apply or deny approved ability freebie spending."""
        if deny:
            # Revert the ability
            from characters.models.core.ability_block import Ability

            abb = Ability.objects.filter(name=freebie_request.trait_name).first()
            if abb:
                current_val = getattr(self.character, abb.property_name, 0)
                if current_val > 0:
                    setattr(self.character, abb.property_name, current_val - 1)
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

    @applier("new-background")
    def _apply_new_background(self, freebie_request, approver, deny=False) -> FreebieApplyResult:
        """Apply or deny new background freebie spending."""
        if deny:
            # Remove the background
            from characters.models.core.background_block import Background

            trait_name = freebie_request.trait_name
            if "(" in trait_name:
                bg_name, note = trait_name.split("(")
                note = note.rstrip(")").strip()
                bg_name = bg_name.strip()
            else:
                bg_name = trait_name.strip()
                note = ""

            bg = Background.objects.filter(name=bg_name).first()
            if bg:
                self.character.backgrounds.filter(bg=bg, note=note, rating=1).delete()

            return FreebieApplyResult(
                success=True,
                trait=freebie_request.trait_name,
                message=f"Denied and removed {freebie_request.trait_name}",
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

    @applier("background")
    def _apply_background(self, freebie_request, approver, deny=False) -> FreebieApplyResult:
        """Apply or deny existing background freebie spending."""
        if deny:
            # Reduce the background rating
            trait_name = freebie_request.trait_name
            if " (" in trait_name:
                bg_name, note = trait_name.split(" (")
                note = note.rstrip(")")
            else:
                bg_name = trait_name
                note = ""

            bgr = self.character.backgrounds.filter(bg__name=bg_name, note=note).first()
            if bgr and bgr.rating > 1:
                bgr.rating -= 1
                bgr.save()
            elif bgr and bgr.rating == 1:
                bgr.delete()

            return FreebieApplyResult(
                success=True,
                trait=trait_name,
                message=f"Denied and reverted {trait_name}",
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

    @applier("willpower")
    def _apply_willpower(self, freebie_request, approver, deny=False) -> FreebieApplyResult:
        """Apply or deny willpower freebie spending."""
        if deny:
            # Revert willpower
            if self.character.willpower > 1:
                self.character.willpower -= 1
                self.character.temporary_willpower = self.character.willpower
                self.character.save()
            return FreebieApplyResult(
                success=True,
                trait="Willpower",
                message="Denied and reverted Willpower",
            )

        # Mark as approved
        freebie_request.approved = "Approved"
        freebie_request.approved_by = approver
        freebie_request.approved_at = timezone.now()
        freebie_request.save()
        return FreebieApplyResult(
            success=True,
            trait="Willpower",
            message="Approved Willpower",
        )

    @applier("meritflaw")
    def _apply_meritflaw(self, freebie_request, approver, deny=False) -> FreebieApplyResult:
        """Apply or deny merit/flaw freebie spending."""
        if deny:
            # Remove the merit/flaw
            from characters.models.core.merit_flaw_block import MeritFlaw

            mf = MeritFlaw.objects.filter(name=freebie_request.trait_name).first()
            if mf:
                self.character.remove_mf(mf)
            return FreebieApplyResult(
                success=True,
                trait=freebie_request.trait_name,
                message=f"Denied and removed {freebie_request.trait_name}",
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


# Register base human type
FreebieSpendingServiceFactory.register("human", HumanFreebieSpendingService)
