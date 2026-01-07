"""
Linked Stat System for World of Darkness Character Sheets

This module provides a consistent pattern for handling paired permanent/temporary
stats common in WoD games, such as:
- Willpower (permanent rating vs temporary points)
- Blood Pool (max capacity vs current blood)
- Gnosis (permanent vs temporary)
- Renown (permanent vs temporary glory/honor/wisdom)
- Pathos/Angst (permanent vs current)

Components:
1. LinkedStat - Descriptor for clean model access
2. linked_stat_fields() - Factory to create both fields + descriptor together
3. linked_stat_constraints() - Generates CheckConstraints for validation
4. LinkedStatAccessor - Provides spend/restore/query methods
"""

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import CheckConstraint, F, Q


class LinkedStatFields:
    """
    Container for linked stat field definitions.

    Holds the permanent field, temporary field, descriptor, and constraints
    for a linked stat pair. Use with linked_stat_fields() factory function.

    Usage:
        wp = linked_stat_fields('willpower', default=3, min_permanent=1)

        class Human(Character):
            willpower = wp.permanent
            temporary_willpower = wp.temporary
            willpower_stat = wp.descriptor

            class Meta:
                constraints = [*wp.constraints('characters_human_')]
    """

    def __init__(
        self,
        name,
        permanent_field,
        temporary_field,
        descriptor,
        *,
        cap_temporary=True,
        min_permanent=0,
        max_permanent=10,
        min_temporary=0,
        max_temporary=10,
    ):
        self.name = name
        self.permanent = permanent_field
        self.temporary = temporary_field
        self.descriptor = descriptor
        self._cap_temporary = cap_temporary
        self._min_permanent = min_permanent
        self._max_permanent = max_permanent
        self._min_temporary = min_temporary
        self._max_temporary = max_temporary
        # Store field names for constraint generation
        self._permanent_name = name
        self._temporary_name = f"temporary_{name}"

    def constraints(self, prefix=""):
        """
        Generate CheckConstraints for this linked stat.

        Args:
            prefix: Constraint name prefix (e.g., 'characters_human_')

        Returns:
            list: List of CheckConstraint objects
        """
        return linked_stat_constraints(
            self._permanent_name,
            self._temporary_name,
            cap_temporary=self._cap_temporary,
            min_permanent=self._min_permanent,
            max_permanent=self._max_permanent,
            min_temporary=self._min_temporary,
            max_temporary=self._max_temporary,
            constraint_prefix=prefix,
        )


def linked_stat_fields(
    name,
    *,
    default=0,
    min_permanent=0,
    max_permanent=10,
    min_temporary=0,
    max_temporary=10,
    cap_temporary=True,
    temporary_default=None,
):
    """
    Factory function to create a complete linked stat (both fields + descriptor).

    Creates:
    - permanent field: {name}
    - temporary field: temporary_{name}
    - descriptor: {name}_stat

    Args:
        name: Base name for the stat (e.g., 'willpower')
        default: Default value for both fields (default 0)
        min_permanent: Minimum permanent value (default 0)
        max_permanent: Maximum permanent value (default 10)
        min_temporary: Minimum temporary value (default 0)
        max_temporary: Maximum temporary value (default 10)
        cap_temporary: Whether temporary is capped at permanent (default True)
        temporary_default: Default for temporary if different from permanent (default None = same as default)

    Returns:
        LinkedStatFields: Container with .permanent, .temporary, .descriptor attributes

    Usage:
        wp = linked_stat_fields('willpower', default=3, min_permanent=1)

        class Human(Character):
            willpower = wp.permanent
            temporary_willpower = wp.temporary
            willpower_stat = wp.descriptor

            class Meta:
                constraints = [*wp.constraints('characters_human_')]

    Or for blood pool style (max/current naming):
        blood = linked_stat_fields(
            'blood_pool',
            default=10,
            max_permanent=50,
            max_temporary=50,
        )

        class Vampire(Human):
            max_blood_pool = blood.permanent  # Note: you choose the field name
            blood_pool = blood.temporary
            blood = blood.descriptor
    """
    temp_default = temporary_default if temporary_default is not None else default

    # Create the permanent field
    permanent_field = models.IntegerField(
        default=default,
        validators=[
            MinValueValidator(min_permanent),
            MaxValueValidator(max_permanent),
        ],
    )

    # Create the temporary field
    temporary_field = models.IntegerField(
        default=temp_default,
        validators=[
            MinValueValidator(min_temporary),
            MaxValueValidator(max_temporary),
        ],
    )

    # Create the descriptor (field names will be set when assigned to model)
    # We use placeholder names that get overridden by actual assignment
    descriptor = LinkedStat(
        name,  # Will be the permanent field name
        f"temporary_{name}",  # Will be the temporary field name
        cap_temporary=cap_temporary,
        min_temporary=min_temporary,
    )

    return LinkedStatFields(
        name,
        permanent_field,
        temporary_field,
        descriptor,
        cap_temporary=cap_temporary,
        min_permanent=min_permanent,
        max_permanent=max_permanent,
        min_temporary=min_temporary,
        max_temporary=max_temporary,
    )


class LinkedStatAccessor:
    """
    Accessor object returned when accessing a LinkedStat descriptor.

    Provides methods for manipulating linked permanent/temporary stat pairs.

    Attributes:
        instance: The model instance
        permanent_field: Name of the permanent stat field
        temporary_field: Name of the temporary stat field
        cap_temporary: Whether temporary is capped at permanent value
        min_temporary: Minimum allowed temporary value (usually 0)
    """

    def __init__(
        self,
        instance,
        permanent_field,
        temporary_field,
        cap_temporary=True,
        min_temporary=0,
    ):
        self._instance = instance
        self._permanent_field = permanent_field
        self._temporary_field = temporary_field
        self._cap_temporary = cap_temporary
        self._min_temporary = min_temporary

    @property
    def permanent(self):
        """Get the permanent stat value."""
        return getattr(self._instance, self._permanent_field)

    @permanent.setter
    def permanent(self, value):
        """Set the permanent stat value. May adjust temporary if cap_temporary is True."""
        setattr(self._instance, self._permanent_field, value)
        if self._cap_temporary and self.temporary > value:
            setattr(self._instance, self._temporary_field, value)

    @property
    def temporary(self):
        """Get the temporary stat value."""
        return getattr(self._instance, self._temporary_field)

    @temporary.setter
    def temporary(self, value):
        """Set the temporary stat value, respecting caps."""
        if self._cap_temporary:
            value = min(value, self.permanent)
        value = max(value, self._min_temporary)
        setattr(self._instance, self._temporary_field, value)

    @property
    def max(self):
        """Alias for permanent - represents the maximum capacity."""
        return self.permanent

    @property
    def current(self):
        """Alias for temporary - represents the current value."""
        return self.temporary

    @current.setter
    def current(self, value):
        """Alias setter for temporary."""
        self.temporary = value

    @property
    def is_full(self):
        """Check if temporary equals permanent (fully restored)."""
        return self.temporary >= self.permanent

    @property
    def is_depleted(self):
        """Check if temporary is at minimum."""
        return self.temporary <= self._min_temporary

    @property
    def spent(self):
        """Get how many points have been spent (permanent - temporary)."""
        return max(0, self.permanent - self.temporary)

    @property
    def available(self):
        """Alias for temporary - how many points are available to spend."""
        return self.temporary

    def spend(self, amount=1):
        """
        Spend temporary points.

        Args:
            amount: Number of points to spend (default 1)

        Returns:
            True if spending was successful, False if insufficient points
        """
        if self.temporary < amount:
            return False
        self.temporary = self.temporary - amount
        return True

    def restore(self, amount=1):
        """
        Restore temporary points (up to permanent maximum if capped).

        Args:
            amount: Number of points to restore (default 1)

        Returns:
            int: Actual number of points restored
        """
        old_value = self.temporary
        if self._cap_temporary:
            new_value = min(self.temporary + amount, self.permanent)
        else:
            new_value = self.temporary + amount
        self.temporary = new_value
        return new_value - old_value

    def restore_full(self):
        """Fully restore temporary to permanent value (if capped)."""
        if self._cap_temporary:
            restored = self.permanent - self.temporary
            self.temporary = self.permanent
            return restored
        return 0

    def can_spend(self, amount=1):
        """Check if the character can spend a given amount."""
        return self.temporary >= amount

    def __repr__(self):
        return f"<LinkedStat {self._permanent_field}={self.permanent}/{self._temporary_field}={self.temporary}>"

    def __str__(self):
        return f"{self.temporary}/{self.permanent}"

    def __int__(self):
        """Integer conversion returns the temporary (current) value."""
        return self.temporary

    def __bool__(self):
        """Boolean conversion checks if there are any temporary points."""
        return self.temporary > 0


class LinkedStat:
    """
    Descriptor for linked permanent/temporary stat pairs.

    This descriptor provides a clean API for accessing and manipulating
    paired stats in WoD character models.

    Usage:
        class Human(Character):
            willpower = models.IntegerField(default=3)
            temporary_willpower = models.IntegerField(default=3)

            # Add the descriptor for clean access
            willpower_stat = LinkedStat('willpower', 'temporary_willpower')

        # Then use it:
        character.willpower_stat.permanent      # 7
        character.willpower_stat.temporary      # 5
        character.willpower_stat.spend(2)       # Returns True, temp becomes 3
        character.willpower_stat.restore_full() # Temp becomes 7

    Args:
        permanent_field: Name of the permanent stat field
        temporary_field: Name of the temporary stat field
        cap_temporary: Whether temporary should be capped at permanent (default True)
        min_temporary: Minimum value for temporary stat (default 0)
    """

    def __init__(
        self,
        permanent_field,
        temporary_field,
        cap_temporary=True,
        min_temporary=0,
    ):
        self.permanent_field = permanent_field
        self.temporary_field = temporary_field
        self.cap_temporary = cap_temporary
        self.min_temporary = min_temporary
        self.attr_name = None  # Set by __set_name__

    def __set_name__(self, owner, name):
        self.attr_name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            # Class-level access returns the descriptor itself
            return self
        return LinkedStatAccessor(
            obj,
            self.permanent_field,
            self.temporary_field,
            self.cap_temporary,
            self.min_temporary,
        )

    def __set__(self, obj, value):
        """
        Allow direct assignment to set the permanent value.

        Example:
            character.willpower_stat = 7
            # Sets willpower to 7, may cap temporary_willpower
        """
        accessor = self.__get__(obj, type(obj))
        accessor.permanent = value


def linked_stat_constraints(
    permanent_field,
    temporary_field,
    *,
    cap_temporary=True,
    min_permanent=0,
    max_permanent=10,
    min_temporary=0,
    max_temporary=10,
    constraint_prefix="",
):
    """
    Generate CheckConstraints for a linked stat pair.

    This function creates the database constraints to ensure data integrity
    for linked permanent/temporary stat pairs.

    Args:
        permanent_field: Name of the permanent stat field
        temporary_field: Name of the temporary stat field
        cap_temporary: Whether temporary should be <= permanent (default True)
        min_permanent: Minimum value for permanent stat (default 0)
        max_permanent: Maximum value for permanent stat (default 10)
        min_temporary: Minimum value for temporary stat (default 0)
        max_temporary: Maximum value for temporary stat (default 10)
        constraint_prefix: Prefix for constraint names (e.g., 'characters_vampire_')

    Returns:
        list: List of CheckConstraint objects

    Usage:
        class Meta:
            constraints = [
                *linked_stat_constraints(
                    'willpower', 'temporary_willpower',
                    constraint_prefix='characters_human_',
                ),
            ]
    """
    constraints = []

    # Permanent value range constraint
    constraints.append(
        CheckConstraint(
            check=Q(**{f"{permanent_field}__gte": min_permanent})
            & Q(**{f"{permanent_field}__lte": max_permanent}),
            name=f"{constraint_prefix}{permanent_field}_range",
            violation_error_message=f"{permanent_field.replace('_', ' ').title()} must be between {min_permanent} and {max_permanent}",
        )
    )

    # Temporary value range constraint
    constraints.append(
        CheckConstraint(
            check=Q(**{f"{temporary_field}__gte": min_temporary})
            & Q(**{f"{temporary_field}__lte": max_temporary}),
            name=f"{constraint_prefix}{temporary_field}_range",
            violation_error_message=f"{temporary_field.replace('_', ' ').title()} must be between {min_temporary} and {max_temporary}",
        )
    )

    # Temporary <= Permanent constraint (if capped)
    if cap_temporary:
        constraints.append(
            CheckConstraint(
                check=Q(**{f"{temporary_field}__lte": F(permanent_field)}),
                name=f"{constraint_prefix}{temporary_field}_not_exceeds_perm",
                violation_error_message=f"{temporary_field.replace('_', ' ').title()} cannot exceed {permanent_field.replace('_', ' ')}",
            )
        )

    return constraints


# Convenience aliases for different naming conventions
class MaxCurrentStat(LinkedStat):
    """
    LinkedStat variant for max/current naming (e.g., max_blood_pool/blood_pool).

    The "permanent" value is the max, and "temporary" is current.
    """

    pass


class PermanentTemporaryStat(LinkedStat):
    """
    LinkedStat variant for permanent/temporary naming (standard WoD pattern).

    This is identical to LinkedStat but makes the naming convention explicit.
    """

    pass
