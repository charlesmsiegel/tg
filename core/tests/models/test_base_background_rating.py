"""
Tests for BaseBackgroundRating abstract base class.

Verifies that all concrete implementations inherit the shared functionality
correctly and maintain database constraints.
"""

from django.core.exceptions import ValidationError
from django.test import TestCase

from characters.models.core.background_block import (
    Background,
    BackgroundRating,
    PooledBackgroundRating,
)
from characters.models.core.group import Group
from characters.models.core.human import Human
from locations.models.mage.chantry import Chantry, ChantryBackgroundRating


class TestBaseBackgroundRatingInheritance(TestCase):
    """Test that all concrete implementations inherit from BaseBackgroundRating."""

    def test_backgroundrating_inherits_base(self):
        """Test BackgroundRating inherits from BaseBackgroundRating."""
        from core.models import BaseBackgroundRating

        self.assertTrue(issubclass(BackgroundRating, BaseBackgroundRating))

    def test_pooledbackgroundrating_inherits_base(self):
        """Test PooledBackgroundRating inherits from BaseBackgroundRating."""
        from core.models import BaseBackgroundRating

        self.assertTrue(issubclass(PooledBackgroundRating, BaseBackgroundRating))

    def test_chantrybackgroundrating_inherits_base(self):
        """Test ChantryBackgroundRating inherits from BaseBackgroundRating."""
        from core.models import BaseBackgroundRating

        self.assertTrue(issubclass(ChantryBackgroundRating, BaseBackgroundRating))


class TestBackgroundRatingSharedBehavior(TestCase):
    """Test shared behavior inherited from BaseBackgroundRating."""

    def setUp(self):
        self.bg = Background.objects.create(name="Test Background", property_name="test_bg")

    def test_str_method_inherited(self):
        """Test __str__ returns expected format for all implementations."""
        # Create instances for each type
        human = Human.objects.create(name="Test Human")
        char_rating = BackgroundRating.objects.create(char=human, bg=self.bg, note="Personal")
        self.assertEqual(str(char_rating), f"{self.bg} (Personal)")

        group = Group.objects.create(name="Test Group")
        group_rating = PooledBackgroundRating.objects.create(group=group, bg=self.bg, note="Shared")
        self.assertEqual(str(group_rating), f"{self.bg} (Shared)")

        chantry = Chantry.objects.create(name="Test Chantry")
        chantry_rating = ChantryBackgroundRating.objects.create(
            chantry=chantry, bg=self.bg, note="Chantry"
        )
        self.assertEqual(str(chantry_rating), f"{self.bg} (Chantry)")

    def test_default_rating_is_zero(self):
        """Test that default rating is 0 for all implementations."""
        human = Human.objects.create(name="Test Human")
        char_rating = BackgroundRating.objects.create(char=human, bg=self.bg)
        self.assertEqual(char_rating.rating, 0)

        group = Group.objects.create(name="Test Group")
        group_rating = PooledBackgroundRating.objects.create(group=group, bg=self.bg)
        self.assertEqual(group_rating.rating, 0)

        chantry = Chantry.objects.create(name="Test Chantry")
        chantry_rating = ChantryBackgroundRating.objects.create(chantry=chantry, bg=self.bg)
        self.assertEqual(chantry_rating.rating, 0)

    def test_default_note_is_empty(self):
        """Test that default note is empty string for all implementations."""
        human = Human.objects.create(name="Test Human")
        char_rating = BackgroundRating.objects.create(char=human, bg=self.bg)
        self.assertEqual(char_rating.note, "")

        group = Group.objects.create(name="Test Group")
        group_rating = PooledBackgroundRating.objects.create(group=group, bg=self.bg)
        self.assertEqual(group_rating.note, "")

        chantry = Chantry.objects.create(name="Test Chantry")
        chantry_rating = ChantryBackgroundRating.objects.create(chantry=chantry, bg=self.bg)
        self.assertEqual(chantry_rating.note, "")

    def test_default_url_is_empty(self):
        """Test that default url is empty string for all implementations."""
        human = Human.objects.create(name="Test Human")
        char_rating = BackgroundRating.objects.create(char=human, bg=self.bg)
        self.assertEqual(char_rating.url, "")

        group = Group.objects.create(name="Test Group")
        group_rating = PooledBackgroundRating.objects.create(group=group, bg=self.bg)
        self.assertEqual(group_rating.url, "")

        chantry = Chantry.objects.create(name="Test Chantry")
        chantry_rating = ChantryBackgroundRating.objects.create(chantry=chantry, bg=self.bg)
        self.assertEqual(chantry_rating.url, "")

    def test_default_complete_is_false(self):
        """Test that default complete is False for all implementations."""
        human = Human.objects.create(name="Test Human")
        char_rating = BackgroundRating.objects.create(char=human, bg=self.bg)
        self.assertFalse(char_rating.complete)

        group = Group.objects.create(name="Test Group")
        group_rating = PooledBackgroundRating.objects.create(group=group, bg=self.bg)
        self.assertFalse(group_rating.complete)

        chantry = Chantry.objects.create(name="Test Chantry")
        chantry_rating = ChantryBackgroundRating.objects.create(chantry=chantry, bg=self.bg)
        self.assertFalse(chantry_rating.complete)


class TestBackgroundRatingValidation(TestCase):
    """Test rating validation for all implementations."""

    def setUp(self):
        self.bg = Background.objects.create(name="Test Background", property_name="test_bg")

    def test_rating_at_boundary_values(self):
        """Test ratings at 0 and 10 are valid."""
        human = Human.objects.create(name="Test Human")

        # Test 0
        rating_zero = BackgroundRating(char=human, bg=self.bg, rating=0)
        rating_zero.full_clean()  # Should not raise
        rating_zero.save()
        self.assertEqual(rating_zero.rating, 0)

        # Test 10
        bg2 = Background.objects.create(name="Test Background 2", property_name="test_bg_2")
        rating_max = BackgroundRating(char=human, bg=bg2, rating=10)
        rating_max.full_clean()  # Should not raise
        rating_max.save()
        self.assertEqual(rating_max.rating, 10)

    def test_rating_outside_range_fails_validation(self):
        """Test ratings outside 0 to 10 fail validation."""
        human = Human.objects.create(name="Test Human")

        # Test > 10
        rating_high = BackgroundRating(char=human, bg=self.bg, rating=11)
        with self.assertRaises(ValidationError):
            rating_high.full_clean()

        # Test < 0
        rating_low = BackgroundRating(char=human, bg=self.bg, rating=-1)
        with self.assertRaises(ValidationError):
            rating_low.full_clean()

    def test_pooled_rating_outside_range_fails_validation(self):
        """Test PooledBackgroundRating ratings outside 0 to 10 fail validation."""
        group = Group.objects.create(name="Test Group")

        # Test > 10
        rating_high = PooledBackgroundRating(group=group, bg=self.bg, rating=11)
        with self.assertRaises(ValidationError):
            rating_high.full_clean()

        # Test < 0
        rating_low = PooledBackgroundRating(group=group, bg=self.bg, rating=-1)
        with self.assertRaises(ValidationError):
            rating_low.full_clean()

    def test_chantry_rating_outside_range_fails_validation(self):
        """Test ChantryBackgroundRating ratings outside 0 to 10 fail validation."""
        chantry = Chantry.objects.create(name="Test Chantry")

        # Test > 10
        rating_high = ChantryBackgroundRating(chantry=chantry, bg=self.bg, rating=11)
        with self.assertRaises(ValidationError):
            rating_high.full_clean()

        # Test < 0
        rating_low = ChantryBackgroundRating(chantry=chantry, bg=self.bg, rating=-1)
        with self.assertRaises(ValidationError):
            rating_low.full_clean()


class TestBackgroundRatingModelSpecificFields(TestCase):
    """Test model-specific fields that aren't in the base class."""

    def setUp(self):
        self.bg = Background.objects.create(
            name="Test Background", property_name="test_bg", alternate_name="Alt Name"
        )

    def test_backgroundrating_pooled_field(self):
        """Test BackgroundRating has pooled field."""
        human = Human.objects.create(name="Test Human")
        rating = BackgroundRating.objects.create(char=human, bg=self.bg, pooled=True)
        self.assertTrue(rating.pooled)

    def test_backgroundrating_display_alt_name_field(self):
        """Test BackgroundRating has display_alt_name field."""
        human = Human.objects.create(name="Test Human")
        rating = BackgroundRating.objects.create(char=human, bg=self.bg, display_alt_name=True)
        self.assertTrue(rating.display_alt_name)

    def test_chantrybackgroundrating_display_alt_name_field(self):
        """Test ChantryBackgroundRating has display_alt_name field."""
        chantry = Chantry.objects.create(name="Test Chantry")
        rating = ChantryBackgroundRating.objects.create(
            chantry=chantry, bg=self.bg, display_alt_name=True
        )
        self.assertTrue(rating.display_alt_name)

    def test_pooledbackgroundrating_no_display_alt_name(self):
        """Test PooledBackgroundRating doesn't have display_alt_name field."""
        self.assertFalse(hasattr(PooledBackgroundRating, "display_alt_name"))

    def test_pooledbackgroundrating_no_pooled(self):
        """Test PooledBackgroundRating doesn't have pooled field."""
        # PooledBackgroundRating doesn't need a pooled field as it's inherently pooled
        group = Group.objects.create(name="Test Group")
        rating = PooledBackgroundRating.objects.create(group=group, bg=self.bg)
        self.assertFalse(hasattr(rating, "pooled"))


class TestDisplayNameMethod(TestCase):
    """Test display_name method on ratings that have it."""

    def setUp(self):
        self.bg = Background.objects.create(
            name="Resources", property_name="resources", alternate_name="Wealth"
        )
        self.bg_no_alt = Background.objects.create(
            name="Allies", property_name="allies", alternate_name=""
        )

    def test_backgroundrating_display_name_default(self):
        """Test BackgroundRating display_name returns bg.name by default."""
        human = Human.objects.create(name="Test Human")
        rating = BackgroundRating.objects.create(char=human, bg=self.bg, display_alt_name=False)
        self.assertEqual(rating.display_name(), "Resources")

    def test_backgroundrating_display_name_alt(self):
        """Test BackgroundRating display_name returns alternate_name when flag is set."""
        human = Human.objects.create(name="Test Human")
        rating = BackgroundRating.objects.create(char=human, bg=self.bg, display_alt_name=True)
        self.assertEqual(rating.display_name(), "Wealth")

    def test_backgroundrating_display_name_no_alt_available(self):
        """Test BackgroundRating display_name returns name when no alternate exists."""
        human = Human.objects.create(name="Test Human")
        rating = BackgroundRating.objects.create(
            char=human, bg=self.bg_no_alt, display_alt_name=True
        )
        # Even with flag True, if alternate_name is empty, returns name
        self.assertEqual(rating.display_name(), "Allies")

    def test_chantrybackgroundrating_display_name_default(self):
        """Test ChantryBackgroundRating display_name returns bg.name by default."""
        chantry = Chantry.objects.create(name="Test Chantry")
        rating = ChantryBackgroundRating.objects.create(
            chantry=chantry, bg=self.bg, display_alt_name=False
        )
        self.assertEqual(rating.display_name(), "Resources")

    def test_chantrybackgroundrating_display_name_alt(self):
        """Test ChantryBackgroundRating display_name returns alternate_name when flag set."""
        chantry = Chantry.objects.create(name="Test Chantry")
        rating = ChantryBackgroundRating.objects.create(
            chantry=chantry, bg=self.bg, display_alt_name=True
        )
        self.assertEqual(rating.display_name(), "Wealth")
