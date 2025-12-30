from characters.models.mage.resonance import Resonance
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase
from game.models import Chronicle
from locations.models.mage.realm import (
    EnvironmentChoices,
    HorizonRealm,
    HorizonRealmResonanceRating,
    SizeChoices,
)


class TestHorizonRealmModel(TestCase):
    """Test HorizonRealm model fields and methods."""

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.realm = HorizonRealm.objects.create(
            name="Test Horizon Realm",
            owner=self.user,
        )

    def test_default_values(self):
        """Test that default values are set correctly."""
        self.assertEqual(self.realm.rank, 1)
        self.assertEqual(self.realm.build_points, 11)
        self.assertEqual(self.realm.base_maintenance, 1)
        self.assertEqual(self.realm.quintessence_maintenance, 1)
        self.assertEqual(self.realm.size, SizeChoices.SINGLE_ROOM)
        self.assertEqual(self.realm.environment, EnvironmentChoices.SAME_AS_CONNECTION)
        self.assertEqual(self.realm.access_points, 1)
        self.assertEqual(self.realm.plants, 0)
        self.assertEqual(self.realm.animals, 0)
        self.assertEqual(self.realm.people, 0)
        self.assertEqual(self.realm.ephemera, 0)
        self.assertEqual(self.realm.guardians, 0)
        self.assertEqual(self.realm.arcane, 0)

    def test_set_rank(self):
        """Test set_rank updates build_points and maintenance correctly."""
        # Test rank 1 (default)
        self.realm.set_rank(1)
        self.assertEqual(self.realm.rank, 1)
        self.assertEqual(self.realm.build_points, 11)
        self.assertEqual(self.realm.base_maintenance, 1)

        # Test rank 5
        self.realm.set_rank(5)
        self.assertEqual(self.realm.rank, 5)
        self.assertEqual(self.realm.build_points, 55)
        self.assertEqual(self.realm.base_maintenance, 5)

        # Test rank 10
        self.realm.set_rank(10)
        self.assertEqual(self.realm.rank, 10)
        self.assertEqual(self.realm.build_points, 150)
        self.assertEqual(self.realm.base_maintenance, 50)

    def test_structure_cost(self):
        """Test structure_cost calculation."""
        # Default: size=1 (5), environment=1 (3), access_points=1 (0)
        self.assertEqual(self.realm.structure_cost(), 8)

        # Change size to city (4)
        self.realm.size = SizeChoices.CITY
        self.assertEqual(self.realm.structure_cost(), 23)  # 4*5 + 1*3 + 0

        # Add more access points
        self.realm.access_points = 3
        self.assertEqual(self.realm.structure_cost(), 27)  # 4*5 + 1*3 + (3-1)*2

    def test_inhabitants_cost(self):
        """Test inhabitants_cost calculation."""
        # Default: all at 0
        self.assertEqual(self.realm.inhabitants_cost(), 0)

        # Set inhabitants
        self.realm.plants = 2  # 2*2 = 4
        self.realm.animals = 1  # 1*2 = 2
        self.realm.people = 3  # 3*5 = 15
        self.realm.ephemera = 2  # 2*4 = 8
        self.assertEqual(self.realm.inhabitants_cost(), 29)

    def test_security_cost(self):
        """Test security_cost calculation."""
        # Default: all at 0
        self.assertEqual(self.realm.security_cost(), 0)

        # Set security
        self.realm.guardians = 2  # 2*3 = 6
        self.realm.arcane = 3  # 3*2 = 6
        self.assertEqual(self.realm.security_cost(), 12)

    def test_total_cost(self):
        """Test total_cost calculation."""
        # Default structure cost is 8 (size=1*5, environment=1*3)
        self.assertEqual(self.realm.total_cost(), 8)

        # Add some traits
        self.realm.plants = 2
        self.realm.guardians = 1
        expected = 8 + 4 + 3  # structure + plants*2 + guardians*3
        self.assertEqual(self.realm.total_cost(), expected)

    def test_remaining_points(self):
        """Test remaining_points calculation."""
        # Rank 1 has 11 points, default structure cost is 8
        self.assertEqual(self.realm.remaining_points(), 3)

        # Set rank 5 (55 points)
        self.realm.set_rank(5)
        self.assertEqual(self.realm.remaining_points(), 47)


class TestHorizonRealmResonance(TestCase):
    """Test HorizonRealm resonance functionality."""

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.realm = HorizonRealm.objects.create(
            name="Test Horizon Realm",
            owner=self.user,
        )
        self.resonance = Resonance.objects.create(name="Dynamic")

    def test_add_resonance(self):
        """Test adding resonance to a realm."""
        result = self.realm.add_resonance(self.resonance)
        self.assertTrue(result)
        self.assertEqual(self.realm.resonance_rating(self.resonance), 1)

    def test_add_resonance_increases_rating(self):
        """Test that adding resonance multiple times increases the rating."""
        self.realm.add_resonance(self.resonance)
        self.realm.add_resonance(self.resonance)
        self.assertEqual(self.realm.resonance_rating(self.resonance), 2)

    def test_add_resonance_max_five(self):
        """Test that resonance cannot exceed 5."""
        for _ in range(5):
            self.realm.add_resonance(self.resonance)
        self.assertEqual(self.realm.resonance_rating(self.resonance), 5)

        # Try to add beyond 5
        result = self.realm.add_resonance(self.resonance)
        self.assertFalse(result)
        self.assertEqual(self.realm.resonance_rating(self.resonance), 5)

    def test_total_resonance(self):
        """Test total_resonance calculation."""
        res2 = Resonance.objects.create(name="Static")
        self.realm.add_resonance(self.resonance)
        self.realm.add_resonance(self.resonance)
        self.realm.add_resonance(res2)
        self.assertEqual(self.realm.total_resonance(), 3)

    def test_has_resonance(self):
        """Test has_resonance check against rank."""
        # Rank 1 needs at least 1 resonance
        self.assertFalse(self.realm.has_resonance())
        self.realm.add_resonance(self.resonance)
        self.assertTrue(self.realm.has_resonance())

        # Rank 3 needs at least 3 resonance
        self.realm.set_rank(3)
        self.assertFalse(self.realm.has_resonance())
        self.realm.add_resonance(self.resonance)
        self.realm.add_resonance(self.resonance)
        self.assertTrue(self.realm.has_resonance())


class TestHorizonRealmRankBuildPoints(TestCase):
    """Test the rank-to-build-points mapping."""

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.realm = HorizonRealm.objects.create(
            name="Test Horizon Realm",
            owner=self.user,
        )

    def test_rank_build_points_mapping(self):
        """Test all rank to build points mappings."""
        expected = {
            1: 11,
            2: 22,
            3: 33,
            4: 44,
            5: 55,
            6: 70,
            7: 85,
            8: 100,
            9: 115,
            10: 150,
        }
        for rank, points in expected.items():
            self.realm.set_rank(rank)
            self.assertEqual(self.realm.build_points, points, f"Rank {rank} should have {points} points")

    def test_rank_maintenance_mapping(self):
        """Test all rank to maintenance mappings."""
        expected = {
            1: 1,
            2: 2,
            3: 3,
            4: 4,
            5: 5,
            6: 10,
            7: 15,
            8: 20,
            9: 25,
            10: 50,
        }
        for rank, maintenance in expected.items():
            self.realm.set_rank(rank)
            self.assertEqual(
                self.realm.base_maintenance, maintenance, f"Rank {rank} should have {maintenance} maintenance"
            )


class TestHorizonRealmConstraints(TestCase):
    """Test database constraints on HorizonRealm."""

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")

    def test_rank_minimum_constraint(self):
        """Test that rank cannot be less than 1."""
        realm = HorizonRealm(name="Test", owner=self.user, rank=0)
        with self.assertRaises(ValidationError):
            realm.full_clean()

    def test_rank_maximum_constraint(self):
        """Test that rank cannot exceed 10."""
        realm = HorizonRealm(name="Test", owner=self.user, rank=11)
        with self.assertRaises(ValidationError):
            realm.full_clean()

    def test_plants_maximum_constraint(self):
        """Test that plants cannot exceed 5."""
        realm = HorizonRealm(name="Test", owner=self.user, plants=6)
        with self.assertRaises(ValidationError):
            realm.full_clean()

    def test_guardians_maximum_constraint(self):
        """Test that guardians cannot exceed 10."""
        realm = HorizonRealm(name="Test", owner=self.user, guardians=11)
        with self.assertRaises(ValidationError):
            realm.full_clean()


class TestHorizonRealmResonanceRatingConstraints(TestCase):
    """Test database constraints on HorizonRealmResonanceRating."""

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.realm = HorizonRealm.objects.create(name="Test", owner=self.user)
        self.resonance = Resonance.objects.create(name="Dynamic")

    def test_rating_minimum_constraint(self):
        """Test that resonance rating cannot be negative."""
        rating = HorizonRealmResonanceRating(
            horizon_realm=self.realm, resonance=self.resonance, rating=-1
        )
        with self.assertRaises(ValidationError):
            rating.full_clean()

    def test_rating_maximum_constraint(self):
        """Test that resonance rating cannot exceed 10."""
        rating = HorizonRealmResonanceRating(
            horizon_realm=self.realm, resonance=self.resonance, rating=11
        )
        with self.assertRaises(ValidationError):
            rating.full_clean()


class TestHorizonRealmDetailView(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="testuser", password="password")
        self.realm = HorizonRealm.objects.create(
            name="Test HorizonRealm",
            owner=self.user,
            status="App",
        )
        self.url = self.realm.get_absolute_url()

    def test_realm_detail_view_status_code(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_realm_detail_view_templates(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "locations/mage/realm/detail.html")


class TestHorizonRealmCreateView(TestCase):
    """Test HorizonRealm create view GET requests.

    Note: POST tests require complex form validation which is beyond the scope
    of basic CRUD view tests. GET tests verify accessibility.
    """

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.url = HorizonRealm.get_creation_url()

    def test_create_view_status_code(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "locations/mage/realm/form.html")


class TestHorizonRealmUpdateView(TestCase):
    """Test HorizonRealm update view GET requests.

    Note: POST tests require complex form validation which is beyond the scope
    of basic CRUD view tests. GET tests verify accessibility.
    """

    def setUp(self):
        self.st = User.objects.create_user(username="st_user", password="password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.chronicle.storytellers.add(self.st)
        self.realm = HorizonRealm.objects.create(
            name="Test HorizonRealm",
            description="Test description",
            owner=self.st,
            chronicle=self.chronicle,
            status="App",
        )
        self.url = self.realm.get_update_url()

    def test_update_view_status_code(self):
        self.client.login(username="st_user", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        self.client.login(username="st_user", password="password")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "locations/mage/realm/form.html")
