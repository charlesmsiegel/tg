"""
Tests for BaseMeritFlawRating abstract base class.

Verifies that all concrete implementations inherit the shared functionality
correctly and maintain database constraints.
"""

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from characters.models.core import MeritFlaw
from characters.models.core.human import Human
from characters.models.core.merit_flaw_block import MeritFlawRating
from locations.models.mage import Node, NodeMeritFlawRating
from locations.models.mummy import Tomb, TombMeritFlawRating
from locations.models.vampire import Haven, HavenMeritFlawRating


class TestBaseMeritFlawRatingInheritance(TestCase):
    """Test that all concrete implementations inherit from BaseMeritFlawRating."""

    def test_meritflawrating_inherits_base(self):
        """Test MeritFlawRating inherits from BaseMeritFlawRating."""
        from core.models import BaseMeritFlawRating

        self.assertTrue(issubclass(MeritFlawRating, BaseMeritFlawRating))

    def test_nodemeritflawrating_inherits_base(self):
        """Test NodeMeritFlawRating inherits from BaseMeritFlawRating."""
        from core.models import BaseMeritFlawRating

        self.assertTrue(issubclass(NodeMeritFlawRating, BaseMeritFlawRating))

    def test_havenmeritflawrating_inherits_base(self):
        """Test HavenMeritFlawRating inherits from BaseMeritFlawRating."""
        from core.models import BaseMeritFlawRating

        self.assertTrue(issubclass(HavenMeritFlawRating, BaseMeritFlawRating))

    def test_tombmeritflawrating_inherits_base(self):
        """Test TombMeritFlawRating inherits from BaseMeritFlawRating."""
        from core.models import BaseMeritFlawRating

        self.assertTrue(issubclass(TombMeritFlawRating, BaseMeritFlawRating))


class TestMeritFlawRatingSharedBehavior(TestCase):
    """Test shared behavior inherited from BaseMeritFlawRating."""

    def setUp(self):
        self.mf = MeritFlaw.objects.create(name="Test Merit")
        self.mf.add_ratings([1, 2, 3])

    def test_str_method_inherited(self):
        """Test __str__ returns expected format for all implementations."""
        # Create instances for each type
        human = Human.objects.create(name="Test Human")
        char_rating = MeritFlawRating.objects.create(character=human, mf=self.mf, rating=2)
        self.assertEqual(str(char_rating), f"{self.mf}: 2")

        node = Node.objects.create(name="Test Node")
        node_rating = NodeMeritFlawRating.objects.create(node=node, mf=self.mf, rating=3)
        self.assertEqual(str(node_rating), f"{self.mf}: 3")

        haven = Haven.objects.create(name="Test Haven")
        haven_rating = HavenMeritFlawRating.objects.create(haven=haven, mf=self.mf, rating=1)
        self.assertEqual(str(haven_rating), f"{self.mf}: 1")

        tomb = Tomb.objects.create(name="Test Tomb")
        tomb_rating = TombMeritFlawRating.objects.create(tomb=tomb, mf=self.mf, rating=-2)
        self.assertEqual(str(tomb_rating), f"{self.mf}: -2")

    def test_default_rating_is_zero(self):
        """Test that default rating is 0 for all implementations."""
        human = Human.objects.create(name="Test Human")
        char_rating = MeritFlawRating.objects.create(character=human, mf=self.mf)
        self.assertEqual(char_rating.rating, 0)

        node = Node.objects.create(name="Test Node")
        node_rating = NodeMeritFlawRating.objects.create(node=node, mf=self.mf)
        self.assertEqual(node_rating.rating, 0)

        haven = Haven.objects.create(name="Test Haven")
        haven_rating = HavenMeritFlawRating.objects.create(haven=haven, mf=self.mf)
        self.assertEqual(haven_rating.rating, 0)

        tomb = Tomb.objects.create(name="Test Tomb")
        tomb_rating = TombMeritFlawRating.objects.create(tomb=tomb, mf=self.mf)
        self.assertEqual(tomb_rating.rating, 0)


class TestMeritFlawRatingValidation(TestCase):
    """Test rating validation for all implementations."""

    def setUp(self):
        self.mf = MeritFlaw.objects.create(name="Test Merit")
        self.mf.add_ratings([-5, -3, -1, 1, 3, 5])

    def test_rating_at_boundary_values(self):
        """Test ratings at -10 and 10 are valid."""
        human = Human.objects.create(name="Test Human")

        # Test -10
        rating_neg = MeritFlawRating(character=human, mf=self.mf, rating=-10)
        rating_neg.full_clean()  # Should not raise
        rating_neg.save()
        self.assertEqual(rating_neg.rating, -10)

        # Test 10
        mf2 = MeritFlaw.objects.create(name="Test Merit 2")
        rating_pos = MeritFlawRating(character=human, mf=mf2, rating=10)
        rating_pos.full_clean()  # Should not raise
        rating_pos.save()
        self.assertEqual(rating_pos.rating, 10)

    def test_rating_outside_range_fails_validation(self):
        """Test ratings outside -10 to 10 fail validation."""
        human = Human.objects.create(name="Test Human")

        # Test > 10
        rating_high = MeritFlawRating(character=human, mf=self.mf, rating=11)
        with self.assertRaises(ValidationError):
            rating_high.full_clean()

        # Test < -10
        rating_low = MeritFlawRating(character=human, mf=self.mf, rating=-11)
        with self.assertRaises(ValidationError):
            rating_low.full_clean()


class TestMeritFlawRatingConstraints(TestCase):
    """Test database constraints on concrete implementations."""

    def setUp(self):
        self.mf = MeritFlaw.objects.create(name="Test Merit")
        self.mf.add_ratings([1, 2, 3])

    def test_haven_unique_together_constraint(self):
        """Test HavenMeritFlawRating unique_together constraint."""
        haven = Haven.objects.create(name="Test Haven")
        HavenMeritFlawRating.objects.create(haven=haven, mf=self.mf, rating=1)

        with self.assertRaises(IntegrityError):
            HavenMeritFlawRating.objects.create(haven=haven, mf=self.mf, rating=2)

    def test_tomb_unique_together_constraint(self):
        """Test TombMeritFlawRating unique_together constraint."""
        tomb = Tomb.objects.create(name="Test Tomb")
        TombMeritFlawRating.objects.create(tomb=tomb, mf=self.mf, rating=1)

        with self.assertRaises(IntegrityError):
            TombMeritFlawRating.objects.create(tomb=tomb, mf=self.mf, rating=2)
