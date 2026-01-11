"""Tests for Trod views."""

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from locations.models.changeling import Trod


class TrodListViewTest(TestCase):
    """Tests for TrodListView."""

    def setUp(self):
        self.client = Client()
        self.url = reverse("locations:changeling:list:trod")

    def test_list_view_returns_200(self):
        """Test that the list view returns a 200 response."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_list_view_uses_correct_template(self):
        """Test that list view uses the correct template."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "locations/changeling/trod/list.html")

    def test_list_view_shows_trods(self):
        """Test that the list view shows existing trods."""
        trod = Trod.objects.create(
            name="Silver Path",
            trod_type="silver_path",
        )
        response = self.client.get(self.url)
        self.assertContains(response, "Silver Path")

    def test_list_view_shows_empty_message(self):
        """Test that the list view shows empty message when no trods exist."""
        response = self.client.get(self.url)
        self.assertContains(response, "No trods have been created yet")

    def test_list_view_has_create_link(self):
        """Test that the list view has a link to create new trods."""
        response = self.client.get(self.url)
        self.assertContains(response, "Create New Trod")
        self.assertContains(response, reverse("locations:changeling:create:trod"))


class TrodCreateViewTest(TestCase):
    """Tests for TrodCreateView."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.url = reverse("locations:changeling:create:trod")

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
        self.assertTemplateUsed(response, "locations/changeling/trod/form.html")

    def test_create_trod_success(self):
        """Test successful creation of a trod."""
        self.client.login(username="testuser", password="password")
        data = {
            "name": "New Trod",
            "description": "A test trod",
            "trod_type": "silver_path",
            "origin_name": "The Oak",
            "destination_name": "The Glade",
            "strength": 3,
            "difficulty": 4,
            "is_two_way": True,
            "is_stable": True,
            "glamour_cost": 1,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(Trod.objects.count(), 1)
        trod = Trod.objects.first()
        self.assertEqual(trod.name, "New Trod")
        # The redirect goes to the detail view, follow the redirect
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, trod.get_absolute_url())


class TrodDetailViewTest(TestCase):
    """Tests for TrodDetailView."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password", is_staff=True
        )
        self.trod = Trod.objects.create(
            name="Test Trod",
            trod_type="rath",
        )

    def test_detail_view_returns_200(self):
        """Test that the detail view returns 200 for staff users."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.trod.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_detail_view_shows_trod_info(self):
        """Test that the detail view shows trod information."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.trod.get_absolute_url())
        self.assertContains(response, "Test Trod")


class TrodUpdateViewTest(TestCase):
    """Tests for TrodUpdateView."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password", is_staff=True
        )
        self.trod = Trod.objects.create(
            name="Test Trod",
            trod_type="silver_path",
        )

    def test_update_view_returns_200_for_staff(self):
        """Test that the update view returns 200 for staff users."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.trod.get_update_url())
        self.assertEqual(response.status_code, 200)

    def test_update_view_uses_correct_template(self):
        """Test that update view uses the correct template."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.trod.get_update_url())
        self.assertTemplateUsed(response, "locations/changeling/trod/form.html")

    def test_update_trod_success(self):
        """Test successful update of a trod."""
        self.client.login(username="testuser", password="password")
        data = {
            "name": "Updated Trod",
            "description": "Updated description",
            "trod_type": "rath",
            "strength": 4,
            "difficulty": 5,
            "is_two_way": False,
            "is_stable": True,
            "glamour_cost": 2,
        }
        response = self.client.post(self.trod.get_update_url(), data)
        self.trod.refresh_from_db()
        self.assertEqual(self.trod.name, "Updated Trod")
        self.assertEqual(self.trod.trod_type, "rath")
