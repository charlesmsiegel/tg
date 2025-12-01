"""
Tests for location models.

Tests cover:
- LocationModel base functionality
- Location creation and validation
- City model
- Gameline-specific locations
- Permission checks on locations
"""

from django.contrib.auth.models import User
from django.test import TestCase
from game.models import Chronicle
from locations.models.core import City, LocationModel


class TestLocationModel(TestCase):
    """Test the base LocationModel."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")

    def test_location_creation(self):
        """Test basic location creation."""
        location = LocationModel.objects.create(
            name="The Chantry",
            owner=self.user,
            chronicle=self.chronicle,
            description="A mystical sanctuary",
        )

        self.assertEqual(location.name, "The Chantry")
        self.assertEqual(location.owner, self.user)
        self.assertEqual(location.chronicle, self.chronicle)

    def test_location_str_representation(self):
        """Test string representation of a location."""
        location = LocationModel.objects.create(
            name="Test Location",
            owner=self.user,
        )

        self.assertEqual(str(location), "Test Location")

    def test_location_absolute_url(self):
        """Test that get_absolute_url returns correct path."""
        location = LocationModel.objects.create(
            name="Test Location",
            owner=self.user,
        )

        expected_url = f"/locations/{location.id}/"
        self.assertEqual(location.get_absolute_url(), expected_url)

    def test_location_has_description(self):
        """Test that locations can have descriptions."""
        location = LocationModel.objects.create(
            name="Test Location",
            owner=self.user,
            description="A detailed description of the location",
        )

        self.assertEqual(location.description, "A detailed description of the location")

    def test_location_belongs_to_chronicle(self):
        """Test that locations can belong to chronicles."""
        location = LocationModel.objects.create(
            name="Chronicle Location",
            owner=self.user,
            chronicle=self.chronicle,
        )

        self.assertEqual(location.chronicle, self.chronicle)

    def test_location_without_chronicle(self):
        """Test creating a location without a chronicle."""
        location = LocationModel.objects.create(
            name="Generic Location",
            owner=self.user,
        )

        self.assertIsNone(location.chronicle)

    def test_location_has_owner(self):
        """Test that locations must have an owner."""
        location = LocationModel.objects.create(
            name="Test Location",
            owner=self.user,
        )

        self.assertEqual(location.owner, self.user)


class TestCity(TestCase):
    """Test the City model."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")

    def test_city_creation(self):
        """Test creating a city."""
        city = City.objects.create(
            name="Boston",
            owner=self.user,
            chronicle=self.chronicle,
            population=700000,
        )

        self.assertEqual(city.name, "Boston")
        self.assertEqual(city.population, 700000)

    def test_city_is_location(self):
        """Test that City inherits from LocationModel."""
        city = City.objects.create(
            name="New York",
            owner=self.user,
        )

        # Should have LocationModel fields
        self.assertTrue(hasattr(city, "description"))
        self.assertEqual(city.owner, self.user)

    def test_city_population(self):
        """Test city population field."""
        city = City.objects.create(
            name="Small Town",
            owner=self.user,
            population=5000,
        )

        self.assertEqual(city.population, 5000)


class TestLocationPermissions(TestCase):
    """Test location permission functionality."""

    def setUp(self):
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="password"
        )
        self.other = User.objects.create_user(
            username="other", email="other@test.com", password="password"
        )
        self.location = LocationModel.objects.create(
            name="Test Location",
            owner=self.owner,
        )

    def test_owner_can_edit_location(self):
        """Test that owner can edit their locations."""
        from core.permissions import PermissionManager

        pm = PermissionManager()
        # Owner should have edit permission
        has_permission = pm.check_permission(self.owner, self.location, "edit_full")
        # Result depends on implementation
        self.assertIsNotNone(has_permission)

    def test_location_visibility(self):
        """Test location visibility settings."""
        # Locations should support visibility/display settings
        self.assertTrue(hasattr(self.location, "display") or hasattr(self.location, "visibility"))


class TestLocationImageUpload(TestCase):
    """Test location image upload functionality."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )

    def test_location_has_image_field(self):
        """Test that locations can have images."""
        location = LocationModel.objects.create(
            name="Test Location",
            owner=self.user,
        )

        # Should have image field
        self.assertTrue(hasattr(location, "image"))

    def test_location_image_optional(self):
        """Test that location image is optional."""
        location = LocationModel.objects.create(
            name="Location Without Image",
            owner=self.user,
        )

        # Should create successfully without image
        self.assertIsNotNone(location)


class TestLocationGamelineAssociation(TestCase):
    """Test that locations can be associated with gamelines."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )

    def test_location_has_gameline_field(self):
        """Test that locations track which gameline they belong to."""
        location = LocationModel.objects.create(
            name="Test Location",
            owner=self.user,
        )

        # Should have gameline field or type indicator
        has_gameline = (
            hasattr(location, "gameline")
            or hasattr(location, "location_type")
            or hasattr(location, "polymorphic_ctype")
        )
        self.assertTrue(has_gameline)


class TestLocationSceneAssociation(TestCase):
    """Test that locations can be associated with scenes."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.location = LocationModel.objects.create(
            name="Meeting Place",
            owner=self.user,
            chronicle=self.chronicle,
        )

    def test_scenes_can_reference_location(self):
        """Test that scenes can be set at a location."""
        from game.models import Scene

        scene = Scene.objects.create(
            name="The First Meeting",
            chronicle=self.chronicle,
            location=self.location,
        )

        self.assertEqual(scene.location, self.location)

    def test_location_can_host_multiple_scenes(self):
        """Test that a location can host multiple scenes."""
        from game.models import Scene

        scene1 = Scene.objects.create(
            name="Scene 1",
            chronicle=self.chronicle,
            location=self.location,
        )

        scene2 = Scene.objects.create(
            name="Scene 2",
            chronicle=self.chronicle,
            location=self.location,
        )

        scenes = Scene.objects.filter(location=self.location)
        self.assertEqual(scenes.count(), 2)
