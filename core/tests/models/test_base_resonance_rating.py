"""
Tests for BaseResonanceRating abstract base class.

Verifies that all concrete implementations inherit the shared functionality
correctly and maintain database constraints.
"""

from django.core.exceptions import ValidationError
from django.test import TestCase

from characters.models.mage.mage import Mage, ResRating
from characters.models.mage.resonance import Resonance
from items.models.mage.wonder import Wonder, WonderResonanceRating
from items.models.mummy.relic import MummyRelic, RelicResonanceRating
from locations.models.mage.node import Node, NodeResonanceRating


class TestBaseResonanceRatingInheritance(TestCase):
    """Test that all concrete implementations inherit from BaseResonanceRating."""

    def test_resrating_inherits_base(self):
        """Test ResRating inherits from BaseResonanceRating."""
        from core.models import BaseResonanceRating

        self.assertTrue(issubclass(ResRating, BaseResonanceRating))

    def test_wonderresonancerating_inherits_base(self):
        """Test WonderResonanceRating inherits from BaseResonanceRating."""
        from core.models import BaseResonanceRating

        self.assertTrue(issubclass(WonderResonanceRating, BaseResonanceRating))

    def test_noderesonancerating_inherits_base(self):
        """Test NodeResonanceRating inherits from BaseResonanceRating."""
        from core.models import BaseResonanceRating

        self.assertTrue(issubclass(NodeResonanceRating, BaseResonanceRating))

    def test_relicresonancerating_inherits_base(self):
        """Test RelicResonanceRating inherits from BaseResonanceRating."""
        from core.models import BaseResonanceRating

        self.assertTrue(issubclass(RelicResonanceRating, BaseResonanceRating))


class TestResonanceRatingSharedBehavior(TestCase):
    """Test shared behavior inherited from BaseResonanceRating."""

    def setUp(self):
        self.resonance = Resonance.objects.create(name="Dynamic")

    def test_str_method_inherited(self):
        """Test __str__ returns expected format for implementations using base class."""
        # Test ResRating - uses base class __str__
        mage = Mage.objects.create(name="Test Mage")
        mage_rating = ResRating.objects.create(mage=mage, resonance=self.resonance, rating=2)
        self.assertEqual(str(mage_rating), "Dynamic: 2")

        # Test WonderResonanceRating - uses base class __str__
        wonder = Wonder.objects.create(name="Test Wonder")
        wonder_rating = WonderResonanceRating.objects.create(
            wonder=wonder, resonance=self.resonance, rating=3
        )
        self.assertEqual(str(wonder_rating), "Dynamic: 3")

        # Test RelicResonanceRating - uses base class __str__
        relic = MummyRelic.objects.create(name="Test Relic")
        relic_rating = RelicResonanceRating.objects.create(
            relic=relic, resonance=self.resonance, rating=5
        )
        self.assertEqual(str(relic_rating), "Dynamic: 5")

    def test_str_method_overridden(self):
        """Test NodeResonanceRating uses custom __str__ that includes node name."""
        node = Node.objects.create(name="Test Node")
        node_rating = NodeResonanceRating.objects.create(
            node=node, resonance=self.resonance, rating=4
        )
        # NodeResonanceRating has custom __str__: f"{self.node}: {self.resonance} {self.rating}"
        self.assertEqual(str(node_rating), "Test Node: Dynamic 4")

    def test_default_rating_is_zero(self):
        """Test that default rating is 0 for all implementations."""
        mage = Mage.objects.create(name="Test Mage")
        mage_rating = ResRating.objects.create(mage=mage, resonance=self.resonance)
        self.assertEqual(mage_rating.rating, 0)

        wonder = Wonder.objects.create(name="Test Wonder")
        wonder_rating = WonderResonanceRating.objects.create(
            wonder=wonder, resonance=self.resonance
        )
        self.assertEqual(wonder_rating.rating, 0)

        node = Node.objects.create(name="Test Node")
        node_rating = NodeResonanceRating.objects.create(node=node, resonance=self.resonance)
        self.assertEqual(node_rating.rating, 0)


class TestResonanceRatingValidation(TestCase):
    """Test rating validation for all implementations."""

    def setUp(self):
        self.resonance = Resonance.objects.create(name="Dynamic")

    def test_rating_at_boundary_values(self):
        """Test ratings at 0 and 10 are valid."""
        mage = Mage.objects.create(name="Test Mage")

        # Test 0
        rating_zero = ResRating(mage=mage, resonance=self.resonance, rating=0)
        rating_zero.full_clean()  # Should not raise
        rating_zero.save()
        self.assertEqual(rating_zero.rating, 0)

        # Test 10
        resonance2 = Resonance.objects.create(name="Static")
        rating_max = ResRating(mage=mage, resonance=resonance2, rating=10)
        rating_max.full_clean()  # Should not raise
        rating_max.save()
        self.assertEqual(rating_max.rating, 10)

    def test_rating_outside_range_fails_validation(self):
        """Test ratings outside 0 to 10 fail validation."""
        mage = Mage.objects.create(name="Test Mage")

        # Test > 10
        rating_high = ResRating(mage=mage, resonance=self.resonance, rating=11)
        with self.assertRaises(ValidationError):
            rating_high.full_clean()

        # Test < 0
        rating_low = ResRating(mage=mage, resonance=self.resonance, rating=-1)
        with self.assertRaises(ValidationError):
            rating_low.full_clean()

    def test_all_implementations_validate_range(self):
        """Test all implementations enforce 0-10 range."""
        # Test WonderResonanceRating
        wonder = Wonder.objects.create(name="Test Wonder")
        wonder_rating = WonderResonanceRating(wonder=wonder, resonance=self.resonance, rating=11)
        with self.assertRaises(ValidationError):
            wonder_rating.full_clean()

        # Test NodeResonanceRating
        node = Node.objects.create(name="Test Node")
        node_rating = NodeResonanceRating(node=node, resonance=self.resonance, rating=11)
        with self.assertRaises(ValidationError):
            node_rating.full_clean()

        # Test RelicResonanceRating
        relic = MummyRelic.objects.create(name="Test Relic")
        relic_rating = RelicResonanceRating(relic=relic, resonance=self.resonance, rating=11)
        with self.assertRaises(ValidationError):
            relic_rating.full_clean()


class TestResonanceRatingForeignKeyBehavior(TestCase):
    """Test FK behavior for different ResonanceRating implementations."""

    def setUp(self):
        self.resonance = Resonance.objects.create(name="Dynamic")

    def test_set_null_on_resonance_delete_for_mage(self):
        """Test that deleting resonance sets FK to NULL for ResRating."""
        mage = Mage.objects.create(name="Test Mage")
        rating = ResRating.objects.create(mage=mage, resonance=self.resonance, rating=3)

        self.assertEqual(ResRating.objects.count(), 1)
        self.resonance.delete()
        # ResRating uses SET_NULL, so record should remain with null resonance
        self.assertEqual(ResRating.objects.count(), 1)
        rating.refresh_from_db()
        self.assertIsNone(rating.resonance)

    def test_set_null_on_parent_delete_for_wonder(self):
        """Test that deleting Wonder sets FK to NULL for WonderResonanceRating."""
        wonder = Wonder.objects.create(name="Test Wonder")
        rating = WonderResonanceRating.objects.create(
            wonder=wonder, resonance=self.resonance, rating=3
        )

        self.assertEqual(WonderResonanceRating.objects.count(), 1)
        wonder.delete()
        # WonderResonanceRating uses SET_NULL, so record remains
        self.assertEqual(WonderResonanceRating.objects.count(), 1)
        rating.refresh_from_db()
        self.assertIsNone(rating.wonder)

    def test_cascade_delete_for_relic(self):
        """Test that deleting Relic cascades to RelicResonanceRating."""
        relic = MummyRelic.objects.create(name="Test Relic")
        RelicResonanceRating.objects.create(relic=relic, resonance=self.resonance, rating=3)

        self.assertEqual(RelicResonanceRating.objects.count(), 1)
        relic.delete()
        # RelicResonanceRating uses CASCADE, so record is deleted
        self.assertEqual(RelicResonanceRating.objects.count(), 0)
