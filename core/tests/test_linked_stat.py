"""
Tests for the LinkedStat system.

Tests cover:
1. LinkedStatAccessor - property access and manipulation methods
2. LinkedStat descriptor - model integration
3. linked_stat_constraints - database constraint generation
4. Template tags - rendering linked stats
"""

from unittest.mock import Mock

import pytest
from core.linked_stat import LinkedStat, LinkedStatAccessor, linked_stat_constraints
from django.db.models import CheckConstraint


class TestLinkedStatAccessor:
    """Tests for LinkedStatAccessor class."""

    def test_permanent_property(self):
        """Test reading permanent value."""
        instance = Mock()
        instance.willpower = 7
        instance.temporary_willpower = 5

        accessor = LinkedStatAccessor(instance, "willpower", "temporary_willpower")

        assert accessor.permanent == 7

    def test_temporary_property(self):
        """Test reading temporary value."""
        instance = Mock()
        instance.willpower = 7
        instance.temporary_willpower = 5

        accessor = LinkedStatAccessor(instance, "willpower", "temporary_willpower")

        assert accessor.temporary == 5

    def test_permanent_setter_caps_temporary(self):
        """Test that setting permanent caps temporary if cap_temporary=True."""
        instance = Mock()
        instance.willpower = 7
        instance.temporary_willpower = 7

        accessor = LinkedStatAccessor(
            instance, "willpower", "temporary_willpower", cap_temporary=True
        )

        # Lower permanent below current temporary
        accessor.permanent = 5

        # Should have set willpower to 5 and capped temporary
        assert instance.willpower == 5
        assert instance.temporary_willpower == 5

    def test_permanent_setter_no_cap(self):
        """Test that setting permanent doesn't cap temporary if cap_temporary=False."""
        instance = Mock()
        instance.willpower = 7
        instance.temporary_willpower = 7

        accessor = LinkedStatAccessor(
            instance, "willpower", "temporary_willpower", cap_temporary=False
        )

        # Lower permanent below current temporary
        accessor.permanent = 5

        # Should only change permanent, not temporary
        assert instance.willpower == 5
        # temporary_willpower should not be modified in this call
        # (The accessor checks instance.temporary_willpower which is still 7)

    def test_temporary_setter_respects_cap(self):
        """Test that setting temporary respects the permanent cap."""
        instance = Mock()
        instance.willpower = 5
        instance.temporary_willpower = 3

        accessor = LinkedStatAccessor(
            instance, "willpower", "temporary_willpower", cap_temporary=True
        )

        # Try to set temporary above permanent
        accessor.temporary = 10

        # Should cap at permanent value
        assert instance.temporary_willpower == 5

    def test_temporary_setter_respects_minimum(self):
        """Test that setting temporary respects minimum value."""
        instance = Mock()
        instance.willpower = 5
        instance.temporary_willpower = 3

        accessor = LinkedStatAccessor(instance, "willpower", "temporary_willpower", min_temporary=0)

        # Try to set temporary below minimum
        accessor.temporary = -5

        # Should cap at minimum
        assert instance.temporary_willpower == 0

    def test_spend_success(self):
        """Test successful spending."""
        instance = Mock()
        instance.willpower = 7
        instance.temporary_willpower = 5

        accessor = LinkedStatAccessor(instance, "willpower", "temporary_willpower")

        result = accessor.spend(2)

        assert result is True
        assert instance.temporary_willpower == 3

    def test_spend_failure_insufficient(self):
        """Test spending failure when insufficient points."""
        instance = Mock()
        instance.willpower = 7
        instance.temporary_willpower = 1

        accessor = LinkedStatAccessor(instance, "willpower", "temporary_willpower")

        result = accessor.spend(5)

        assert result is False
        # Value should not change
        assert instance.temporary_willpower == 1

    def test_restore(self):
        """Test restoring temporary points."""
        instance = Mock()
        instance.willpower = 7
        instance.temporary_willpower = 3

        accessor = LinkedStatAccessor(
            instance, "willpower", "temporary_willpower", cap_temporary=True
        )

        restored = accessor.restore(2)

        assert restored == 2
        assert instance.temporary_willpower == 5

    def test_restore_caps_at_permanent(self):
        """Test that restore respects permanent cap."""
        instance = Mock()
        instance.willpower = 7
        instance.temporary_willpower = 5

        accessor = LinkedStatAccessor(
            instance, "willpower", "temporary_willpower", cap_temporary=True
        )

        # Try to restore more than available
        restored = accessor.restore(10)

        assert restored == 2  # Only 2 points were actually restored
        assert instance.temporary_willpower == 7

    def test_restore_full(self):
        """Test full restoration."""
        instance = Mock()
        instance.willpower = 7
        instance.temporary_willpower = 2

        accessor = LinkedStatAccessor(
            instance, "willpower", "temporary_willpower", cap_temporary=True
        )

        restored = accessor.restore_full()

        assert restored == 5
        assert instance.temporary_willpower == 7

    def test_is_full(self):
        """Test is_full property."""
        instance = Mock()

        # Full
        instance.willpower = 7
        instance.temporary_willpower = 7
        accessor = LinkedStatAccessor(instance, "willpower", "temporary_willpower")
        assert accessor.is_full is True

        # Not full
        instance.temporary_willpower = 5
        assert accessor.is_full is False

    def test_is_depleted(self):
        """Test is_depleted property."""
        instance = Mock()

        # Not depleted
        instance.willpower = 7
        instance.temporary_willpower = 3
        accessor = LinkedStatAccessor(instance, "willpower", "temporary_willpower", min_temporary=0)
        assert accessor.is_depleted is False

        # Depleted
        instance.temporary_willpower = 0
        assert accessor.is_depleted is True

    def test_spent_property(self):
        """Test spent property calculation."""
        instance = Mock()
        instance.willpower = 7
        instance.temporary_willpower = 3

        accessor = LinkedStatAccessor(instance, "willpower", "temporary_willpower")

        assert accessor.spent == 4

    def test_can_spend(self):
        """Test can_spend method."""
        instance = Mock()
        instance.willpower = 7
        instance.temporary_willpower = 3

        accessor = LinkedStatAccessor(instance, "willpower", "temporary_willpower")

        assert accessor.can_spend(1) is True
        assert accessor.can_spend(3) is True
        assert accessor.can_spend(4) is False

    def test_str_representation(self):
        """Test string representation."""
        instance = Mock()
        instance.willpower = 7
        instance.temporary_willpower = 3

        accessor = LinkedStatAccessor(instance, "willpower", "temporary_willpower")

        assert str(accessor) == "3/7"

    def test_int_conversion(self):
        """Test integer conversion returns temporary."""
        instance = Mock()
        instance.willpower = 7
        instance.temporary_willpower = 3

        accessor = LinkedStatAccessor(instance, "willpower", "temporary_willpower")

        assert int(accessor) == 3

    def test_bool_conversion(self):
        """Test boolean conversion."""
        instance = Mock()
        instance.willpower = 7

        accessor = LinkedStatAccessor(instance, "willpower", "temporary_willpower")

        # Has points
        instance.temporary_willpower = 3
        assert bool(accessor) is True

        # Depleted
        instance.temporary_willpower = 0
        assert bool(accessor) is False

    def test_max_and_current_aliases(self):
        """Test max and current aliases."""
        instance = Mock()
        instance.willpower = 7
        instance.temporary_willpower = 3

        accessor = LinkedStatAccessor(instance, "willpower", "temporary_willpower")

        assert accessor.max == 7
        assert accessor.current == 3

        # Test setter
        accessor.current = 5
        assert instance.temporary_willpower == 5


class TestLinkedStatDescriptor:
    """Tests for LinkedStat descriptor."""

    def test_class_level_access(self):
        """Test that class-level access returns the descriptor."""

        class TestModel:
            willpower = 7
            temporary_willpower = 5
            willpower_stat = LinkedStat("willpower", "temporary_willpower")

        # Class-level access should return descriptor
        assert isinstance(TestModel.willpower_stat, LinkedStat)

    def test_instance_access(self):
        """Test that instance access returns LinkedStatAccessor."""

        class TestModel:
            def __init__(self):
                self.willpower = 7
                self.temporary_willpower = 5

            willpower_stat = LinkedStat("willpower", "temporary_willpower")

        instance = TestModel()

        # Instance access should return accessor
        accessor = instance.willpower_stat
        assert isinstance(accessor, LinkedStatAccessor)
        assert accessor.permanent == 7
        assert accessor.temporary == 5

    def test_descriptor_assignment(self):
        """Test that assignment through descriptor sets permanent."""

        class TestModel:
            def __init__(self):
                self.willpower = 7
                self.temporary_willpower = 7

            willpower_stat = LinkedStat("willpower", "temporary_willpower")

        instance = TestModel()
        instance.willpower_stat = 5

        assert instance.willpower == 5
        assert instance.temporary_willpower == 5  # Capped


class TestLinkedStatConstraints:
    """Tests for linked_stat_constraints function."""

    def test_generates_three_constraints_when_capped(self):
        """Test that function generates 3 constraints when cap_temporary=True."""
        constraints = linked_stat_constraints(
            "willpower",
            "temporary_willpower",
            cap_temporary=True,
            constraint_prefix="test_",
        )

        assert len(constraints) == 3
        assert all(isinstance(c, CheckConstraint) for c in constraints)

    def test_generates_two_constraints_when_not_capped(self):
        """Test that function generates 2 constraints when cap_temporary=False."""
        constraints = linked_stat_constraints(
            "willpower",
            "temporary_willpower",
            cap_temporary=False,
            constraint_prefix="test_",
        )

        assert len(constraints) == 2

    def test_constraint_names(self):
        """Test that constraints have correct names."""
        constraints = linked_stat_constraints(
            "willpower",
            "temporary_willpower",
            cap_temporary=True,
            constraint_prefix="characters_human_",
        )

        names = [c.name for c in constraints]

        assert "characters_human_willpower_range" in names
        assert "characters_human_temporary_willpower_range" in names
        assert "characters_human_temporary_willpower_not_exceeds_perm" in names

    def test_custom_min_max_values(self):
        """Test constraints with custom min/max values."""
        constraints = linked_stat_constraints(
            "blood_pool",
            "max_blood_pool",
            min_permanent=1,
            max_permanent=50,
            min_temporary=0,
            max_temporary=50,
            cap_temporary=False,
            constraint_prefix="vamp_",
        )

        assert len(constraints) == 2


class TestLinkedStatTemplateFilters:
    """Tests for linked stat template filters."""

    def test_linked_dots_with_accessor(self):
        """Test linked_dots filter with LinkedStatAccessor."""
        from core.templatetags.dots import linked_dots

        instance = Mock()
        instance.willpower = 7
        instance.temporary_willpower = 5

        accessor = LinkedStatAccessor(instance, "willpower", "temporary_willpower")

        result = linked_dots(accessor, 10)

        assert "●●●●●●●○○○" in result  # Permanent dots
        assert "■■■■■□□□□□" in result  # Temporary boxes

    def test_linked_dots_with_tuple(self):
        """Test linked_dots filter with tuple."""
        from core.templatetags.dots import linked_dots

        result = linked_dots((7, 5), 10)

        assert "●●●●●●●○○○" in result
        assert "■■■■■□□□□□" in result

    def test_linked_dots_with_dict(self):
        """Test linked_dots filter with dict."""
        from core.templatetags.dots import linked_dots

        result = linked_dots({"permanent": 7, "temporary": 5}, 10)

        assert "●●●●●●●○○○" in result
        assert "■■■■■□□□□□" in result


class TestLinkedStatIntegration:
    """Integration tests for the LinkedStat system."""

    def test_full_workflow(self):
        """Test a complete workflow: create, spend, restore."""

        class Character:
            def __init__(self):
                self.willpower = 7
                self.temporary_willpower = 7

            willpower_stat = LinkedStat("willpower", "temporary_willpower")

        char = Character()

        # Initial state
        assert char.willpower_stat.permanent == 7
        assert char.willpower_stat.temporary == 7
        assert char.willpower_stat.is_full

        # Spend some points
        assert char.willpower_stat.spend(3) is True
        assert char.willpower_stat.temporary == 4
        assert char.willpower_stat.spent == 3
        assert not char.willpower_stat.is_full

        # Try to spend too many
        assert char.willpower_stat.spend(5) is False
        assert char.willpower_stat.temporary == 4  # Unchanged

        # Restore some
        restored = char.willpower_stat.restore(2)
        assert restored == 2
        assert char.willpower_stat.temporary == 6

        # Restore full
        char.willpower_stat.restore_full()
        assert char.willpower_stat.is_full
        assert char.willpower_stat.temporary == 7

    def test_blood_pool_pattern(self):
        """Test the max/current pattern used for blood pool."""

        class Vampire:
            def __init__(self):
                self.max_blood_pool = 10
                self.blood_pool = 10

            blood = LinkedStat("max_blood_pool", "blood_pool")

        vamp = Vampire()

        # Use blood
        vamp.blood.spend(3)
        assert vamp.blood_pool == 7
        assert vamp.blood.current == 7
        assert vamp.blood.max == 10

        # Feed
        vamp.blood.restore(5)
        assert vamp.blood_pool == 10  # Capped at max
