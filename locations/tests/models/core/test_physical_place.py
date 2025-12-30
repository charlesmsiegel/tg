from decimal import Decimal

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from game.models import Chronicle
from locations.models import LocationModel, PhysicalPlace
from locations.models.mage.node import Node
from locations.models.vampire.elysium import Elysium
from locations.models.wraith.haunt import Haunt


class TestPhysicalPlaceModel(TestCase):
    """Tests for the PhysicalPlace model."""

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.place = PhysicalPlace.objects.create(
            name="Pike Place Market",
            description="Historic public market in Seattle",
            address="85 Pike Street",
            city="Seattle",
            state="WA",
            country="USA",
            postal_code="98101",
            owner=self.user,
            chronicle=self.chronicle,
        )

    def test_physical_place_creation(self):
        """Test basic PhysicalPlace creation."""
        self.assertEqual(self.place.name, "Pike Place Market")
        self.assertEqual(self.place.city, "Seattle")
        self.assertEqual(self.place.state, "WA")

    def test_physical_place_str(self):
        """Test string representation."""
        self.assertEqual(str(self.place), "Pike Place Market")

    def test_get_full_address(self):
        """Test full address formatting."""
        address = self.place.get_full_address()
        self.assertIn("85 Pike Street", address)
        self.assertIn("Seattle", address)
        self.assertIn("WA", address)
        self.assertIn("98101", address)
        self.assertIn("USA", address)

    def test_get_full_address_partial(self):
        """Test full address with missing components."""
        place = PhysicalPlace.objects.create(
            name="Simple Place",
            city="Portland",
        )
        address = place.get_full_address()
        self.assertEqual(address, "Portland")

    def test_has_coordinates_false(self):
        """Test has_coordinates returns False when not set."""
        self.assertFalse(self.place.has_coordinates())

    def test_has_coordinates_true(self):
        """Test has_coordinates returns True when set."""
        self.place.latitude = Decimal("47.6097")
        self.place.longitude = Decimal("-122.3331")
        self.place.save()
        self.assertTrue(self.place.has_coordinates())

    def test_place_type_default(self):
        """Test default place type."""
        self.assertEqual(self.place.place_type, "building")

    def test_display_default(self):
        """Test default display value."""
        self.assertTrue(self.place.display)


class TestPhysicalPlaceValidation(TestCase):
    """Tests for PhysicalPlace validation."""

    def test_name_required(self):
        """Test that name is required."""
        place = PhysicalPlace(name="")
        with self.assertRaises(ValidationError) as context:
            place.full_clean()
        self.assertIn("name", context.exception.message_dict)

    def test_coordinates_must_be_paired(self):
        """Test that both latitude and longitude must be set together."""
        place = PhysicalPlace(
            name="Test Place",
            latitude=Decimal("47.6097"),
        )
        with self.assertRaises(ValidationError) as context:
            place.full_clean()
        self.assertIn("latitude", context.exception.message_dict)

    def test_latitude_range_validation(self):
        """Test latitude must be between -90 and 90."""
        place = PhysicalPlace(
            name="Test Place",
            latitude=Decimal("91.0"),
            longitude=Decimal("0.0"),
        )
        with self.assertRaises(ValidationError) as context:
            place.full_clean()
        self.assertIn("latitude", context.exception.message_dict)

    def test_longitude_range_validation(self):
        """Test longitude must be between -180 and 180."""
        place = PhysicalPlace(
            name="Test Place",
            latitude=Decimal("0.0"),
            longitude=Decimal("181.0"),
        )
        with self.assertRaises(ValidationError) as context:
            place.full_clean()
        self.assertIn("longitude", context.exception.message_dict)

    def test_valid_coordinates(self):
        """Test valid coordinate values pass validation."""
        place = PhysicalPlace(
            name="Test Place",
            latitude=Decimal("47.6097"),
            longitude=Decimal("-122.3331"),
        )
        place.full_clean()  # Should not raise


class TestPhysicalPlaceLocationRelationship(TestCase):
    """Tests for PhysicalPlace relationships with LocationModel."""

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.place = PhysicalPlace.objects.create(
            name="St. Mark's Cathedral",
            address="1245 10th Ave E",
            city="Seattle",
            state="WA",
        )

    def test_link_location_to_physical_place(self):
        """Test linking a LocationModel to a PhysicalPlace."""
        location = LocationModel.objects.create(
            name="St. Mark's Cathedral",
            physical_place=self.place,
        )
        self.assertEqual(location.physical_place, self.place)
        self.assertIn(location, self.place.locations.all())

    def test_multiple_locations_same_place(self):
        """Test multiple supernatural locations at the same physical place."""
        # A Mage Node at St. Mark's
        node = Node.objects.create(
            name="Faith Nexus",
            physical_place=self.place,
            rank=3,
        )

        # A Vampire Elysium at St. Mark's
        elysium = Elysium.objects.create(
            name="The Cathedral Elysium",
            physical_place=self.place,
            prestige=4,
        )

        # A Wraith Haunt at St. Mark's
        haunt = Haunt.objects.create(
            name="The Whispering Choir",
            physical_place=self.place,
            rank=2,
            faith_resonance="Echoes of prayer",
        )

        # All three should be linked
        locations = self.place.get_supernatural_locations()
        self.assertEqual(locations.count(), 3)
        self.assertIn(node, locations)
        self.assertIn(elysium, locations)
        self.assertIn(haunt, locations)

    def test_get_supernatural_locations_by_gameline(self):
        """Test grouping locations by gameline."""
        # Create locations from different gamelines
        node = Node.objects.create(
            name="Faith Nexus",
            physical_place=self.place,
            rank=3,
        )
        elysium = Elysium.objects.create(
            name="The Cathedral Elysium",
            physical_place=self.place,
            prestige=4,
        )
        haunt = Haunt.objects.create(
            name="The Whispering Choir",
            physical_place=self.place,
            rank=2,
            faith_resonance="Echoes of prayer",
        )

        by_gameline = self.place.get_supernatural_locations_by_gameline()

        self.assertIn("mta", by_gameline)
        self.assertIn("vtm", by_gameline)
        self.assertIn("wto", by_gameline)
        self.assertIn(node, by_gameline["mta"])
        self.assertIn(elysium, by_gameline["vtm"])
        self.assertIn(haunt, by_gameline["wto"])


class TestLocationModelSiblings(TestCase):
    """Tests for LocationModel sibling methods."""

    def setUp(self):
        self.place = PhysicalPlace.objects.create(
            name="The Waterfront",
            city="Seattle",
        )
        self.node = Node.objects.create(
            name="Tidal Node",
            physical_place=self.place,
            rank=2,
        )
        self.elysium = Elysium.objects.create(
            name="Harbor Elysium",
            physical_place=self.place,
            prestige=3,
        )
        self.haunt = Haunt.objects.create(
            name="Drowned Whispers",
            physical_place=self.place,
            rank=1,
            faith_resonance="The call of the deep",
        )

    def test_get_sibling_locations(self):
        """Test getting sibling locations at the same physical place."""
        siblings = self.node.get_sibling_locations()

        # Should include the elysium and haunt but not the node itself
        self.assertEqual(siblings.count(), 2)
        self.assertIn(self.elysium, siblings)
        self.assertIn(self.haunt, siblings)
        self.assertNotIn(self.node, siblings)

    def test_get_sibling_locations_no_physical_place(self):
        """Test sibling locations when no physical place is set."""
        orphan = LocationModel.objects.create(name="Unplaced Location")
        siblings = orphan.get_sibling_locations()
        self.assertEqual(siblings.count(), 0)

    def test_get_sibling_locations_single_location(self):
        """Test sibling locations when only one location at a place."""
        solo_place = PhysicalPlace.objects.create(name="Solo Place")
        solo_location = Node.objects.create(
            name="Solo Node",
            physical_place=solo_place,
            rank=1,
        )
        siblings = solo_location.get_sibling_locations()
        self.assertEqual(siblings.count(), 0)


class TestPhysicalPlaceUrls(TestCase):
    """Tests for PhysicalPlace URL methods."""

    def setUp(self):
        self.place = PhysicalPlace.objects.create(name="Test Place")

    def test_get_absolute_url(self):
        """Test get_absolute_url method."""
        url = self.place.get_absolute_url()
        self.assertEqual(url, f"/locations/physical-place/{self.place.id}/")

    def test_get_update_url(self):
        """Test get_update_url method."""
        url = self.place.get_update_url()
        self.assertEqual(url, f"/locations/update/physical-place/{self.place.id}/")

    def test_get_creation_url(self):
        """Test get_creation_url class method."""
        url = PhysicalPlace.get_creation_url()
        self.assertEqual(url, "/locations/create/physical-place/")
