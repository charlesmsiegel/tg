"""Tests for Holding views."""

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from locations.models.changeling import Holding


class HoldingListViewTest(TestCase):
    """Tests for HoldingListView."""

    def setUp(self):
        self.client = Client()
        self.url = reverse("locations:changeling:list:holding")

    def test_list_view_returns_200(self):
        """Test that the list view returns a 200 response."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_list_view_uses_correct_template(self):
        """Test that list view uses the correct template."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "locations/changeling/holding/list.html")

    def test_list_view_shows_holdings(self):
        """Test that the list view shows existing holdings."""
        holding = Holding.objects.create(
            name="Test Barony",
            rank="barony",
            court="seelie",
        )
        response = self.client.get(self.url)
        self.assertContains(response, "Test Barony")

    def test_list_view_shows_empty_message(self):
        """Test that the list view shows empty message when no holdings exist."""
        response = self.client.get(self.url)
        self.assertContains(response, "No holdings have been created yet")

    def test_list_view_has_create_link(self):
        """Test that the list view has a link to create new holdings."""
        response = self.client.get(self.url)
        self.assertContains(response, "Create New Holding")
        self.assertContains(response, reverse("locations:changeling:create:holding"))


class HoldingCreateViewTest(TestCase):
    """Tests for HoldingCreateView."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.url = reverse("locations:changeling:create:holding")

    def test_create_view_requires_login(self):
        """Test that the create view requires authentication."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)  # LoginRequiredMixin returns 401

    def test_create_view_returns_200_for_logged_in_user(self):
        """Test that the create view returns 200 for authenticated users."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_uses_correct_template(self):
        """Test that create view uses the correct template."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "locations/changeling/holding/form.html")

    def test_create_holding_success(self):
        """Test successful creation of a holding."""
        self.client.login(username="testuser", password="password")
        data = {
            "name": "New Barony",
            "description": "A test barony",
            "rank": "barony",
            "court": "seelie",
            "military_strength": 2,
            "wealth": 2,
            "stability": 3,
            "freehold_count": 1,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(Holding.objects.count(), 1)
        holding = Holding.objects.first()
        self.assertEqual(holding.name, "New Barony")
        # The redirect goes to the detail view, follow the redirect
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, holding.get_absolute_url())


class HoldingDetailViewTest(TestCase):
    """Tests for HoldingDetailView."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password", is_staff=True
        )
        self.holding = Holding.objects.create(
            name="Test Duchy",
            rank="duchy",
            court="unseelie",
        )

    def test_detail_view_returns_200(self):
        """Test that the detail view returns 200 for staff users."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.holding.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_detail_view_shows_holding_info(self):
        """Test that the detail view shows holding information."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.holding.get_absolute_url())
        self.assertContains(response, "Test Duchy")


class HoldingUpdateViewTest(TestCase):
    """Tests for HoldingUpdateView."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password", is_staff=True
        )
        self.holding = Holding.objects.create(
            name="Test Barony",
            rank="barony",
            court="seelie",
        )

    def test_update_view_returns_200_for_staff(self):
        """Test that the update view returns 200 for staff users."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.holding.get_update_url())
        self.assertEqual(response.status_code, 200)

    def test_update_view_uses_correct_template(self):
        """Test that update view uses the correct template."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.holding.get_update_url())
        self.assertTemplateUsed(response, "locations/changeling/holding/form.html")

    def test_update_holding_success(self):
        """Test successful update of a holding."""
        self.client.login(username="testuser", password="password")
        data = {
            "name": "Updated Barony",
            "description": "Updated description",
            "rank": "duchy",
            "court": "unseelie",
            "military_strength": 3,
            "wealth": 3,
            "stability": 4,
            "freehold_count": 2,
        }
        response = self.client.post(self.holding.get_update_url(), data)
        self.holding.refresh_from_db()
        self.assertEqual(self.holding.name, "Updated Barony")
        self.assertEqual(self.holding.rank, "duchy")
