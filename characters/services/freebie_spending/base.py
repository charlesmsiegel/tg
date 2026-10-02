"""
Freebie Spending Service base classes and infrastructure.

This module provides the core architecture for freebie spending operations,
including the metaclass for handler inheritance, factory pattern, and
the base HumanFreebieSpendingService with common handlers.

Mirrors the XP spending service architecture but for freebie point spending
during character creation.
"""

import logging
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any

from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from characters.costs import get_freebie_cost, get_meritflaw_freebie_cost
from characters.models.core.ability_block import Ability
from characters.models.core.attribute_block import Attribute
from characters.models.core.background_block import Background, BackgroundRating
from characters.models.core.merit_flaw_block import MeritFlaw
from game.models import FreebieSpendingRecord

logger = logging.getLogger(__name__)


class FreebieRevertError(Exception):
    """A denial's revert could not be performed; ``deny()`` rolls back and reports it."""


@dataclass
class FreebieSpendResult:
    """Result of a freebie spending operation."""

    success: bool
    trait: str
    cost: int
    message: str
    error: str | None = None


@dataclass
class FreebieApplyResult:
    """Result of applying or denying a freebie spending request."""

    success: bool
    trait: str
    message: str
    error: str | None = None


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
        value: int | None = None,
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
            with transaction.atomic():
                return handler_method(
                    example=example, value=value, note=note, pooled=pooled, **kwargs
                )
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
        Deny a freebie spending request: revert the trait, refund the cost, mark Denied.

        The three writes run in one transaction (a savepoint inside the caller's, which
        ``decide_spending_request`` opens with the record and character locked). A revert
        that fails, raises, or has no applier registered for the record's trait type rolls
        everything back and returns a failed result, so the record stays ``Pending``, the
        cost stays deducted and the caller raises instead of reporting success. A failed
        denial also reloads ``self.character`` from the database, so callers must not
        hold unsaved changes on that instance.

        Args:
            freebie_request: FreebieSpendingRecord instance to deny
            denier: User denying the request

        Returns:
            FreebieApplyResult with success/failure info
        """
        trait_name = freebie_request.trait_name
        trait_type = freebie_request.trait_type

        applier_name = self._appliers.get(trait_type)
        applier_method = getattr(self, applier_name, None) if applier_name else None
        if applier_method is None:
            logger.error(
                "No freebie revert registered for trait type %r (record %s, character %s)",
                trait_type,
                freebie_request.pk,
                self.character.pk,
            )
            return FreebieApplyResult(
                success=False,
                trait=trait_name,
                message="",
                error=f"Cannot revert {trait_name}: no revert is registered for {trait_type!r} spends",
            )

        try:
            with transaction.atomic():
                reverted = applier_method(
                    freebie_request=freebie_request, approver=denier, deny=True
                )
                if not reverted.success:
                    raise FreebieRevertError(reverted.error or f"Could not revert {trait_name}")

                self.character.freebies += freebie_request.cost
                self.character.save()

                freebie_request.approved = "Denied"
                freebie_request.approved_by = denier
                freebie_request.approved_at = timezone.now()
                freebie_request.save()
        except FreebieRevertError as exc:
            logger.warning(
                "Freebie denial of %s (record %s, character %s) refused: %s",
                trait_name,
                freebie_request.pk,
                self.character.pk,
                exc,
            )
            self.character.refresh_from_db()
            return FreebieApplyResult(success=False, trait=trait_name, message="", error=str(exc))
        except Exception as exc:
            logger.exception(
                "Freebie denial of %s (record %s, character %s) failed",
                trait_name,
                freebie_request.pk,
                self.character.pk,
            )
            # The savepoint restored the row; drop whatever the applier set in memory.
            self.character.refresh_from_db()
            return FreebieApplyResult(success=False, trait=trait_name, message="", error=str(exc))

        return FreebieApplyResult(
            success=True,
            trait=trait_name,
            message=f"{reverted.message}; refunded {freebie_request.cost} freebies",
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

    # ------------------------------------------------------------------
    # Record-driven reverts, shared by the ``deny=True`` branch of appliers
    # ------------------------------------------------------------------

    @staticmethod
    def _revert_refused(trait_name: str, error: str) -> FreebieApplyResult:
        return FreebieApplyResult(success=False, trait=trait_name, message="", error=error)

    def _revert_column(
        self, freebie_request, property_name: str, *, step: int = 1, mirror: tuple[str, ...] = ()
    ) -> FreebieApplyResult:
        """Set an integer trait column back to the value before the recorded spend.

        The record's ``trait_value`` is the value the spend set, so the value before it
        is ``trait_value - step`` (``step`` is negative for a spend that lowers a trait,
        such as a Banality reduction). The revert refuses when the column no longer holds
        ``trait_value``: the player raised the trait again, or something else changed it,
        and undoing that later change would not be this spend's reversal. ``mirror``
        names columns kept equal to the trait (a temporary pool).
        """
        trait_name = freebie_request.trait_name
        if not hasattr(self.character, property_name):
            return self._revert_refused(
                trait_name, f"{self.character.name} has no {property_name} trait to revert"
            )
        current = getattr(self.character, property_name)
        expected = freebie_request.trait_value
        if current != expected:
            return self._revert_refused(
                trait_name,
                f"{trait_name} is {current}, not the {expected} this spend set. Deny any "
                f"later spend on {trait_name} first, or correct it by hand",
            )
        restored = expected - step
        setattr(self.character, property_name, restored)
        for name in mirror:
            setattr(self.character, name, restored)
        self.character.save()
        return FreebieApplyResult(
            success=True,
            trait=trait_name,
            message=f"Denied and reverted {trait_name} to {restored}",
        )

    def _revert_catalogue_column(self, freebie_request, model, **kwargs) -> FreebieApplyResult:
        """Revert a column named by a catalogue row (``Attribute``, ``Sphere``, ...)
        looked up by the record's display name; refuse when the row is missing or the
        name is ambiguous (catalogue names carry no unique constraint)."""
        trait_name = freebie_request.trait_name
        rows = list(model.objects.filter(name=trait_name)[:2])
        if not rows:
            return self._revert_refused(
                trait_name, f"No {model._meta.verbose_name} named {trait_name!r} to revert"
            )
        if len(rows) > 1:
            return self._revert_refused(
                trait_name,
                f"More than one {model._meta.verbose_name} is named {trait_name!r}; "
                "correct the trait by hand",
            )
        return self._revert_column(freebie_request, rows[0].property_name, **kwargs)

    def _revert_rating_row(self, freebie_request, row) -> FreebieApplyResult:
        """Revert a rating row (a background, practice or path rating) to the value
        before the recorded spend: delete the row the spend created (``trait_value``
        1), otherwise lower it by one. Refuse when the row is gone or no longer holds
        ``trait_value``."""
        trait_name = freebie_request.trait_name
        expected = freebie_request.trait_value
        if row is None:
            return self._revert_refused(
                trait_name, f"{self.character.name} no longer has {trait_name} to revert"
            )
        if row.rating != expected:
            return self._revert_refused(
                trait_name,
                f"{trait_name} is {row.rating}, not the {expected} this spend set. Deny any "
                f"later spend on {trait_name} first, or correct it by hand",
            )
        if expected <= 1:
            row.delete()
            return FreebieApplyResult(
                success=True, trait=trait_name, message=f"Denied and removed {trait_name}"
            )
        row.rating = expected - 1
        row.save()
        return FreebieApplyResult(
            success=True,
            trait=trait_name,
            message=f"Denied and reverted {trait_name} to {row.rating}",
        )

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
    @contextmanager
    def locked(cls, character):
        """Yield a service bound to a row-locked, freshly read ``character``.

        Opens a transaction and re-reads the character with
        ``select_for_update()`` so concurrent spends serialize and each sees
        the other's deduction. Views spend through this; unit tests may still
        build services around in-memory instances with ``get_service``.
        """
        with transaction.atomic():
            fresh = type(character).objects.select_for_update().get(pk=character.pk)
            yield cls.get_service(fresh)

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

    willpower_cost_multiplier = 1

    @handler("Attribute")
    def _handle_attribute(self, example, **kwargs) -> FreebieSpendResult:
        """Handle attribute freebie spending."""
        trait = example.name
        property_name = example.property_name
        current_value = getattr(self.character, property_name)
        new_value = current_value + 1
        cost = get_freebie_cost("attribute")

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
        cost = get_freebie_cost("ability")

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

    @handler("Background")
    def _handle_background(self, example, note="", pooled=False, **kwargs) -> FreebieSpendResult:
        """Handle background freebie spending.

        Automatically detects new vs existing background based on example type:
        - Background model = new background (create BackgroundRating)
        - BackgroundRating model = existing background (increase rating)
        """
        # Detect new vs existing based on example type
        is_new = isinstance(example, Background)

        if is_new:
            # New background - example is a Background model
            bg = example
            trait = bg.name + (f" ({note})" if note else "")
            new_value = 1
            base_cost = get_freebie_cost("background")
            multiplier = bg.multiplier if hasattr(bg, "multiplier") else 1
            cost = base_cost * multiplier

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
                bg=bg,
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
        else:
            # Existing background - example is a BackgroundRating model
            bg_rating = example
            trait = bg_rating.bg.name + (f" ({bg_rating.note})" if bg_rating.note else "")
            current_value = bg_rating.rating
            new_value = current_value + 1
            base_cost = get_freebie_cost("background")
            multiplier = bg_rating.bg.multiplier if hasattr(bg_rating.bg, "multiplier") else 1
            cost = base_cost * multiplier

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
            bg_rating.rating = new_value
            bg_rating.save()

            # Record and deduct
            self._record_spending(trait, "background", new_value, cost)
            self._deduct_freebies(cost)

            return FreebieSpendResult(
                success=True,
                trait=trait,
                cost=cost,
                message=f"Spent {cost} freebies on {trait}",
            )

    # Keep legacy handlers for backward compatibility during transition
    @handler("New Background")
    def _handle_new_background(
        self, example, note="", pooled=False, **kwargs
    ) -> FreebieSpendResult:
        """Legacy handler - redirects to unified Background handler."""
        return self._handle_background(example, note=note, pooled=pooled, **kwargs)

    @handler("Existing Background")
    def _handle_existing_background(self, example, **kwargs) -> FreebieSpendResult:
        """Legacy handler - redirects to unified Background handler."""
        return self._handle_background(example, **kwargs)

    @handler("Willpower")
    def _handle_willpower(self, **kwargs) -> FreebieSpendResult:
        """Handle willpower freebie spending."""
        trait = "Willpower"
        current_value = self.character.willpower
        new_value = current_value + 1
        cost = get_freebie_cost("willpower") * self.willpower_cost_multiplier

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
        """Handle merit/flaw freebie spending.

        Merit/flaw costs equal their rating. Flaws (negative ratings) grant
        freebies instead of costing them.
        """
        trait = example.name
        rating = value if value is not None else example.max_rating
        cost = get_meritflaw_freebie_cost(rating)  # abs(rating)

        # For flaws, cost is negative (grants freebies)
        if rating < 0:
            cost = rating  # Negative = gain freebies
            current_flaws = self.character.total_flaws()
            if current_flaws + rating < -7:
                return FreebieSpendResult(
                    success=False,
                    trait=trait,
                    cost=cost,
                    message="",
                    error="Would exceed maximum flaw limit of 7",
                )
        elif cost > self.character.freebies:
            return FreebieSpendResult(
                success=False,
                trait=trait,
                cost=cost,
                message="",
                error="Not enough freebies",
            )

        # Add the merit/flaw
        self.character.add_mf(example, rating)

        # Record and deduct (for flaws, this adds freebies)
        self._record_spending(trait, "meritflaw", rating, cost)
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
            return self._revert_catalogue_column(freebie_request, Attribute)

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
            return self._revert_catalogue_column(freebie_request, Ability)

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
        """Apply or deny new background freebie spending.

        The revert is driven by the record, which holds ``trait_value`` 1 for a background
        the spend created, so it shares ``_apply_background``: that deletes the rating row
        a new-background spend created and lowers one an existing-background spend raised.
        Going through the same method also keeps a gameline override of
        ``_apply_background`` (the Mage Avatar hook) in force for both spellings.
        """
        return self._apply_background(freebie_request, approver, deny=deny)

    @applier("background")
    def _apply_background(self, freebie_request, approver, deny=False) -> FreebieApplyResult:
        """Apply or deny background freebie spending (a new background or a raise)."""
        if deny:
            # The spend recorded ``"<background> (<note>)"``; strip exactly one closing
            # parenthesis so a note that ends in one survives.
            bg_name, _, note = freebie_request.trait_name.partition(" (")
            note = note.removesuffix(")")
            row = self.character.backgrounds.filter(bg__name=bg_name, note=note).first()
            return self._revert_rating_row(freebie_request, row)

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
            return self._revert_column(
                freebie_request, "willpower", mirror=("temporary_willpower",)
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
