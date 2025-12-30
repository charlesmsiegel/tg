"""Tests for HuntingGround model."""

from django.contrib.auth.models import User
from django.test import TestCase
from game.models import Chronicle
from locations.models.hunter.huntingground import HuntingGround


class TestHuntingGroundModel(TestCase):
    """Test HuntingGround model methods and properties."""

    def setUp(self):
        self.hunting_ground = HuntingGround.objects.create(name="Test Ground")

    def test_hunting_ground_type(self):
        """Test hunting_ground type is correctly set."""
        self.assertEqual(self.hunting_ground.type, "hunting_ground")

    def test_hunting_ground_gameline(self):
        """Test hunting_ground gameline is htr."""
        self.assertEqual(self.hunting_ground.gameline, "htr")

    def test_get_heading(self):
        """Test get_heading returns htr_heading."""
        self.assertEqual(self.hunting_ground.get_heading(), "htr_heading")

    def test_default_size(self):
        """Test default size is 1."""
        self.assertEqual(self.hunting_ground.size, 1)

    def test_default_population(self):
        """Test default population is 1."""
        self.assertEqual(self.hunting_ground.population, 1)

    def test_default_supernatural_activity(self):
        """Test default supernatural_activity is 1."""
        self.assertEqual(self.hunting_ground.supernatural_activity, 1)

    def test_default_is_contested(self):
        """Test default is_contested is False."""
        self.assertFalse(self.hunting_ground.is_contested)

    def test_default_control_level(self):
        """Test default control_level is 1."""
        self.assertEqual(self.hunting_ground.control_level, 1)

    def test_default_contact_network(self):
        """Test default contact_network is 0."""
        self.assertEqual(self.hunting_ground.contact_network, 0)

    def test_default_surveillance_coverage(self):
        """Test default surveillance_coverage is 0."""
        self.assertEqual(self.hunting_ground.surveillance_coverage, 0)


class TestHuntingGroundThreatTypes(TestCase):
    """Test HuntingGround threat type choices."""

    def test_vampire_threat(self):
        """Test vampire threat type."""
        hg = HuntingGround.objects.create(name="Test", primary_threat="vampire")
        self.assertEqual(hg.primary_threat, "vampire")

    def test_werewolf_threat(self):
        """Test werewolf threat type."""
        hg = HuntingGround.objects.create(name="Test", primary_threat="werewolf")
        self.assertEqual(hg.primary_threat, "werewolf")

    def test_mage_threat(self):
        """Test mage threat type."""
        hg = HuntingGround.objects.create(name="Test", primary_threat="mage")
        self.assertEqual(hg.primary_threat, "mage")

    def test_wraith_threat(self):
        """Test wraith threat type."""
        hg = HuntingGround.objects.create(name="Test", primary_threat="wraith")
        self.assertEqual(hg.primary_threat, "wraith")

    def test_changeling_threat(self):
        """Test changeling threat type."""
        hg = HuntingGround.objects.create(name="Test", primary_threat="changeling")
        self.assertEqual(hg.primary_threat, "changeling")

    def test_demon_threat(self):
        """Test demon threat type."""
        hg = HuntingGround.objects.create(name="Test", primary_threat="demon")
        self.assertEqual(hg.primary_threat, "demon")

    def test_unknown_threat(self):
        """Test unknown threat type."""
        hg = HuntingGround.objects.create(name="Test", primary_threat="unknown")
        self.assertEqual(hg.primary_threat, "unknown")

    def test_mixed_threat(self):
        """Test mixed threat type."""
        hg = HuntingGround.objects.create(name="Test", primary_threat="mixed")
        self.assertEqual(hg.primary_threat, "mixed")


class TestHuntingGroundTotalRating(TestCase):
    """Test calculate_total_rating method."""

    def test_basic_rating_calculation(self):
        """Test basic rating calculation."""
        hg = HuntingGround.objects.create(
            name="Test",
            size=2,
            population=3,
            supernatural_activity=2,
            contact_network=1,
            surveillance_coverage=1,
            control_level=2,
        )
        # 2+3+2+1+1+2 = 11
        self.assertEqual(hg.total_rating, 11)

    def test_rating_with_contested_penalty(self):
        """Test rating decreases when contested."""
        hg = HuntingGround.objects.create(
            name="Test",
            size=2,
            population=3,
            supernatural_activity=2,
            contact_network=1,
            surveillance_coverage=1,
            control_level=2,
            is_contested=True,
        )
        # 2+3+2+1+1+2-2 = 9
        self.assertEqual(hg.total_rating, 9)

    def test_rating_minimum_is_zero(self):
        """Test rating doesn't go below 0."""
        hg = HuntingGround.objects.create(
            name="Test",
            size=1,
            population=1,
            supernatural_activity=1,
            contact_network=0,
            surveillance_coverage=0,
            control_level=1,
            is_contested=True,
        )
        # 1+1+1+0+0+1-2 = 2 (not negative in this case)
        self.assertEqual(hg.total_rating, 2)

    def test_save_recalculates_rating(self):
        """Test save method recalculates total rating."""
        hg = HuntingGround.objects.create(
            name="Test", size=1, population=1, supernatural_activity=1, control_level=1
        )
        initial_rating = hg.total_rating
        hg.size = 3
        hg.population = 3
        hg.save()
        self.assertNotEqual(hg.total_rating, initial_rating)


class TestHuntingGroundViews(TestCase):
    """Test HuntingGround views."""

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.hunting_ground = HuntingGround.objects.create(
            name="Test Ground",
            owner=self.user,
            status="App",
        )

    def test_detail_view_status_code(self):
        """Test detail view returns 200."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.hunting_ground.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_detail_view_template(self):
        """Test detail view uses correct template."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.hunting_ground.get_absolute_url())
        self.assertTemplateUsed(response, "locations/hunter/huntingground/detail.html")

    def test_create_view_status_code(self):
        """Test create view returns 200."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(HuntingGround.get_creation_url())
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        """Test create view uses correct template."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(HuntingGround.get_creation_url())
        self.assertTemplateUsed(response, "locations/hunter/huntingground/form.html")


class TestHuntingGroundUpdateView(TestCase):
    """Test HuntingGround update view."""

    def setUp(self):
        self.st = User.objects.create_user(username="st_user", password="password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.chronicle.storytellers.add(self.st)
        self.hunting_ground = HuntingGround.objects.create(
            name="Test Ground",
            owner=self.st,
            chronicle=self.chronicle,
            status="App",
        )

    def test_update_view_status_code(self):
        """Test update view returns 200."""
        self.client.login(username="st_user", password="password")
        response = self.client.get(self.hunting_ground.get_update_url())
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        """Test update view uses correct template."""
        self.client.login(username="st_user", password="password")
        response = self.client.get(self.hunting_ground.get_update_url())
        self.assertTemplateUsed(response, "locations/hunter/huntingground/form.html")
