"""Tests for Barrens model."""

from django.contrib.auth.models import User
from django.test import TestCase

from game.models import Chronicle
from locations.models.vampire.barrens import Barrens


class TestBarrensModel(TestCase):
    """Test Barrens model methods and properties."""

    def setUp(self):
        self.barrens = Barrens.objects.create(name="Test Barrens")

    def test_barrens_type(self):
        """Test barrens type is correctly set."""
        self.assertEqual(self.barrens.type, "barrens")

    def test_barrens_gameline(self):
        """Test barrens gameline is vtm."""
        self.assertEqual(self.barrens.gameline, "vtm")

    def test_get_heading(self):
        """Test get_heading returns vtm_heading."""
        self.assertEqual(self.barrens.get_heading(), "vtm_heading")

    def test_default_size(self):
        """Test default size is 1."""
        self.assertEqual(self.barrens.size, 1)

    def test_default_danger_level(self):
        """Test default danger level is 3."""
        self.assertEqual(self.barrens.danger_level, 3)

    def test_default_population_density(self):
        """Test default population density is 0."""
        self.assertEqual(self.barrens.population_density, 0)

    def test_default_is_contested(self):
        """Test default is_contested is True."""
        self.assertTrue(self.barrens.is_contested)

    def test_default_has_feeding_grounds(self):
        """Test default has_feeding_grounds is True."""
        self.assertTrue(self.barrens.has_feeding_grounds)

    def test_default_feeding_quality(self):
        """Test default feeding quality is 1."""
        self.assertEqual(self.barrens.feeding_quality, 1)

    def test_default_masquerade_threat(self):
        """Test default masquerade threat is 3."""
        self.assertEqual(self.barrens.masquerade_threat, 3)


class TestBarrensControlStatus(TestCase):
    """Test get_control_status method."""

    def test_unclaimed_territory(self):
        """Test unclaimed territory returns 'Unclaimed'."""
        barrens = Barrens.objects.create(name="Test", is_unclaimed=True, is_contested=False)
        self.assertEqual(barrens.get_control_status(), "Unclaimed")

    def test_anarch_territory(self):
        """Test Anarch territory returns 'Anarch'."""
        barrens = Barrens.objects.create(
            name="Test",
            is_anarch_territory=True,
            is_unclaimed=False,
            is_contested=False,
        )
        self.assertEqual(barrens.get_control_status(), "Anarch")

    def test_sabbat_territory(self):
        """Test Sabbat territory returns 'Sabbat'."""
        barrens = Barrens.objects.create(
            name="Test",
            is_sabbat_territory=True,
            is_unclaimed=False,
            is_anarch_territory=False,
            is_contested=False,
        )
        self.assertEqual(barrens.get_control_status(), "Sabbat")

    def test_contested_territory(self):
        """Test contested territory returns 'Contested'."""
        barrens = Barrens.objects.create(
            name="Test",
            is_contested=True,
            is_unclaimed=False,
            is_anarch_territory=False,
            is_sabbat_territory=False,
        )
        self.assertEqual(barrens.get_control_status(), "Contested")

    def test_named_faction_control(self):
        """Test named faction control returns faction name."""
        barrens = Barrens.objects.create(
            name="Test",
            controlling_faction="The Giovanni",
            is_contested=False,
            is_unclaimed=False,
            is_anarch_territory=False,
            is_sabbat_territory=False,
        )
        self.assertEqual(barrens.get_control_status(), "The Giovanni")

    def test_unknown_control(self):
        """Test unknown control returns 'Unknown'."""
        barrens = Barrens.objects.create(
            name="Test",
            is_contested=False,
            is_unclaimed=False,
            is_anarch_territory=False,
            is_sabbat_territory=False,
            controlling_faction="",
        )
        self.assertEqual(barrens.get_control_status(), "Unknown")


class TestBarrensViews(TestCase):
    """Test Barrens views."""

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.barrens = Barrens.objects.create(
            name="Test Barrens",
            owner=self.user,
            status="App",
        )

    def test_detail_view_status_code(self):
        """Test detail view returns 200."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.barrens.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_detail_view_template(self):
        """Test detail view uses correct template."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.barrens.get_absolute_url())
        self.assertTemplateUsed(response, "locations/vampire/barrens/detail.html")

    def test_create_view_status_code(self):
        """Test create view returns 200."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(Barrens.get_creation_url())
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        """Test create view uses correct template."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(Barrens.get_creation_url())
        self.assertTemplateUsed(response, "locations/vampire/barrens/form.html")


class TestBarrensUpdateView(TestCase):
    """Test Barrens update view."""

    def setUp(self):
        self.st = User.objects.create_user(username="st_user", password="password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.chronicle.storytellers.add(self.st)
        self.barrens = Barrens.objects.create(
            name="Test Barrens",
            owner=self.st,
            chronicle=self.chronicle,
            status="App",
        )

    def test_update_view_status_code(self):
        """Test update view returns 200."""
        self.client.login(username="st_user", password="password")
        response = self.client.get(self.barrens.get_update_url())
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        """Test update view uses correct template."""
        self.client.login(username="st_user", password="password")
        response = self.client.get(self.barrens.get_update_url())
        self.assertTemplateUsed(response, "locations/vampire/barrens/form.html")
