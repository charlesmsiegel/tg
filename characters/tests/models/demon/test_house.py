"""Tests for DemonHouse model."""

from characters.models.demon.house import DemonHouse
from django.contrib.auth.models import User
from django.test import TestCase


class DemonHouseModelTests(TestCase):
    """Tests for DemonHouse model functionality."""

    def setUp(self):
        """Create a test user for ownership."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.house = DemonHouse.objects.create(
            name="Devils",
            celestial_name="Namaru",
            starting_torment=4,
            domain="The domain of fire and inspiration",
            owner=self.user,
        )

    def test_type_is_house(self):
        """Test that type is 'house'."""
        self.assertEqual(self.house.type, "house")

    def test_gameline_is_dtf(self):
        """Test that gameline is 'dtf'."""
        self.assertEqual(self.house.gameline, "dtf")

    def test_str_representation(self):
        """Test string representation includes name and celestial name."""
        self.assertEqual(str(self.house), "Devils (Namaru)")

    def test_default_starting_torment(self):
        """Test default starting_torment is 3."""
        house = DemonHouse.objects.create(
            name="Test House",
            celestial_name="Test",
            owner=self.user,
        )
        self.assertEqual(house.starting_torment, 3)

    def test_default_domain(self):
        """Test default domain is empty."""
        house = DemonHouse.objects.create(
            name="Test House",
            celestial_name="Test2",
            owner=self.user,
        )
        self.assertEqual(house.domain, "")

    def test_celestial_name_unique(self):
        """Test that celestial_name must be unique."""
        from django.db import IntegrityError

        with self.assertRaises(IntegrityError):
            DemonHouse.objects.create(
                name="Other Devils",
                celestial_name="Namaru",  # Same celestial name
                owner=self.user,
            )

    def test_ordering_by_name(self):
        """Houses should be ordered by name by default."""
        house_c = DemonHouse.objects.create(
            name="Scourges", celestial_name="Asharu", owner=self.user
        )
        house_a = DemonHouse.objects.create(
            name="Defilers", celestial_name="Lammasu", owner=self.user
        )
        house_b = DemonHouse.objects.create(
            name="Malefactors", celestial_name="Annunaki", owner=self.user
        )

        houses = list(DemonHouse.objects.filter(pk__in=[house_a.pk, house_b.pk, house_c.pk]))

        self.assertEqual(houses[0], house_a)  # Defilers
        self.assertEqual(houses[1], house_b)  # Malefactors
        self.assertEqual(houses[2], house_c)  # Scourges

    def test_get_absolute_url(self):
        """Test get_absolute_url returns correct URL."""
        url = self.house.get_absolute_url()
        self.assertEqual(url, f"/characters/demon/house/{self.house.pk}/")

    def test_get_update_url(self):
        """Test get_update_url returns correct URL."""
        url = self.house.get_update_url()
        self.assertEqual(url, f"/characters/demon/update/house/{self.house.pk}/")

    def test_get_creation_url(self):
        """Test get_creation_url returns correct URL."""
        url = DemonHouse.get_creation_url()
        self.assertEqual(url, "/characters/demon/create/house/")

    def test_get_heading(self):
        """Test get_heading returns DTF heading."""
        self.assertEqual(self.house.get_heading(), "dtf_heading")


class DemonHouseVerboseNameTests(TestCase):
    """Tests for DemonHouse verbose names."""

    def test_verbose_name(self):
        """Test verbose_name is correct."""
        self.assertEqual(DemonHouse._meta.verbose_name, "House")

    def test_verbose_name_plural(self):
        """Test verbose_name_plural is correct."""
        self.assertEqual(DemonHouse._meta.verbose_name_plural, "Houses")


class DemonHouseSevenHousesTests(TestCase):
    """Tests for creating all seven canonical houses."""

    def setUp(self):
        """Create test user."""
        self.user = User.objects.create_user(username="testuser", password="testpass")

    def test_can_create_all_seven_houses(self):
        """Test that all seven canonical houses can be created."""
        houses = [
            ("Devils", "Namaru", 4),
            ("Scourges", "Asharu", 3),
            ("Malefactors", "Annunaki", 3),
            ("Fiends", "Neberu", 3),
            ("Defilers", "Lammasu", 3),
            ("Devourers", "Rabisu", 3),
            ("Slayers", "Halaku", 4),
        ]

        created_houses = []
        for name, celestial_name, starting_torment in houses:
            house = DemonHouse.objects.create(
                name=name,
                celestial_name=celestial_name,
                starting_torment=starting_torment,
                owner=self.user,
            )
            created_houses.append(house)

        self.assertEqual(len(created_houses), 7)
        self.assertEqual(DemonHouse.objects.count(), 7)

    def test_devils_have_higher_starting_torment(self):
        """Test that Devils (Namaru) start with higher torment."""
        devils = DemonHouse.objects.create(
            name="Devils",
            celestial_name="Namaru",
            starting_torment=4,
            owner=self.user,
        )
        scourges = DemonHouse.objects.create(
            name="Scourges",
            celestial_name="Asharu",
            starting_torment=3,
            owner=self.user,
        )

        self.assertGreater(devils.starting_torment, scourges.starting_torment)
