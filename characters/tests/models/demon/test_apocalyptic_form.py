"""Tests for ApocalypticForm and ApocalypticFormTrait models."""

from characters.models.demon.apocalyptic_form import (
    ApocalypticForm,
    ApocalypticFormTrait,
)
from characters.models.demon.house import DemonHouse
from django.contrib.auth.models import User
from django.test import TestCase


class ApocalypticFormTraitModelTests(TestCase):
    """Tests for ApocalypticFormTrait model functionality."""

    def setUp(self):
        """Create a test user for ownership."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.trait = ApocalypticFormTrait.objects.create(
            name="Wings",
            description="Manifest wings for flight",
            cost=2,
            owner=self.user,
        )

    def test_default_values(self):
        """Test default values for ApocalypticFormTrait fields."""
        trait = ApocalypticFormTrait.objects.create(name="Simple Trait", owner=self.user)
        self.assertEqual(trait.cost, 1)
        self.assertEqual(trait.description, "")
        self.assertFalse(trait.high_torment_only)
        self.assertIsNone(trait.house)

    def test_type_and_gameline(self):
        """Test type and gameline values."""
        self.assertEqual(self.trait.type, "apocalyptic_form_trait")
        self.assertEqual(self.trait.gameline, "dtf")

    def test_str_representation(self):
        """Test string representation of trait."""
        self.assertEqual(str(self.trait), "Wings (2 pts)")

    def test_str_representation_high_torment_only(self):
        """Test string representation for high torment only trait."""
        trait = ApocalypticFormTrait.objects.create(
            name="Terrifying Visage",
            cost=3,
            high_torment_only=True,
            owner=self.user,
        )
        self.assertEqual(str(trait), "Terrifying Visage (3 pts) (High Torment Only)")


    def test_get_heading(self):
        """Test get_heading returns DTF heading."""
        self.assertEqual(self.trait.get_heading(), "dtf_heading")

    def test_house_relationship(self):
        """Test trait can be associated with a house."""
        house = DemonHouse.objects.create(
            name="Devils", celestial_name="Namaru", owner=self.user
        )
        trait = ApocalypticFormTrait.objects.create(
            name="Devilish Charm",
            cost=2,
            house=house,
            owner=self.user,
        )
        self.assertEqual(trait.house, house)
        self.assertIn(trait, house.apocalyptic_traits.all())

    def test_ordering_by_cost_then_name(self):
        """Traits should be ordered by cost, then by name."""
        trait1 = ApocalypticFormTrait.objects.create(name="Zephyr", cost=1, owner=self.user)
        trait2 = ApocalypticFormTrait.objects.create(name="Alpha", cost=2, owner=self.user)
        trait3 = ApocalypticFormTrait.objects.create(name="Beta", cost=1, owner=self.user)

        traits = list(ApocalypticFormTrait.objects.filter(pk__in=[trait1.pk, trait2.pk, trait3.pk]))
        # Cost 1: Beta, Zephyr (alphabetical), then Cost 2: Alpha
        self.assertEqual(traits[0], trait3)  # Beta (cost 1)
        self.assertEqual(traits[1], trait1)  # Zephyr (cost 1)
        self.assertEqual(traits[2], trait2)  # Alpha (cost 2)


class ApocalypticFormModelTests(TestCase):
    """Tests for ApocalypticForm model functionality."""

    def setUp(self):
        """Create test fixtures."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.form = ApocalypticForm.objects.create(name="Test Form", owner=self.user)

        # Create some traits for testing
        self.low_cost_trait = ApocalypticFormTrait.objects.create(
            name="Minor Power",
            cost=1,
            owner=self.user,
        )
        self.medium_cost_trait = ApocalypticFormTrait.objects.create(
            name="Medium Power",
            cost=2,
            owner=self.user,
        )
        self.high_cost_trait = ApocalypticFormTrait.objects.create(
            name="Major Power",
            cost=3,
            owner=self.user,
        )
        self.high_torment_only_trait = ApocalypticFormTrait.objects.create(
            name="Terrifying Aspect",
            cost=2,
            high_torment_only=True,
            owner=self.user,
        )

    def test_type_and_gameline(self):
        """Test type and gameline values."""
        self.assertEqual(self.form.type, "apocalyptic_form")
        self.assertEqual(self.form.gameline, "dtf")

    def test_str_representation(self):
        """Test string representation of form."""
        self.assertEqual(str(self.form), "Test Form")


    def test_get_heading(self):
        """Test get_heading returns DTF heading."""
        self.assertEqual(self.form.get_heading(), "dtf_heading")

    def test_ordering_by_name(self):
        """Forms should be ordered by name."""
        form_c = ApocalypticForm.objects.create(name="Charlie Form", owner=self.user)
        form_a = ApocalypticForm.objects.create(name="Alpha Form", owner=self.user)
        form_b = ApocalypticForm.objects.create(name="Beta Form", owner=self.user)

        forms = list(ApocalypticForm.objects.filter(pk__in=[form_a.pk, form_b.pk, form_c.pk]))
        self.assertEqual(forms[0], form_a)
        self.assertEqual(forms[1], form_b)
        self.assertEqual(forms[2], form_c)


class ApocalypticFormTraitCountTests(TestCase):
    """Tests for trait counting methods."""

    def setUp(self):
        """Create test fixtures."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.form = ApocalypticForm.objects.create(name="Test Form", owner=self.user)

        # Create traits
        self.traits = []
        for i in range(8):
            trait = ApocalypticFormTrait.objects.create(
                name=f"Trait {i}",
                cost=1,
                owner=self.user,
            )
            self.traits.append(trait)

    def test_low_torment_count_empty(self):
        """Low torment count should be 0 for empty form."""
        self.assertEqual(self.form.low_torment_count(), 0)

    def test_high_torment_count_empty(self):
        """High torment count should be 0 for empty form."""
        self.assertEqual(self.form.high_torment_count(), 0)

    def test_total_traits_empty(self):
        """Total traits should be 0 for empty form."""
        self.assertEqual(self.form.total_traits(), 0)

    def test_low_torment_count_with_traits(self):
        """Low torment count should reflect added traits."""
        self.form.low_torment_traits.add(self.traits[0], self.traits[1])
        self.assertEqual(self.form.low_torment_count(), 2)

    def test_high_torment_count_with_traits(self):
        """High torment count should reflect added traits."""
        self.form.high_torment_traits.add(self.traits[0], self.traits[1], self.traits[2])
        self.assertEqual(self.form.high_torment_count(), 3)

    def test_total_traits_with_both(self):
        """Total traits should sum low and high torment counts."""
        self.form.low_torment_traits.add(self.traits[0], self.traits[1])
        self.form.high_torment_traits.add(self.traits[2], self.traits[3], self.traits[4])
        self.assertEqual(self.form.total_traits(), 5)


class ApocalypticFormPointsTests(TestCase):
    """Tests for point calculation methods."""

    def setUp(self):
        """Create test fixtures."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.form = ApocalypticForm.objects.create(name="Test Form", owner=self.user)

        # Create traits with different costs
        self.trait_cost_1 = ApocalypticFormTrait.objects.create(
            name="Cheap Power", cost=1, owner=self.user
        )
        self.trait_cost_2 = ApocalypticFormTrait.objects.create(
            name="Medium Power", cost=2, owner=self.user
        )
        self.trait_cost_3 = ApocalypticFormTrait.objects.create(
            name="Expensive Power", cost=3, owner=self.user
        )
        self.trait_cost_2b = ApocalypticFormTrait.objects.create(
            name="Another Medium", cost=2, owner=self.user
        )

    def test_low_torment_points_empty(self):
        """Low torment points should be 0 for empty form."""
        self.assertEqual(self.form.low_torment_points(), 0)

    def test_high_torment_points_empty(self):
        """High torment points should be 0 for empty form."""
        self.assertEqual(self.form.high_torment_points(), 0)

    def test_total_points_empty(self):
        """Total points should be 0 for empty form."""
        self.assertEqual(self.form.total_points(), 0)

    def test_points_remaining_empty(self):
        """Points remaining should be 16 for empty form."""
        self.assertEqual(self.form.points_remaining(), 16)

    def test_low_torment_points_calculated(self):
        """Low torment points should sum trait costs."""
        self.form.low_torment_traits.add(self.trait_cost_1, self.trait_cost_3)
        self.assertEqual(self.form.low_torment_points(), 4)  # 1 + 3

    def test_high_torment_points_calculated(self):
        """High torment points should sum trait costs."""
        self.form.high_torment_traits.add(self.trait_cost_2, self.trait_cost_2b)
        self.assertEqual(self.form.high_torment_points(), 4)  # 2 + 2

    def test_total_points_both_categories(self):
        """Total points should sum both low and high torment."""
        self.form.low_torment_traits.add(self.trait_cost_1, self.trait_cost_2)
        self.form.high_torment_traits.add(self.trait_cost_3)
        self.assertEqual(self.form.total_points(), 6)  # 1 + 2 + 3

    def test_points_remaining_with_traits(self):
        """Points remaining should be 16 minus total points."""
        self.form.low_torment_traits.add(self.trait_cost_1)
        self.form.high_torment_traits.add(self.trait_cost_3)
        self.assertEqual(self.form.points_remaining(), 12)  # 16 - 1 - 3


class ApocalypticFormValidationTests(TestCase):
    """Tests for form validation methods."""

    def setUp(self):
        """Create test fixtures."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.form = ApocalypticForm.objects.create(name="Test Form", owner=self.user)

        # Create 8 cost-1 traits for a valid form
        self.traits = []
        for i in range(8):
            trait = ApocalypticFormTrait.objects.create(
                name=f"Trait {i}", cost=1, owner=self.user
            )
            self.traits.append(trait)

    def test_is_valid_empty_form(self):
        """Empty form should not be valid."""
        self.assertFalse(self.form.is_valid())

    def test_is_complete_empty_form(self):
        """Empty form should not be complete."""
        self.assertFalse(self.form.is_complete())

    def test_is_valid_partial_form(self):
        """Partial form should not be valid."""
        self.form.low_torment_traits.add(*self.traits[:2])
        self.form.high_torment_traits.add(*self.traits[4:6])
        self.assertFalse(self.form.is_valid())

    def test_is_complete_partial_form(self):
        """Partial form should not be complete."""
        self.form.low_torment_traits.add(*self.traits[:3])
        self.form.high_torment_traits.add(*self.traits[4:7])
        self.assertFalse(self.form.is_complete())

    def test_is_valid_complete_form(self):
        """Form with 4+4 traits and points <= 16 should be valid."""
        self.form.low_torment_traits.add(*self.traits[:4])
        self.form.high_torment_traits.add(*self.traits[4:8])
        self.assertTrue(self.form.is_valid())

    def test_is_complete_complete_form(self):
        """Form with 4+4 traits should be complete."""
        self.form.low_torment_traits.add(*self.traits[:4])
        self.form.high_torment_traits.add(*self.traits[4:8])
        self.assertTrue(self.form.is_complete())

    def test_is_valid_over_point_limit(self):
        """Form over 16 points should not be valid."""
        # Create expensive traits
        expensive_traits = []
        for i in range(8):
            trait = ApocalypticFormTrait.objects.create(
                name=f"Expensive {i}", cost=3, owner=self.user
            )
            expensive_traits.append(trait)

        # Add them to form (total = 24 points)
        self.form.low_torment_traits.set(expensive_traits[:4])
        self.form.high_torment_traits.set(expensive_traits[4:8])
        self.assertFalse(self.form.is_valid())


class ApocalypticFormCanAddTraitTests(TestCase):
    """Tests for can_add_*_torment_trait methods."""

    def setUp(self):
        """Create test fixtures."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.form = ApocalypticForm.objects.create(name="Test Form", owner=self.user)

        self.normal_trait = ApocalypticFormTrait.objects.create(
            name="Normal", cost=2, owner=self.user
        )
        self.high_torment_only_trait = ApocalypticFormTrait.objects.create(
            name="High Torment Only", cost=2, high_torment_only=True, owner=self.user
        )

    def test_can_add_low_torment_trait_empty_form(self):
        """Should be able to add low torment trait to empty form."""
        self.assertTrue(self.form.can_add_low_torment_trait(self.normal_trait))

    def test_cannot_add_high_torment_only_to_low_torment(self):
        """Cannot add high_torment_only trait to low torment list."""
        self.assertFalse(self.form.can_add_low_torment_trait(self.high_torment_only_trait))

    def test_can_add_high_torment_only_to_high_torment(self):
        """Can add high_torment_only trait to high torment list."""
        self.assertTrue(self.form.can_add_high_torment_trait(self.high_torment_only_trait))

    def test_cannot_add_low_torment_when_full(self):
        """Cannot add to low torment when already has 4 traits."""
        for i in range(4):
            trait = ApocalypticFormTrait.objects.create(
                name=f"Filler {i}", cost=1, owner=self.user
            )
            self.form.low_torment_traits.add(trait)

        self.assertFalse(self.form.can_add_low_torment_trait(self.normal_trait))

    def test_cannot_add_high_torment_when_full(self):
        """Cannot add to high torment when already has 4 traits."""
        for i in range(4):
            trait = ApocalypticFormTrait.objects.create(
                name=f"Filler {i}", cost=1, owner=self.user
            )
            self.form.high_torment_traits.add(trait)

        self.assertFalse(self.form.can_add_high_torment_trait(self.normal_trait))

    def test_cannot_add_duplicate_low_torment(self):
        """Cannot add same trait twice to low torment."""
        self.form.low_torment_traits.add(self.normal_trait)
        self.assertFalse(self.form.can_add_low_torment_trait(self.normal_trait))

    def test_cannot_add_duplicate_high_torment(self):
        """Cannot add same trait twice to high torment."""
        self.form.high_torment_traits.add(self.normal_trait)
        self.assertFalse(self.form.can_add_high_torment_trait(self.normal_trait))

    def test_cannot_add_trait_in_other_list_to_low(self):
        """Cannot add trait already in high torment to low torment."""
        self.form.high_torment_traits.add(self.normal_trait)
        self.assertFalse(self.form.can_add_low_torment_trait(self.normal_trait))

    def test_cannot_add_trait_in_other_list_to_high(self):
        """Cannot add trait already in low torment to high torment."""
        self.form.low_torment_traits.add(self.normal_trait)
        self.assertFalse(self.form.can_add_high_torment_trait(self.normal_trait))

    def test_cannot_exceed_point_limit_low_torment(self):
        """Cannot add trait if it would exceed 16 point limit."""
        # Add 15 points worth of traits
        expensive = ApocalypticFormTrait.objects.create(
            name="Expensive", cost=5, owner=self.user
        )
        self.form.low_torment_traits.add(expensive)

        for i in range(3):
            trait = ApocalypticFormTrait.objects.create(
                name=f"Cost3 {i}", cost=3, owner=self.user
            )
            self.form.high_torment_traits.add(trait)
        # Total: 5 + 9 = 14 points

        # Try to add a 3-point trait (would be 17)
        self.assertFalse(self.form.can_add_low_torment_trait(self.high_torment_only_trait))  # Wait, this is high_torment_only
        three_cost = ApocalypticFormTrait.objects.create(
            name="Three Cost", cost=3, owner=self.user
        )
        self.assertFalse(self.form.can_add_low_torment_trait(three_cost))


class ApocalypticFormAddTraitTests(TestCase):
    """Tests for add_*_torment_trait methods."""

    def setUp(self):
        """Create test fixtures."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.form = ApocalypticForm.objects.create(name="Test Form", owner=self.user)

        self.trait = ApocalypticFormTrait.objects.create(
            name="Power", cost=2, owner=self.user
        )
        self.high_only = ApocalypticFormTrait.objects.create(
            name="Terror", cost=2, high_torment_only=True, owner=self.user
        )

    def test_add_low_torment_trait_success(self):
        """Successfully adding low torment trait returns True."""
        result = self.form.add_low_torment_trait(self.trait)
        self.assertTrue(result)
        self.assertIn(self.trait, self.form.low_torment_traits.all())

    def test_add_low_torment_trait_failure(self):
        """Failing to add low torment trait returns False."""
        result = self.form.add_low_torment_trait(self.high_only)
        self.assertFalse(result)
        self.assertNotIn(self.high_only, self.form.low_torment_traits.all())

    def test_add_high_torment_trait_success(self):
        """Successfully adding high torment trait returns True."""
        result = self.form.add_high_torment_trait(self.trait)
        self.assertTrue(result)
        self.assertIn(self.trait, self.form.high_torment_traits.all())

    def test_add_high_torment_trait_high_only_success(self):
        """High torment only trait can be added to high torment."""
        result = self.form.add_high_torment_trait(self.high_only)
        self.assertTrue(result)
        self.assertIn(self.high_only, self.form.high_torment_traits.all())


class ApocalypticFormRemoveTraitTests(TestCase):
    """Tests for remove_*_torment_trait methods."""

    def setUp(self):
        """Create test fixtures."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.form = ApocalypticForm.objects.create(name="Test Form", owner=self.user)

        self.trait = ApocalypticFormTrait.objects.create(
            name="Power", cost=2, owner=self.user
        )
        self.other_trait = ApocalypticFormTrait.objects.create(
            name="Other", cost=1, owner=self.user
        )

    def test_remove_low_torment_trait_success(self):
        """Successfully removing low torment trait returns True."""
        self.form.low_torment_traits.add(self.trait)
        result = self.form.remove_low_torment_trait(self.trait)
        self.assertTrue(result)
        self.assertNotIn(self.trait, self.form.low_torment_traits.all())

    def test_remove_low_torment_trait_not_present(self):
        """Removing non-present trait from low torment returns False."""
        result = self.form.remove_low_torment_trait(self.trait)
        self.assertFalse(result)

    def test_remove_high_torment_trait_success(self):
        """Successfully removing high torment trait returns True."""
        self.form.high_torment_traits.add(self.trait)
        result = self.form.remove_high_torment_trait(self.trait)
        self.assertTrue(result)
        self.assertNotIn(self.trait, self.form.high_torment_traits.all())

    def test_remove_high_torment_trait_not_present(self):
        """Removing non-present trait from high torment returns False."""
        result = self.form.remove_high_torment_trait(self.trait)
        self.assertFalse(result)


class ApocalypticFormCopyTests(TestCase):
    """Tests for copy_from method."""

    def setUp(self):
        """Create test fixtures."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.source = ApocalypticForm.objects.create(name="Source Form", owner=self.user)
        self.target = ApocalypticForm.objects.create(name="Target Form", owner=self.user)

        # Create traits
        self.low_traits = []
        self.high_traits = []
        for i in range(4):
            low = ApocalypticFormTrait.objects.create(
                name=f"Low {i}", cost=1, owner=self.user
            )
            high = ApocalypticFormTrait.objects.create(
                name=f"High {i}", cost=1, owner=self.user
            )
            self.low_traits.append(low)
            self.high_traits.append(high)

        # Set up source form
        self.source.low_torment_traits.set(self.low_traits)
        self.source.high_torment_traits.set(self.high_traits)

    def test_copy_from_copies_low_torment_traits(self):
        """copy_from should copy low torment traits."""
        self.target.copy_from(self.source)
        self.assertEqual(
            set(self.target.low_torment_traits.all()),
            set(self.source.low_torment_traits.all()),
        )

    def test_copy_from_copies_high_torment_traits(self):
        """copy_from should copy high torment traits."""
        self.target.copy_from(self.source)
        self.assertEqual(
            set(self.target.high_torment_traits.all()),
            set(self.source.high_torment_traits.all()),
        )

    def test_copy_from_overwrites_existing(self):
        """copy_from should overwrite existing traits in target."""
        # Add some traits to target first
        other_trait = ApocalypticFormTrait.objects.create(
            name="Other", cost=1, owner=self.user
        )
        self.target.low_torment_traits.add(other_trait)

        self.target.copy_from(self.source)

        # Target should only have source's traits
        self.assertNotIn(other_trait, self.target.low_torment_traits.all())
        self.assertEqual(self.target.low_torment_count(), 4)
