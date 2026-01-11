"""Tests for Passion model."""

from django.contrib.auth.models import User
from django.test import TestCase

from characters.models.wraith.passion import Passion
from characters.models.wraith.wraith import Wraith


class PassionTestCase(TestCase):
    """Base test case with common setup for Passion tests."""

    def setUp(self):
        """Create test user and wraith."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.wraith = Wraith.objects.create(name="Test Wraith", owner=self.user)


class TestPassionModel(PassionTestCase):
    """Tests for Passion model creation and attributes."""

    def test_passion_creation(self):
        """Passion can be created with required attributes."""
        passion = Passion.objects.create(
            wraith=self.wraith,
            emotion="Love",
            description="Protect my sister at all costs",
            rating=4,
        )
        self.assertEqual(passion.wraith, self.wraith)
        self.assertEqual(passion.emotion, "Love")
        self.assertEqual(passion.description, "Protect my sister at all costs")
        self.assertEqual(passion.rating, 4)

    def test_passion_default_values(self):
        """Passion has correct default values."""
        passion = Passion.objects.create(
            wraith=self.wraith,
            emotion="Rage",
            description="Test passion",
        )
        self.assertEqual(passion.rating, 1)
        self.assertFalse(passion.is_dark_passion)

    def test_passion_can_be_dark(self):
        """Passion can be marked as a dark passion."""
        passion = Passion.objects.create(
            wraith=self.wraith,
            emotion="Hatred",
            description="Destroy the living",
            is_dark_passion=True,
        )
        self.assertTrue(passion.is_dark_passion)


class TestPassionStrRepresentation(PassionTestCase):
    """Tests for Passion string representation."""

    def test_passion_str(self):
        """Passion string includes emotion, description, and rating."""
        passion = Passion.objects.create(
            wraith=self.wraith,
            emotion="Grief",
            description="Mourn my lost family",
            rating=3,
        )
        self.assertEqual(str(passion), "Grief: Mourn my lost family (3)")


class TestPassionRelationship(PassionTestCase):
    """Tests for Passion-Wraith relationship."""

    def test_wraith_related_name(self):
        """Passion is accessible via wraith.passions."""
        passion = Passion.objects.create(
            wraith=self.wraith,
            emotion="Fear",
            description="Test passion",
        )
        self.assertIn(passion, self.wraith.passions.all())

    def test_deleting_wraith_deletes_passions(self):
        """Deleting a wraith cascades to delete its passions."""
        passion = Passion.objects.create(
            wraith=self.wraith,
            emotion="Fear",
            description="Test passion",
        )
        passion_id = passion.id
        self.wraith.delete()
        self.assertFalse(Passion.objects.filter(id=passion_id).exists())

    def test_multiple_passions_per_wraith(self):
        """A wraith can have multiple passions."""
        passion1 = Passion.objects.create(
            wraith=self.wraith,
            emotion="Love",
            description="Family",
        )
        passion2 = Passion.objects.create(
            wraith=self.wraith,
            emotion="Rage",
            description="Murder",
        )
        passion3 = Passion.objects.create(
            wraith=self.wraith,
            emotion="Fear",
            description="Being forgotten",
        )
        self.assertEqual(self.wraith.passions.count(), 3)


class TestPassionDarkConversion(PassionTestCase):
    """Tests for converting passions to dark passions."""

    def test_convert_passion_to_dark(self):
        """Regular passion can be converted to dark passion."""
        passion = Passion.objects.create(
            wraith=self.wraith,
            emotion="Love",
            description="Family",
        )
        self.assertFalse(passion.is_dark_passion)

        passion.is_dark_passion = True
        passion.save()
        passion.refresh_from_db()
        self.assertTrue(passion.is_dark_passion)

    def test_mix_of_regular_and_dark_passions(self):
        """Wraith can have both regular and dark passions."""
        regular = Passion.objects.create(
            wraith=self.wraith,
            emotion="Love",
            description="Family",
            is_dark_passion=False,
        )
        dark = Passion.objects.create(
            wraith=self.wraith,
            emotion="Hatred",
            description="Enemies",
            is_dark_passion=True,
        )
        regular_passions = Passion.objects.filter(wraith=self.wraith, is_dark_passion=False)
        dark_passions = Passion.objects.filter(wraith=self.wraith, is_dark_passion=True)
        self.assertEqual(regular_passions.count(), 1)
        self.assertEqual(dark_passions.count(), 1)


class TestPassionMetaOptions(PassionTestCase):
    """Tests for Passion Meta options."""

    def test_verbose_name(self):
        """Passion has correct verbose_name."""
        self.assertEqual(Passion._meta.verbose_name, "Passion")

    def test_verbose_name_plural(self):
        """Passion has correct verbose_name_plural."""
        self.assertEqual(Passion._meta.verbose_name_plural, "Passions")


class TestPassionRatings(PassionTestCase):
    """Tests for Passion rating functionality."""

    def test_passion_rating_values(self):
        """Passion ratings can range from 1 to higher values."""
        for rating in [1, 2, 3, 4, 5]:
            passion = Passion.objects.create(
                wraith=self.wraith,
                emotion=f"Test{rating}",
                description=f"Rating {rating} passion",
                rating=rating,
            )
            self.assertEqual(passion.rating, rating)

    def test_wraith_total_passion_rating_calculation(self):
        """Wraith can calculate total passion ratings."""
        Passion.objects.create(
            wraith=self.wraith,
            emotion="Love",
            description="Family",
            rating=3,
        )
        Passion.objects.create(
            wraith=self.wraith,
            emotion="Rage",
            description="Murder",
            rating=4,
        )
        total = sum(p.rating for p in Passion.objects.filter(wraith=self.wraith))
        self.assertEqual(total, 7)
