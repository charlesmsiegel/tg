"""Tests for Fetter model."""

from django.contrib.auth.models import User
from django.test import TestCase

from characters.models.wraith.fetter import Fetter
from characters.models.wraith.wraith import Wraith


class FetterTestCase(TestCase):
    """Base test case with common setup for Fetter tests."""

    def setUp(self):
        """Create test user and wraith."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.wraith = Wraith.objects.create(name="Test Wraith", owner=self.user)


class TestFetterModel(FetterTestCase):
    """Tests for Fetter model creation and attributes."""

    def test_fetter_creation(self):
        """Fetter can be created with required attributes."""
        fetter = Fetter.objects.create(
            wraith=self.wraith,
            fetter_type="object",
            description="My wedding ring",
            rating=3,
        )
        self.assertEqual(fetter.wraith, self.wraith)
        self.assertEqual(fetter.fetter_type, "object")
        self.assertEqual(fetter.description, "My wedding ring")
        self.assertEqual(fetter.rating, 3)

    def test_fetter_default_values(self):
        """Fetter has correct default values."""
        fetter = Fetter.objects.create(
            wraith=self.wraith,
            description="Test fetter",
        )
        self.assertEqual(fetter.fetter_type, "object")
        self.assertEqual(fetter.rating, 1)

    def test_fetter_type_choices(self):
        """Fetter can have object, location, or person type."""
        object_fetter = Fetter.objects.create(
            wraith=self.wraith,
            fetter_type="object",
            description="Ring",
        )
        location_fetter = Fetter.objects.create(
            wraith=self.wraith,
            fetter_type="location",
            description="Old house",
        )
        person_fetter = Fetter.objects.create(
            wraith=self.wraith,
            fetter_type="person",
            description="My daughter",
        )
        self.assertEqual(object_fetter.fetter_type, "object")
        self.assertEqual(location_fetter.fetter_type, "location")
        self.assertEqual(person_fetter.fetter_type, "person")


class TestFetterStrRepresentation(FetterTestCase):
    """Tests for Fetter string representation."""

    def test_fetter_str(self):
        """Fetter string includes description and rating."""
        fetter = Fetter.objects.create(
            wraith=self.wraith,
            description="My childhood home",
            rating=4,
        )
        self.assertEqual(str(fetter), "My childhood home (4)")


class TestFetterRelationship(FetterTestCase):
    """Tests for Fetter-Wraith relationship."""

    def test_wraith_related_name(self):
        """Fetter is accessible via wraith.fetters."""
        fetter = Fetter.objects.create(
            wraith=self.wraith,
            description="Test fetter",
        )
        self.assertIn(fetter, self.wraith.fetters.all())

    def test_deleting_wraith_deletes_fetters(self):
        """Deleting a wraith cascades to delete its fetters."""
        fetter = Fetter.objects.create(
            wraith=self.wraith,
            description="Test fetter",
        )
        fetter_id = fetter.id
        self.wraith.delete()
        self.assertFalse(Fetter.objects.filter(id=fetter_id).exists())

    def test_multiple_fetters_per_wraith(self):
        """A wraith can have multiple fetters."""
        fetter1 = Fetter.objects.create(
            wraith=self.wraith,
            fetter_type="object",
            description="Ring",
        )
        fetter2 = Fetter.objects.create(
            wraith=self.wraith,
            fetter_type="location",
            description="House",
        )
        fetter3 = Fetter.objects.create(
            wraith=self.wraith,
            fetter_type="person",
            description="Child",
        )
        self.assertEqual(self.wraith.fetters.count(), 3)


class TestFetterMetaOptions(FetterTestCase):
    """Tests for Fetter Meta options."""

    def test_verbose_name(self):
        """Fetter has correct verbose_name."""
        self.assertEqual(Fetter._meta.verbose_name, "Fetter")

    def test_verbose_name_plural(self):
        """Fetter has correct verbose_name_plural."""
        self.assertEqual(Fetter._meta.verbose_name_plural, "Fetters")
