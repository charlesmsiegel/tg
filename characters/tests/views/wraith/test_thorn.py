"""Tests for thorn views module."""

from characters.models.wraith.thorn import Thorn
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse


class TestThornDetailView(TestCase):
    """Test ThornDetailView functionality."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.thorn = Thorn.objects.create(
            name="Test Thorn",
            description="A test thorn",
            point_cost=2,
            thorn_type="individual",
        )

    def test_detail_view_accessible(self):
        """Test that thorn detail view is accessible."""
        url = reverse("characters:wraith:thorn", kwargs={"pk": self.thorn.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_detail_view_uses_correct_template(self):
        """Test that correct template is used for thorn detail view."""
        url = reverse("characters:wraith:thorn", kwargs={"pk": self.thorn.pk})
        response = self.client.get(url)
        self.assertTemplateUsed(response, "characters/wraith/thorn/detail.html")

    def test_detail_view_returns_404_for_invalid_pk(self):
        """Test that detail view returns 404 for non-existent thorn."""
        url = reverse("characters:wraith:thorn", kwargs={"pk": 99999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class TestThornCreateView(TestCase):
    """Test ThornCreateView functionality."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )

    def test_create_view_accessible_when_logged_in(self):
        """Test that thorn create view is accessible when logged in."""
        self.client.login(username="testuser", password="password")
        url = reverse("characters:wraith:create:thorn")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_uses_correct_template(self):
        """Test that correct template is used for thorn create view."""
        self.client.login(username="testuser", password="password")
        url = reverse("characters:wraith:create:thorn")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "characters/wraith/thorn/form.html")

    def test_create_view_requires_login(self):
        """Test that thorn create view requires login."""
        url = reverse("characters:wraith:create:thorn")
        response = self.client.get(url)
        # App returns 401 for unauthenticated users instead of redirect
        self.assertEqual(response.status_code, 401)

    def test_create_thorn_successfully(self):
        """Test creating a thorn successfully."""
        self.client.login(username="testuser", password="password")
        url = reverse("characters:wraith:create:thorn")
        data = {
            "name": "New Thorn",
            "description": "A new thorn",
            "thorn_type": "individual",
            "point_cost": 3,
            "activation_cost": "",
            "activation_trigger": "",
            "mechanical_description": "",
            "resistance_system": "",
            "resistance_difficulty": "",
            "duration": "",
            "frequency_limitation": "",
            "limitations": "",
        }
        response = self.client.post(url, data)
        # Should redirect on success
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Thorn.objects.filter(name="New Thorn").exists())


class TestThornUpdateView(TestCase):
    """Test ThornUpdateView functionality."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.thorn = Thorn.objects.create(
            name="Test Thorn",
            description="A test thorn",
            point_cost=2,
            thorn_type="individual",
        )

    def test_update_view_accessible_when_logged_in(self):
        """Test that thorn update view is accessible when logged in."""
        self.client.login(username="testuser", password="password")
        url = reverse("characters:wraith:update:thorn", kwargs={"pk": self.thorn.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_uses_correct_template(self):
        """Test that correct template is used for thorn update view."""
        self.client.login(username="testuser", password="password")
        url = reverse("characters:wraith:update:thorn", kwargs={"pk": self.thorn.pk})
        response = self.client.get(url)
        self.assertTemplateUsed(response, "characters/wraith/thorn/form.html")

    def test_update_view_returns_404_for_invalid_pk(self):
        """Test that update view returns 404 for non-existent thorn."""
        self.client.login(username="testuser", password="password")
        url = reverse("characters:wraith:update:thorn", kwargs={"pk": 99999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_update_thorn_successfully(self):
        """Test updating a thorn successfully."""
        self.client.login(username="testuser", password="password")
        url = reverse("characters:wraith:update:thorn", kwargs={"pk": self.thorn.pk})
        data = {
            "name": "Updated Thorn",
            "description": "Updated description",
            "thorn_type": "collective",
            "point_cost": 4,
            "activation_cost": "",
            "activation_trigger": "",
            "mechanical_description": "",
            "resistance_system": "",
            "resistance_difficulty": "",
            "duration": "",
            "frequency_limitation": "",
            "limitations": "",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.thorn.refresh_from_db()
        self.assertEqual(self.thorn.name, "Updated Thorn")


class TestThornListView(TestCase):
    """Test ThornListView functionality."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        # Create thorns with different point costs
        Thorn.objects.create(name="Thorn 1", point_cost=1, thorn_type="individual")
        Thorn.objects.create(name="Thorn 2", point_cost=2, thorn_type="individual")
        Thorn.objects.create(name="Thorn 3", point_cost=3, thorn_type="collective")

    def test_list_view_accessible(self):
        """Test that thorn list view is accessible."""
        url = reverse("characters:wraith:list:thorn")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_list_view_uses_correct_template(self):
        """Test that correct template is used for thorn list view."""
        url = reverse("characters:wraith:list:thorn")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "characters/wraith/thorn/list.html")

    def test_list_view_has_point_costs_in_context(self):
        """Test that point_costs are in the context for filtering."""
        url = reverse("characters:wraith:list:thorn")
        response = self.client.get(url)
        self.assertIn("point_costs", response.context)

    def test_list_view_point_costs_are_sorted(self):
        """Test that point_costs in context are sorted."""
        url = reverse("characters:wraith:list:thorn")
        response = self.client.get(url)
        point_costs = response.context["point_costs"]
        self.assertEqual(list(point_costs), sorted(point_costs))

    def test_list_view_shows_all_thorns(self):
        """Test that list view shows all thorns."""
        url = reverse("characters:wraith:list:thorn")
        response = self.client.get(url)
        self.assertEqual(len(response.context["object_list"]), 3)
