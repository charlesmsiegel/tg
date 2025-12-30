"""Tests for DtFHuman views."""

from characters.models.demon.dtf_human import DtFHuman
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from game.models import Chronicle


class TestDtFHumanDetailView(TestCase):
    """Test DtFHumanDetailView permissions and functionality."""

    def setUp(self):
        self.client = Client()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="password"
        )
        self.other_user = User.objects.create_user(
            username="other", email="other@test.com", password="password"
        )
        self.st = User.objects.create_user(
            username="st", email="st@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.chronicle.storytellers.add(self.st)

        self.human = DtFHuman.objects.create(
            name="Test Human",
            owner=self.owner,
            chronicle=self.chronicle,
            status="App",
        )

    def test_detail_view_accessible_to_owner(self):
        """Test that dtfhuman detail view is accessible to the owner."""
        self.client.login(username="owner", password="password")
        response = self.client.get(self.human.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_detail_view_accessible_to_st(self):
        """Test that dtfhuman detail view is accessible to storytellers."""
        self.client.login(username="st", password="password")
        response = self.client.get(self.human.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_detail_view_hidden_from_other_users(self):
        """Test that characters are hidden from other users (404)."""
        self.client.login(username="other", password="password")
        response = self.client.get(self.human.get_absolute_url())
        self.assertEqual(response.status_code, 404)

    def test_detail_view_returns_404_without_login(self):
        """Test that unauthenticated users get 404 (not login redirect)."""
        response = self.client.get(self.human.get_absolute_url())
        self.assertEqual(response.status_code, 404)

    def test_detail_view_template_used(self):
        """Test that correct template is used for dtfhuman detail view."""
        self.client.login(username="owner", password="password")
        response = self.client.get(self.human.get_absolute_url())
        self.assertTemplateUsed(response, "characters/demon/dtfhuman/detail.html")


class TestDtFHumanCreateView(TestCase):
    """Test DtFHumanCreateView functionality."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="user", email="user@test.com", password="password"
        )

    def test_create_view_accessible_when_logged_in(self):
        """Test that dtfhuman create view is accessible when logged in."""
        self.client.login(username="user", password="password")
        url = reverse("characters:demon:create:dtfhuman")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_redirects_when_not_logged_in(self):
        """Test that create view redirects when not logged in."""
        url = reverse("characters:demon:create:dtfhuman")
        response = self.client.get(url)
        self.assertIn(response.status_code, [302, 403])

    def test_create_view_has_get_success_url_method(self):
        """Test that DtFHumanCreateView has explicit get_success_url method."""
        from characters.views.demon.dtfhuman import DtFHumanCreateView

        self.assertTrue(
            hasattr(DtFHumanCreateView, "get_success_url"),
            "DtFHumanCreateView should have get_success_url method",
        )
        # Verify it's defined on the class itself, not inherited
        self.assertIn(
            "get_success_url",
            DtFHumanCreateView.__dict__,
            "get_success_url should be explicitly defined on DtFHumanCreateView",
        )


class TestDtFHumanUpdateView(TestCase):
    """Test DtFHumanUpdateView permissions and functionality."""

    def setUp(self):
        self.client = Client()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="password"
        )
        self.other_user = User.objects.create_user(
            username="other", email="other@test.com", password="password"
        )
        self.st = User.objects.create_user(
            username="st", email="st@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.chronicle.storytellers.add(self.st)

        self.human = DtFHuman.objects.create(
            name="Test Human",
            owner=self.owner,
            chronicle=self.chronicle,
            status="App",
        )

    def test_full_update_view_denied_to_owner(self):
        """Test that full update is denied to owners (ST-only)."""
        self.client.login(username="owner", password="password")
        url = reverse("characters:demon:update:dtfhuman_full", kwargs={"pk": self.human.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_full_update_view_accessible_to_st(self):
        """Test that full dtfhuman update view is accessible to storytellers."""
        self.client.login(username="st", password="password")
        url = reverse("characters:demon:update:dtfhuman_full", kwargs={"pk": self.human.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_full_update_view_denied_to_other_users(self):
        """Test that full dtfhuman update view is denied to other users."""
        self.client.login(username="other", password="password")
        url = reverse("characters:demon:update:dtfhuman_full", kwargs={"pk": self.human.pk})
        response = self.client.get(url)
        self.assertIn(response.status_code, [403, 302])


class TestDtFHumanListView(TestCase):
    """Test DtFHumanListView functionality."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="user", email="user@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")

    def test_list_view_accessible_when_logged_in(self):
        """Test that dtfhuman list view is accessible when logged in."""
        self.client.login(username="user", password="password")
        url = reverse("characters:demon:list:dtfhuman")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_list_view_shows_own_characters(self):
        """Test that list view shows user's own characters."""
        human = DtFHuman.objects.create(
            name="My Human", owner=self.user, status="App"
        )
        self.client.login(username="user", password="password")
        url = reverse("characters:demon:list:dtfhuman")
        response = self.client.get(url)
        self.assertContains(response, "My Human")


class TestDtFHuman404Handling(TestCase):
    """Test 404 error handling for dtfhuman views."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.chronicle.storytellers.add(self.user)

    def test_dtfhuman_detail_returns_404_for_invalid_pk(self):
        """Test that dtfhuman detail returns 404 for non-existent character."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(
            reverse("characters:demon:dtfhuman", kwargs={"pk": 99999})
        )
        self.assertEqual(response.status_code, 404)

    def test_dtfhuman_update_returns_404_for_invalid_pk(self):
        """Test that dtfhuman update returns 404 for non-existent character."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(
            reverse("characters:demon:update:dtfhuman_full", kwargs={"pk": 99999})
        )
        self.assertEqual(response.status_code, 404)
