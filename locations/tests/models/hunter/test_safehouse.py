"""Tests for Safehouse model."""

from django.contrib.auth.models import User
from django.test import TestCase

from game.models import Chronicle
from locations.models.hunter.safehouse import Safehouse


class TestSafehouseBasics(TestCase):
    """Test basic Safehouse model functionality."""

    def test_safehouse_creation(self):
        """Test creating a safehouse."""
        safehouse = Safehouse.objects.create(
            name="The Bunker",
            size=3,
            security_level=4,
            armory_level=3,
        )
        self.assertEqual(safehouse.name, "The Bunker")
        self.assertEqual(safehouse.size, 3)
        self.assertEqual(safehouse.security_level, 4)
        self.assertEqual(safehouse.armory_level, 3)
        self.assertEqual(safehouse.type, "safehouse")
        self.assertEqual(safehouse.gameline, "htr")

    def test_safehouse_defaults(self):
        """Test safehouse default values."""
        safehouse = Safehouse.objects.create(name="Test Safehouse")
        self.assertEqual(safehouse.size, 1)
        self.assertEqual(safehouse.capacity, 5)
        self.assertEqual(safehouse.security_level, 1)
        self.assertEqual(safehouse.armory_level, 0)
        self.assertEqual(safehouse.surveillance_level, 0)
        self.assertEqual(safehouse.medical_facilities, 0)
        self.assertFalse(safehouse.is_compromised)
        self.assertFalse(safehouse.is_mobile)
        self.assertFalse(safehouse.has_panic_room)
        self.assertFalse(safehouse.has_escape_routes)
        self.assertFalse(safehouse.has_dead_drop)
        self.assertTrue(safehouse.has_communications)
        self.assertEqual(safehouse.cover_story, "")
        self.assertEqual(safehouse.legal_owner, "")

    def test_safehouse_get_heading(self):
        """Test get_heading returns htr_heading."""
        safehouse = Safehouse.objects.create(name="Test")
        self.assertEqual(safehouse.get_heading(), "htr_heading")

    def test_safehouse_get_update_url(self):
        """Test get_update_url returns valid URL."""
        safehouse = Safehouse.objects.create(name="Test")
        url = safehouse.get_update_url()
        self.assertIn(str(safehouse.id), url)
        self.assertIn("safehouse", url)

    def test_safehouse_get_creation_url(self):
        """Test get_creation_url returns valid URL."""
        url = Safehouse.get_creation_url()
        self.assertIn("safehouse", url)


class TestSafehouseTotalRating(TestCase):
    """Test Safehouse total rating calculation."""

    def test_calculate_total_rating_basic(self):
        """Test basic total rating calculation."""
        safehouse = Safehouse.objects.create(
            name="Test",
            size=2,
            security_level=3,
            armory_level=1,
            surveillance_level=2,
            medical_facilities=1,
        )
        # Total = 2 + 3 + 1 + 2 + 1 = 9
        self.assertEqual(safehouse.total_rating, 9)

    def test_calculate_total_rating_with_features(self):
        """Test total rating with bonus features."""
        safehouse = Safehouse.objects.create(
            name="Test",
            size=2,
            security_level=2,
            armory_level=1,
            surveillance_level=1,
            medical_facilities=1,
            has_panic_room=True,  # +1
            has_escape_routes=True,  # +1
            has_dead_drop=True,  # +1
        )
        # Total = 2 + 2 + 1 + 1 + 1 + 1 + 1 + 1 = 10
        self.assertEqual(safehouse.total_rating, 10)

    def test_calculate_total_rating_compromised_penalty(self):
        """Test total rating with compromised penalty."""
        safehouse = Safehouse.objects.create(
            name="Test",
            size=2,
            security_level=2,
            armory_level=1,
            surveillance_level=1,
            medical_facilities=1,
            is_compromised=True,  # -2
        )
        # Total = 2 + 2 + 1 + 1 + 1 - 2 = 5
        self.assertEqual(safehouse.total_rating, 5)

    def test_calculate_total_rating_features_and_compromised(self):
        """Test total rating with both features and compromised."""
        safehouse = Safehouse.objects.create(
            name="Test",
            size=2,
            security_level=2,
            armory_level=1,
            surveillance_level=1,
            medical_facilities=1,
            has_panic_room=True,  # +1
            has_escape_routes=True,  # +1
            is_compromised=True,  # -2
        )
        # Total = 2 + 2 + 1 + 1 + 1 + 1 + 1 - 2 = 7
        self.assertEqual(safehouse.total_rating, 7)

    def test_calculate_total_rating_no_negative(self):
        """Test total rating cannot go negative."""
        safehouse = Safehouse.objects.create(
            name="Test",
            size=1,
            security_level=1,
            armory_level=0,
            surveillance_level=0,
            medical_facilities=0,
            is_compromised=True,  # -2
        )
        # Total = 1 + 1 + 0 + 0 + 0 - 2 = 0 (clamped)
        self.assertEqual(safehouse.total_rating, 0)

    def test_save_recalculates_total_rating(self):
        """Test save() recalculates total rating."""
        safehouse = Safehouse.objects.create(
            name="Test",
            size=1,
            security_level=1,
            armory_level=0,
        )
        self.assertEqual(safehouse.total_rating, 2)

        safehouse.size = 3
        safehouse.security_level = 4
        safehouse.armory_level = 3
        safehouse.has_panic_room = True
        safehouse.save()
        safehouse.refresh_from_db()
        self.assertEqual(safehouse.total_rating, 11)  # 3 + 4 + 3 + 1


class TestSafehouseFeatures(TestCase):
    """Test Safehouse special features."""

    def test_is_compromised(self):
        """Test is_compromised feature."""
        safehouse = Safehouse.objects.create(name="Test", is_compromised=True)
        self.assertTrue(safehouse.is_compromised)

    def test_is_mobile(self):
        """Test is_mobile feature."""
        safehouse = Safehouse.objects.create(name="Test", is_mobile=True)
        self.assertTrue(safehouse.is_mobile)

    def test_has_panic_room(self):
        """Test has_panic_room feature."""
        safehouse = Safehouse.objects.create(name="Test", has_panic_room=True)
        self.assertTrue(safehouse.has_panic_room)

    def test_has_escape_routes(self):
        """Test has_escape_routes feature."""
        safehouse = Safehouse.objects.create(name="Test", has_escape_routes=True)
        self.assertTrue(safehouse.has_escape_routes)

    def test_has_dead_drop(self):
        """Test has_dead_drop feature."""
        safehouse = Safehouse.objects.create(name="Test", has_dead_drop=True)
        self.assertTrue(safehouse.has_dead_drop)

    def test_has_communications(self):
        """Test has_communications feature (default True)."""
        safehouse = Safehouse.objects.create(name="Test")
        self.assertTrue(safehouse.has_communications)

    def test_cover_story(self):
        """Test cover_story field."""
        safehouse = Safehouse.objects.create(
            name="Test",
            cover_story="Abandoned warehouse rented for storage",
        )
        self.assertEqual(safehouse.cover_story, "Abandoned warehouse rented for storage")

    def test_legal_owner(self):
        """Test legal_owner field."""
        safehouse = Safehouse.objects.create(
            name="Test",
            legal_owner="Shell Corporation LLC",
        )
        self.assertEqual(safehouse.legal_owner, "Shell Corporation LLC")


class TestSafehouseViews(TestCase):
    """Test Safehouse views integration."""

    def test_safehouse_list_view(self):
        """Test safehouse list view."""
        Safehouse.objects.create(name="Safehouse 1")
        Safehouse.objects.create(name="Safehouse 2")
        response = self.client.get("/locations/hunter/safehouse/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Safehouse 1")
        self.assertContains(response, "Safehouse 2")

    def test_safehouse_detail_view(self):
        """Test safehouse detail view."""
        user = User.objects.create_user(username="testuser", password="password")
        safehouse = Safehouse.objects.create(
            name="Test Safehouse",
            size=3,
            security_level=4,
            owner=user,
            status="App",
        )
        self.client.login(username="testuser", password="password")
        response = self.client.get(safehouse.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Safehouse")

    def test_safehouse_create_view(self):
        """Test safehouse create view."""
        user = User.objects.create_user(username="testuser", password="password")
        self.client.login(username="testuser", password="password")
        response = self.client.get(Safehouse.get_creation_url())
        self.assertEqual(response.status_code, 200)

    def test_safehouse_create_post(self):
        """Test creating safehouse via POST."""
        user = User.objects.create_user(username="testuser", password="password")
        self.client.login(username="testuser", password="password")
        data = {
            "name": "New Safehouse",
            "description": "A new safehouse",
            "size": 2,
            "capacity": 6,
            "security_level": 3,
            "armory_level": 2,
            "surveillance_level": 1,
            "medical_facilities": 1,
            "gauntlet": 5,
            "shroud": 5,
            "dimension_barrier": 5,
        }
        response = self.client.post(Safehouse.get_creation_url(), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Safehouse.objects.filter(name="New Safehouse").exists())
        safehouse = Safehouse.objects.get(name="New Safehouse")
        self.assertEqual(safehouse.total_rating, 9)  # 2 + 3 + 2 + 1 + 1

    def test_safehouse_update_view(self):
        """Test safehouse update view."""
        st = User.objects.create_user(username="st_user", password="password")
        chronicle = Chronicle.objects.create(name="Test Chronicle")
        chronicle.storytellers.add(st)
        safehouse = Safehouse.objects.create(
            name="Existing Safehouse",
            size=2,
            security_level=2,
            owner=st,
            chronicle=chronicle,
            status="App",
        )
        self.client.login(username="st_user", password="password")
        response = self.client.get(safehouse.get_update_url())
        self.assertEqual(response.status_code, 200)

    def test_safehouse_update_post(self):
        """Test updating safehouse via POST."""
        st = User.objects.create_user(username="st_user", password="password")
        chronicle = Chronicle.objects.create(name="Test Chronicle")
        chronicle.storytellers.add(st)
        safehouse = Safehouse.objects.create(
            name="Existing Safehouse",
            size=2,
            security_level=2,
            owner=st,
            chronicle=chronicle,
            status="App",
        )
        self.client.login(username="st_user", password="password")
        data = {
            "name": "Updated Safehouse",
            "description": "Updated description",
            "size": 4,
            "capacity": 8,
            "security_level": 5,
            "armory_level": 4,
            "surveillance_level": 3,
            "medical_facilities": 2,
            "has_panic_room": True,
            "has_escape_routes": True,
            "gauntlet": 5,
            "shroud": 5,
            "dimension_barrier": 5,
        }
        response = self.client.post(safehouse.get_update_url(), data=data)
        self.assertEqual(response.status_code, 302)
        safehouse.refresh_from_db()
        self.assertEqual(safehouse.name, "Updated Safehouse")
        # 4 + 5 + 4 + 3 + 2 + 1 + 1 = 20
        self.assertEqual(safehouse.total_rating, 20)


class TestSafehouseMeta(TestCase):
    """Test Safehouse Meta class."""

    def test_verbose_name(self):
        """Test verbose name."""
        self.assertEqual(Safehouse._meta.verbose_name, "Safehouse")

    def test_verbose_name_plural(self):
        """Test verbose name plural."""
        self.assertEqual(Safehouse._meta.verbose_name_plural, "Safehouses")
