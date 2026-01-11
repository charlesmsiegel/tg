"""Tests for DreamRealm views."""

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from locations.models.changeling import DreamRealm


class DreamRealmListViewTest(TestCase):
    """Tests for DreamRealmListView."""

    def setUp(self):
        self.client = Client()
        self.url = reverse("locations:changeling:list:dream_realm")

    def test_list_view_returns_200(self):
        """Test that the list view returns a 200 response."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_list_view_uses_correct_template(self):
        """Test that list view uses the correct template."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "locations/changeling/dream_realm/list.html")

    def test_list_view_shows_dream_realms(self):
        """Test that the list view shows existing dream realms."""
        realm = DreamRealm.objects.create(
            name="Crystal Gardens",
            depth="far",
            realm_type="mythic",
        )
        response = self.client.get(self.url)
        self.assertContains(response, "Crystal Gardens")

    def test_list_view_shows_empty_message(self):
        """Test that the list view shows empty message when no dream realms exist."""
        response = self.client.get(self.url)
        self.assertContains(response, "No dream realms have been created yet")

    def test_list_view_has_create_link(self):
        """Test that the list view has a link to create new dream realms."""
        response = self.client.get(self.url)
        self.assertContains(response, "Create New Dream Realm")
        self.assertContains(response, reverse("locations:changeling:create:dream_realm"))


class DreamRealmCreateViewTest(TestCase):
    """Tests for DreamRealmCreateView."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.url = reverse("locations:changeling:create:dream_realm")

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
        self.assertTemplateUsed(response, "locations/changeling/dream_realm/form.html")

    def test_create_dream_realm_success(self):
        """Test successful creation of a dream realm."""
        self.client.login(username="testuser", password="password")
        data = {
            "name": "New Realm",
            "description": "A test realm",
            "depth": "near",
            "realm_type": "collective",
            "stability": 3,
            "accessibility": 3,
            "exit_difficulty": 3,
            "glamour_level": 5,
            "provides_glamour": True,
            "time_flow": "normal",
            "is_mutable": True,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(DreamRealm.objects.count(), 1)
        realm = DreamRealm.objects.first()
        self.assertEqual(realm.name, "New Realm")
        # The redirect goes to the detail view, follow the redirect
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, realm.get_absolute_url())


class DreamRealmDetailViewTest(TestCase):
    """Tests for DreamRealmDetailView."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password", is_staff=True
        )
        self.realm = DreamRealm.objects.create(
            name="Test Realm",
            depth="deep",
            realm_type="nightmare",
        )

    def test_detail_view_returns_200(self):
        """Test that the detail view returns 200 for staff users."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.realm.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_detail_view_shows_realm_info(self):
        """Test that the detail view shows dream realm information."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.realm.get_absolute_url())
        self.assertContains(response, "Test Realm")


class DreamRealmUpdateViewTest(TestCase):
    """Tests for DreamRealmUpdateView."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password", is_staff=True
        )
        self.realm = DreamRealm.objects.create(
            name="Test Realm",
            depth="near",
            realm_type="collective",
        )

    def test_update_view_returns_200_for_staff(self):
        """Test that the update view returns 200 for staff users."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.realm.get_update_url())
        self.assertEqual(response.status_code, 200)

    def test_update_view_uses_correct_template(self):
        """Test that update view uses the correct template."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.realm.get_update_url())
        self.assertTemplateUsed(response, "locations/changeling/dream_realm/form.html")

    def test_update_dream_realm_success(self):
        """Test successful update of a dream realm."""
        self.client.login(username="testuser", password="password")
        data = {
            "name": "Updated Realm",
            "description": "Updated description",
            "depth": "far",
            "realm_type": "mythic",
            "stability": 4,
            "accessibility": 2,
            "exit_difficulty": 5,
            "glamour_level": 7,
            "provides_glamour": False,
            "time_flow": "slower",
            "is_mutable": False,
        }
        response = self.client.post(self.realm.get_update_url(), data)
        self.realm.refresh_from_db()
        self.assertEqual(self.realm.name, "Updated Realm")
        self.assertEqual(self.realm.depth, "far")
