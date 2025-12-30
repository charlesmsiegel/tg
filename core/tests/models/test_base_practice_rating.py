"""
Tests for BasePracticeRating abstract base class.

Verifies that all concrete implementations inherit the shared functionality
correctly and maintain database constraints.
"""

from characters.models.mage.focus import Practice
from characters.models.mage.mage import Mage, PracticeRating
from django.core.exceptions import ValidationError
from django.test import TestCase
from locations.models.mage.reality_zone import RealityZone, ZoneRating


class TestBasePracticeRatingInheritance(TestCase):
    """Test that all concrete implementations inherit from BasePracticeRating."""

    def test_practicerating_inherits_base(self):
        """Test PracticeRating inherits from BasePracticeRating."""
        from core.models import BasePracticeRating

        self.assertTrue(issubclass(PracticeRating, BasePracticeRating))

    def test_zonerating_inherits_base(self):
        """Test ZoneRating inherits from BasePracticeRating."""
        from core.models import BasePracticeRating

        self.assertTrue(issubclass(ZoneRating, BasePracticeRating))


class TestBasePracticeRatingSharedFields(TestCase):
    """Test shared fields inherited from BasePracticeRating."""

    @classmethod
    def setUpTestData(cls):
        cls.practice = Practice.objects.create(name="Test Practice")

    def test_practice_fk_on_practicerating(self):
        """Test PracticeRating has practice FK from base class."""
        mage = Mage.objects.create(name="Test Mage")
        rating = PracticeRating.objects.create(
            mage=mage, practice=self.practice, rating=3
        )
        self.assertEqual(rating.practice, self.practice)

    def test_practice_fk_on_zonerating(self):
        """Test ZoneRating has practice FK from base class."""
        zone = RealityZone.objects.create(name="Test Zone")
        rating = ZoneRating.objects.create(zone=zone, practice=self.practice, rating=5)
        self.assertEqual(rating.practice, self.practice)

    def test_practice_fk_allows_null(self):
        """Test practice FK allows null (inherited SET_NULL behavior)."""
        mage = Mage.objects.create(name="Test Mage")
        rating = PracticeRating.objects.create(mage=mage, practice=None, rating=0)
        self.assertIsNone(rating.practice)

        zone = RealityZone.objects.create(name="Test Zone")
        zone_rating = ZoneRating.objects.create(zone=zone, practice=None, rating=0)
        self.assertIsNone(zone_rating.practice)


class TestPracticeRatingValidation(TestCase):
    """Test rating validation for PracticeRating (0-10 range)."""

    @classmethod
    def setUpTestData(cls):
        cls.practice = Practice.objects.create(name="Test Practice")
        cls.mage = Mage.objects.create(name="Test Mage")

    def test_rating_default_is_zero(self):
        """Test default rating is 0."""
        rating = PracticeRating.objects.create(mage=self.mage, practice=self.practice)
        self.assertEqual(rating.rating, 0)

    def test_rating_at_min_boundary(self):
        """Test rating at 0 is valid."""
        rating = PracticeRating(mage=self.mage, practice=self.practice, rating=0)
        rating.full_clean()  # Should not raise
        rating.save()
        self.assertEqual(rating.rating, 0)

    def test_rating_at_max_boundary(self):
        """Test rating at 10 is valid."""
        rating = PracticeRating(mage=self.mage, practice=self.practice, rating=10)
        rating.full_clean()  # Should not raise
        rating.save()
        self.assertEqual(rating.rating, 10)

    def test_rating_below_min_fails_validation(self):
        """Test rating below 0 fails validation."""
        rating = PracticeRating(mage=self.mage, practice=self.practice, rating=-1)
        with self.assertRaises(ValidationError):
            rating.full_clean()

    def test_rating_above_max_fails_validation(self):
        """Test rating above 10 fails validation."""
        rating = PracticeRating(mage=self.mage, practice=self.practice, rating=11)
        with self.assertRaises(ValidationError):
            rating.full_clean()


class TestZoneRatingValidation(TestCase):
    """Test rating validation for ZoneRating (-10 to 10 range)."""

    @classmethod
    def setUpTestData(cls):
        cls.practice = Practice.objects.create(name="Test Practice")
        cls.zone = RealityZone.objects.create(name="Test Zone")

    def test_rating_default_is_zero(self):
        """Test default rating is 0."""
        rating = ZoneRating.objects.create(zone=self.zone, practice=self.practice)
        self.assertEqual(rating.rating, 0)

    def test_rating_at_min_boundary(self):
        """Test rating at -10 is valid."""
        rating = ZoneRating(zone=self.zone, practice=self.practice, rating=-10)
        rating.full_clean()  # Should not raise
        rating.save()
        self.assertEqual(rating.rating, -10)

    def test_rating_at_max_boundary(self):
        """Test rating at 10 is valid."""
        rating = ZoneRating(zone=self.zone, practice=self.practice, rating=10)
        rating.full_clean()  # Should not raise
        rating.save()
        self.assertEqual(rating.rating, 10)

    def test_rating_positive_in_range(self):
        """Test positive ratings in range work."""
        rating = ZoneRating.objects.create(
            zone=self.zone, practice=self.practice, rating=5
        )
        self.assertEqual(rating.rating, 5)

    def test_rating_negative_in_range(self):
        """Test negative ratings in range work."""
        rating = ZoneRating.objects.create(
            zone=self.zone, practice=self.practice, rating=-5
        )
        self.assertEqual(rating.rating, -5)

    def test_rating_below_min_fails_validation(self):
        """Test rating below -10 fails validation."""
        rating = ZoneRating(zone=self.zone, practice=self.practice, rating=-11)
        with self.assertRaises(ValidationError):
            rating.full_clean()

    def test_rating_above_max_fails_validation(self):
        """Test rating above 10 fails validation."""
        rating = ZoneRating(zone=self.zone, practice=self.practice, rating=11)
        with self.assertRaises(ValidationError):
            rating.full_clean()


class TestPracticeRatingStrMethod(TestCase):
    """Test __str__ method for PracticeRating."""

    @classmethod
    def setUpTestData(cls):
        cls.practice = Practice.objects.create(name="High Ritual Magick")
        cls.mage = Mage.objects.create(name="Test Mage")

    def test_str_with_mage_and_practice(self):
        """Test __str__ with both mage and practice set."""
        rating = PracticeRating.objects.create(
            mage=self.mage, practice=self.practice, rating=3
        )
        expected = f"{self.mage.name}: {self.practice}: 3"
        self.assertEqual(str(rating), expected)

    def test_str_without_mage(self):
        """Test __str__ when mage is None."""
        rating = PracticeRating.objects.create(
            mage=None, practice=self.practice, rating=5
        )
        expected = f"No Mage: {self.practice}: 5"
        self.assertEqual(str(rating), expected)

    def test_str_without_practice(self):
        """Test __str__ when practice is None."""
        rating = PracticeRating.objects.create(
            mage=self.mage, practice=None, rating=2
        )
        expected = f"{self.mage.name}: No Practice: 2"
        self.assertEqual(str(rating), expected)


class TestZoneRatingMetaOptions(TestCase):
    """Test ZoneRating Meta options."""

    def test_verbose_name(self):
        """Test verbose_name is set correctly."""
        self.assertEqual(ZoneRating._meta.verbose_name, "Reality Zone Rating")

    def test_verbose_name_plural(self):
        """Test verbose_name_plural is set correctly."""
        self.assertEqual(ZoneRating._meta.verbose_name_plural, "Reality Zone Ratings")
