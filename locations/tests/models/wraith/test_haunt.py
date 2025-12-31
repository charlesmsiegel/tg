"""Tests for Haunt model."""

from django.contrib.auth.models import User
from django.test import TestCase
from game.models import Chronicle
from locations.models.wraith.haunt import Haunt


class TestHauntBasics(TestCase):
    """Test basic Haunt model functionality."""

    def test_haunt_creation(self):
        """Test creating a haunt."""
        haunt = Haunt.objects.create(
            name="Old Cemetery",
            rank=3,
            shroud_rating=3,
            haunt_type="sacred_site",
        )
        self.assertEqual(haunt.name, "Old Cemetery")
        self.assertEqual(haunt.rank, 3)
        self.assertEqual(haunt.shroud_rating, 3)
        self.assertEqual(haunt.haunt_type, "sacred_site")
        self.assertEqual(haunt.type, "haunt")
        self.assertEqual(haunt.gameline, "wto")

    def test_haunt_defaults(self):
        """Test haunt default values."""
        haunt = Haunt.objects.create(name="Test Haunt")
        self.assertEqual(haunt.rank, 1)
        self.assertEqual(haunt.shroud_rating, 5)
        self.assertEqual(haunt.haunt_type, "sacred_site")
        self.assertEqual(haunt.haunt_size, "single_room")
        self.assertEqual(haunt.faith_resonance, "")
        self.assertTrue(haunt.attracts_ghosts)

    def test_haunt_str(self):
        """Test haunt string representation."""
        haunt = Haunt.objects.create(name="The Morgue")
        self.assertEqual(str(haunt), "The Morgue (Haunt)")

    def test_haunt_get_heading(self):
        """Test get_heading returns wto_heading."""
        haunt = Haunt.objects.create(name="Test")
        self.assertEqual(haunt.get_heading(), "wto_heading")

    def test_haunt_get_absolute_url(self):
        """Test get_absolute_url returns valid URL."""
        haunt = Haunt.objects.create(name="Test")
        url = haunt.get_absolute_url()
        self.assertIn(str(haunt.pk), url)
        self.assertIn("haunt", url)

    def test_haunt_get_update_url(self):
        """Test get_update_url returns valid URL."""
        haunt = Haunt.objects.create(name="Test")
        url = haunt.get_update_url()
        self.assertIn(str(haunt.id), url)
        self.assertIn("haunt", url)

    def test_haunt_get_creation_url(self):
        """Test get_creation_url returns valid URL."""
        url = Haunt.get_creation_url()
        self.assertIn("haunt", url)


class TestHauntSetRank(TestCase):
    """Test Haunt set_rank method."""

    def test_set_rank_1(self):
        """Test set_rank for rank 1 sets shroud 5."""
        haunt = Haunt.objects.create(name="Test")
        result = haunt.set_rank(1)
        self.assertTrue(result)
        self.assertEqual(haunt.rank, 1)
        self.assertEqual(haunt.shroud_rating, 5)

    def test_set_rank_2(self):
        """Test set_rank for rank 2 sets shroud 4."""
        haunt = Haunt.objects.create(name="Test")
        result = haunt.set_rank(2)
        self.assertTrue(result)
        self.assertEqual(haunt.rank, 2)
        self.assertEqual(haunt.shroud_rating, 4)

    def test_set_rank_3(self):
        """Test set_rank for rank 3 sets shroud 3."""
        haunt = Haunt.objects.create(name="Test")
        result = haunt.set_rank(3)
        self.assertTrue(result)
        self.assertEqual(haunt.rank, 3)
        self.assertEqual(haunt.shroud_rating, 3)

    def test_set_rank_4(self):
        """Test set_rank for rank 4 sets shroud 2."""
        haunt = Haunt.objects.create(name="Test")
        result = haunt.set_rank(4)
        self.assertTrue(result)
        self.assertEqual(haunt.rank, 4)
        self.assertEqual(haunt.shroud_rating, 2)

    def test_set_rank_5(self):
        """Test set_rank for rank 5 sets shroud 1."""
        haunt = Haunt.objects.create(name="Test")
        result = haunt.set_rank(5)
        self.assertTrue(result)
        self.assertEqual(haunt.rank, 5)
        self.assertEqual(haunt.shroud_rating, 1)

    def test_set_rank_invalid(self):
        """Test set_rank for invalid rank uses default shroud 5."""
        haunt = Haunt.objects.create(name="Test")
        result = haunt.set_rank(10)
        self.assertTrue(result)
        self.assertEqual(haunt.rank, 10)
        self.assertEqual(haunt.shroud_rating, 5)


class TestHauntTypes(TestCase):
    """Test Haunt type choices."""

    def test_haunt_type_sacred_site(self):
        """Test sacred_site haunt type."""
        haunt = Haunt.objects.create(name="Test", haunt_type="sacred_site")
        self.assertEqual(haunt.haunt_type, "sacred_site")

    def test_haunt_type_battlefield(self):
        """Test battlefield haunt type."""
        haunt = Haunt.objects.create(name="Test", haunt_type="battlefield")
        self.assertEqual(haunt.haunt_type, "battlefield")

    def test_haunt_type_crime_scene(self):
        """Test crime_scene haunt type."""
        haunt = Haunt.objects.create(name="Test", haunt_type="crime_scene")
        self.assertEqual(haunt.haunt_type, "crime_scene")

    def test_haunt_type_sickroom(self):
        """Test sickroom haunt type."""
        haunt = Haunt.objects.create(name="Test", haunt_type="sickroom")
        self.assertEqual(haunt.haunt_type, "sickroom")

    def test_haunt_type_place_of_worship(self):
        """Test place_of_worship haunt type."""
        haunt = Haunt.objects.create(name="Test", haunt_type="place_of_worship")
        self.assertEqual(haunt.haunt_type, "place_of_worship")

    def test_haunt_type_place_of_tragedy(self):
        """Test place_of_tragedy haunt type."""
        haunt = Haunt.objects.create(name="Test", haunt_type="place_of_tragedy")
        self.assertEqual(haunt.haunt_type, "place_of_tragedy")

    def test_haunt_type_other(self):
        """Test other haunt type."""
        haunt = Haunt.objects.create(name="Test", haunt_type="other")
        self.assertEqual(haunt.haunt_type, "other")


class TestHauntSizes(TestCase):
    """Test Haunt size choices."""

    def test_haunt_size_single_room(self):
        """Test single_room size."""
        haunt = Haunt.objects.create(name="Test", haunt_size="single_room")
        self.assertEqual(haunt.haunt_size, "single_room")

    def test_haunt_size_apartment(self):
        """Test apartment size."""
        haunt = Haunt.objects.create(name="Test", haunt_size="apartment")
        self.assertEqual(haunt.haunt_size, "apartment")

    def test_haunt_size_house(self):
        """Test house size."""
        haunt = Haunt.objects.create(name="Test", haunt_size="house")
        self.assertEqual(haunt.haunt_size, "house")

    def test_haunt_size_mansion(self):
        """Test mansion size."""
        haunt = Haunt.objects.create(name="Test", haunt_size="mansion")
        self.assertEqual(haunt.haunt_size, "mansion")

    def test_haunt_size_estate(self):
        """Test estate size."""
        haunt = Haunt.objects.create(name="Test", haunt_size="estate")
        self.assertEqual(haunt.haunt_size, "estate")


class TestHauntFeatures(TestCase):
    """Test Haunt features."""

    def test_faith_resonance(self):
        """Test faith_resonance field."""
        haunt = Haunt.objects.create(
            name="Test",
            faith_resonance="Strong Catholic devotion",
        )
        self.assertEqual(haunt.faith_resonance, "Strong Catholic devotion")

    def test_attracts_ghosts_default(self):
        """Test attracts_ghosts defaults to True."""
        haunt = Haunt.objects.create(name="Test")
        self.assertTrue(haunt.attracts_ghosts)

    def test_attracts_ghosts_false(self):
        """Test attracts_ghosts can be False."""
        haunt = Haunt.objects.create(name="Test", attracts_ghosts=False)
        self.assertFalse(haunt.attracts_ghosts)


class TestHauntViews(TestCase):
    """Test Haunt views integration."""

    def test_haunt_list_view(self):
        """Test haunt list view."""
        Haunt.objects.create(name="Haunt 1")
        Haunt.objects.create(name="Haunt 2")
        response = self.client.get("/locations/wraith/list/haunt/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Haunt 1")
        self.assertContains(response, "Haunt 2")

    def test_haunt_detail_view(self):
        """Test haunt detail view."""
        user = User.objects.create_user(username="testuser", password="password")
        haunt = Haunt.objects.create(
            name="Test Haunt",
            rank=3,
            shroud_rating=3,
            owner=user,
            status="App",
        )
        self.client.login(username="testuser", password="password")
        response = self.client.get(haunt.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Haunt")

    def test_haunt_create_view(self):
        """Test haunt create view."""
        user = User.objects.create_user(username="testuser", password="password")
        self.client.login(username="testuser", password="password")
        response = self.client.get(Haunt.get_creation_url())
        self.assertEqual(response.status_code, 200)

    def test_haunt_create_post(self):
        """Test creating haunt via POST."""
        user = User.objects.create_user(username="testuser", password="password")
        self.client.login(username="testuser", password="password")
        data = {
            "name": "New Haunt",
            "description": "A new haunt",
            "rank": 4,
            "shroud_rating": 2,
            "haunt_type": "battlefield",
            "haunt_size": "house",
            "faith_resonance": "War dead",
            "gauntlet": 5,
            "shroud": 5,
            "dimension_barrier": 5,
        }
        response = self.client.post(Haunt.get_creation_url(), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Haunt.objects.filter(name="New Haunt").exists())
        haunt = Haunt.objects.get(name="New Haunt")
        self.assertEqual(haunt.rank, 4)
        self.assertEqual(haunt.shroud_rating, 2)

    def test_haunt_update_view(self):
        """Test haunt update view."""
        st = User.objects.create_user(username="st_user", password="password")
        chronicle = Chronicle.objects.create(name="Test Chronicle")
        chronicle.storytellers.add(st)
        haunt = Haunt.objects.create(
            name="Existing Haunt",
            rank=2,
            shroud_rating=4,
            owner=st,
            chronicle=chronicle,
            status="App",
        )
        self.client.login(username="st_user", password="password")
        response = self.client.get(haunt.get_update_url())
        self.assertEqual(response.status_code, 200)

    def test_haunt_update_post(self):
        """Test updating haunt via POST."""
        st = User.objects.create_user(username="st_user", password="password")
        chronicle = Chronicle.objects.create(name="Test Chronicle")
        chronicle.storytellers.add(st)
        haunt = Haunt.objects.create(
            name="Existing Haunt",
            rank=2,
            shroud_rating=4,
            owner=st,
            chronicle=chronicle,
            status="App",
        )
        self.client.login(username="st_user", password="password")
        data = {
            "name": "Updated Haunt",
            "description": "Updated description",
            "rank": 5,
            "shroud_rating": 1,
            "haunt_type": "place_of_tragedy",
            "haunt_size": "mansion",
            "gauntlet": 5,
            "shroud": 5,
            "dimension_barrier": 5,
        }
        response = self.client.post(haunt.get_update_url(), data=data)
        self.assertEqual(response.status_code, 302)
        haunt.refresh_from_db()
        self.assertEqual(haunt.name, "Updated Haunt")
        self.assertEqual(haunt.rank, 5)
        self.assertEqual(haunt.shroud_rating, 1)


class TestHauntMeta(TestCase):
    """Test Haunt Meta class."""

    def test_verbose_name(self):
        """Test verbose name."""
        self.assertEqual(Haunt._meta.verbose_name, "Haunt")

    def test_verbose_name_plural(self):
        """Test verbose name plural."""
        self.assertEqual(Haunt._meta.verbose_name_plural, "Haunts")

    def test_ordering(self):
        """Test ordering by name."""
        Haunt.objects.create(name="Zeta Haunt")
        Haunt.objects.create(name="Alpha Haunt")
        Haunt.objects.create(name="Beta Haunt")
        haunts = list(Haunt.objects.all())
        self.assertEqual(haunts[0].name, "Alpha Haunt")
        self.assertEqual(haunts[1].name, "Beta Haunt")
        self.assertEqual(haunts[2].name, "Zeta Haunt")
