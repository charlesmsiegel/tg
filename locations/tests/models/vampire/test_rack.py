"""Tests for Rack model."""

from django.contrib.auth.models import User
from django.test import TestCase
from game.models import Chronicle
from locations.models.vampire.rack import Rack


class TestRackModel(TestCase):
    """Test Rack model methods and properties."""

    def setUp(self):
        self.rack = Rack.objects.create(name="Test Rack")

    def test_rack_type(self):
        """Test rack type is correctly set."""
        self.assertEqual(self.rack.type, "rack")

    def test_rack_gameline(self):
        """Test rack gameline is vtm."""
        self.assertEqual(self.rack.gameline, "vtm")

    def test_get_heading(self):
        """Test get_heading returns vtm_heading."""
        self.assertEqual(self.rack.get_heading(), "vtm_heading")

    def test_default_quality(self):
        """Test default quality is 1."""
        self.assertEqual(self.rack.quality, 1)

    def test_default_population_density(self):
        """Test default population density is 1."""
        self.assertEqual(self.rack.population_density, 1)

    def test_default_risk_level(self):
        """Test default risk level is 3."""
        self.assertEqual(self.rack.risk_level, 3)

    def test_default_is_protected(self):
        """Test default is_protected is False."""
        self.assertFalse(self.rack.is_protected)

    def test_default_is_exclusive(self):
        """Test default is_exclusive is False."""
        self.assertFalse(self.rack.is_exclusive)

    def test_default_is_contested(self):
        """Test default is_contested is False."""
        self.assertFalse(self.rack.is_contested)

    def test_default_masquerade_risk(self):
        """Test default masquerade risk is 3."""
        self.assertEqual(self.rack.masquerade_risk, 3)


class TestRackTotalValue(TestCase):
    """Test get_total_value method."""

    def test_basic_value_calculation(self):
        """Test basic value calculation."""
        rack = Rack.objects.create(
            name="Test",
            quality=3,
            population_density=2,
            risk_level=3,  # Average risk, no penalty
        )
        # 3 + 2 - 0 = 5
        self.assertEqual(rack.get_total_value(), 5)

    def test_value_with_low_risk(self):
        """Test value increases with low risk."""
        rack = Rack.objects.create(
            name="Test", quality=3, population_density=2, risk_level=1  # Very safe
        )
        # 3 + 2 - (1-3) = 3 + 2 + 2 = 7
        self.assertEqual(rack.get_total_value(), 7)

    def test_value_with_high_risk(self):
        """Test value decreases with high risk."""
        rack = Rack.objects.create(
            name="Test",
            quality=3,
            population_density=2,
            risk_level=5,  # Very dangerous
        )
        # 3 + 2 - (5-3) = 3 + 2 - 2 = 3
        self.assertEqual(rack.get_total_value(), 3)

    def test_value_with_protected(self):
        """Test value increases when protected."""
        rack = Rack.objects.create(
            name="Test",
            quality=3,
            population_density=2,
            risk_level=3,
            is_protected=True,
        )
        # 3 + 2 + 1 = 6
        self.assertEqual(rack.get_total_value(), 6)

    def test_value_with_exclusive(self):
        """Test value increases when exclusive."""
        rack = Rack.objects.create(
            name="Test",
            quality=3,
            population_density=2,
            risk_level=3,
            is_exclusive=True,
        )
        # 3 + 2 + 1 = 6
        self.assertEqual(rack.get_total_value(), 6)

    def test_value_with_contested(self):
        """Test value decreases when contested."""
        rack = Rack.objects.create(
            name="Test",
            quality=3,
            population_density=2,
            risk_level=3,
            is_contested=True,
        )
        # 3 + 2 - 1 = 4
        self.assertEqual(rack.get_total_value(), 4)

    def test_value_minimum_is_zero(self):
        """Test value doesn't go below 0."""
        rack = Rack.objects.create(
            name="Test",
            quality=1,
            population_density=1,
            risk_level=5,
            is_contested=True,
        )
        # 1 + 1 - 2 - 1 = -1 -> 0
        self.assertEqual(rack.get_total_value(), 0)

    def test_value_with_all_bonuses(self):
        """Test value with all bonuses."""
        rack = Rack.objects.create(
            name="Test",
            quality=5,
            population_density=5,
            risk_level=1,  # +2 from low risk
            is_protected=True,  # +1
            is_exclusive=True,  # +1
        )
        # 5 + 5 + 2 + 1 + 1 = 14
        self.assertEqual(rack.get_total_value(), 14)


class TestRackViews(TestCase):
    """Test Rack views."""

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.rack = Rack.objects.create(
            name="Test Rack",
            owner=self.user,
            status="App",
        )

    def test_detail_view_status_code(self):
        """Test detail view returns 200."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.rack.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_detail_view_template(self):
        """Test detail view uses correct template."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.rack.get_absolute_url())
        self.assertTemplateUsed(response, "locations/vampire/rack/detail.html")

    def test_create_view_status_code(self):
        """Test create view returns 200."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(Rack.get_creation_url())
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        """Test create view uses correct template."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(Rack.get_creation_url())
        self.assertTemplateUsed(response, "locations/vampire/rack/form.html")


class TestRackUpdateView(TestCase):
    """Test Rack update view."""

    def setUp(self):
        self.st = User.objects.create_user(username="st_user", password="password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.chronicle.storytellers.add(self.st)
        self.rack = Rack.objects.create(
            name="Test Rack",
            owner=self.st,
            chronicle=self.chronicle,
            status="App",
        )

    def test_update_view_status_code(self):
        """Test update view returns 200."""
        self.client.login(username="st_user", password="password")
        response = self.client.get(self.rack.get_update_url())
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        """Test update view uses correct template."""
        self.client.login(username="st_user", password="password")
        response = self.client.get(self.rack.get_update_url())
        self.assertTemplateUsed(response, "locations/vampire/rack/form.html")
