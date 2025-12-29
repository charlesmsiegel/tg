"""Tests for wraith views module."""

from characters.models.wraith.guild import Guild
from characters.models.wraith.wraith import Wraith
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from game.models import Chronicle


class TestWraithDetailView(TestCase):
    """Test WraithDetailView permissions and functionality."""

    def setUp(self):
        self.client = Client()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="password"
        )
        self.other_user = User.objects.create_user(
            username="other", email="other@test.com", password="password"
        )
        self.st = User.objects.create_user(username="st", email="st@test.com", password="password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.chronicle.storytellers.add(self.st)

        self.wraith = Wraith.objects.create(
            name="Test Wraith",
            owner=self.owner,
            chronicle=self.chronicle,
            status="App",
        )

    def test_detail_view_accessible_to_owner(self):
        """Test that wraith detail view is accessible to the owner."""
        self.client.login(username="owner", password="password")
        response = self.client.get(self.wraith.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_detail_view_accessible_to_st(self):
        """Test that wraith detail view is accessible to storytellers."""
        self.client.login(username="st", password="password")
        response = self.client.get(self.wraith.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_detail_view_hidden_from_other_users(self):
        """Test that characters are hidden from other users (404)."""
        self.client.login(username="other", password="password")
        response = self.client.get(self.wraith.get_absolute_url())
        self.assertEqual(response.status_code, 404)

    def test_detail_view_returns_404_without_login(self):
        """Test that unauthenticated users get 404 (not login redirect)."""
        response = self.client.get(self.wraith.get_absolute_url())
        self.assertEqual(response.status_code, 404)

    def test_detail_view_template_used(self):
        """Test that correct template is used for wraith detail view."""
        self.client.login(username="owner", password="password")
        response = self.client.get(self.wraith.get_absolute_url())
        self.assertTemplateUsed(response, "characters/wraith/wraith/detail.html")

    def test_detail_view_has_arcanoi_in_context(self):
        """Test that arcanoi are in the context."""
        self.client.login(username="owner", password="password")
        response = self.client.get(self.wraith.get_absolute_url())
        self.assertIn("arcanoi", response.context)

    def test_detail_view_has_dark_arcanoi_in_context(self):
        """Test that dark arcanoi are in the context."""
        self.client.login(username="owner", password="password")
        response = self.client.get(self.wraith.get_absolute_url())
        self.assertIn("dark_arcanoi", response.context)

    def test_detail_view_unapproved_hidden_from_others(self):
        """Test that unapproved characters are hidden from non-owners."""
        unapproved = Wraith.objects.create(
            name="Unapproved Wraith",
            owner=self.owner,
            chronicle=self.chronicle,
            status="Un",
        )
        self.client.login(username="other", password="password")
        response = self.client.get(unapproved.get_absolute_url())
        # Should be 403 or 404 (denied/hidden from other users)
        self.assertIn(response.status_code, [403, 404])

    def test_detail_view_unapproved_visible_to_owner(self):
        """Test that unapproved characters are visible to owners."""
        unapproved = Wraith.objects.create(
            name="Unapproved Wraith",
            owner=self.owner,
            chronicle=self.chronicle,
            status="Un",
        )
        self.client.login(username="owner", password="password")
        response = self.client.get(unapproved.get_absolute_url())
        self.assertEqual(response.status_code, 200)


class TestWraithCreateView(TestCase):
    """Test WraithCreateView functionality."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.guild = Guild.objects.create(name="Usurers", willpower=5)

    def test_create_view_accessible_when_logged_in(self):
        """Test that wraith create view is accessible when logged in."""
        self.client.login(username="testuser", password="password")
        url = reverse("characters:wraith:create:wraith")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_requires_login(self):
        """Test that wraith create view requires login."""
        url = reverse("characters:wraith:create:wraith")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)


class TestWraithUpdateView(TestCase):
    """Test WraithUpdateView permissions and functionality."""

    def setUp(self):
        self.client = Client()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="password"
        )
        self.other_user = User.objects.create_user(
            username="other", email="other@test.com", password="password"
        )
        self.st = User.objects.create_user(username="st", email="st@test.com", password="password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.chronicle.storytellers.add(self.st)

        self.wraith = Wraith.objects.create(
            name="Test Wraith",
            owner=self.owner,
            chronicle=self.chronicle,
            status="App",
        )

    def test_update_view_denied_to_other_users(self):
        """Test that update view is denied to other users."""
        self.client.login(username="other", password="password")
        url = reverse("characters:wraith:update:wraith", kwargs={"pk": self.wraith.pk})
        response = self.client.get(url)
        self.assertIn(response.status_code, [403, 302, 404])


class TestWraithView404Handling(TestCase):
    """Test 404 error handling for wraith views with invalid IDs."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.chronicle.storytellers.add(self.user)

    def test_wraith_detail_returns_404_for_invalid_pk(self):
        """Test that wraith detail returns 404 for non-existent character."""
        self.client.login(username="testuser", password="password")
        url = reverse("characters:wraith:wraith", kwargs={"pk": 99999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_wraith_chargen_returns_404_for_invalid_pk(self):
        """Test that wraith chargen returns 404 for non-existent character."""
        self.client.login(username="testuser", password="password")
        url = reverse("characters:wraith:wraith_chargen", kwargs={"pk": 99999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class TestWraithGetAbsoluteUrl(TestCase):
    """Test get_absolute_url method for Wraith."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.wraith = Wraith.objects.create(
            name="Test Wraith",
            owner=self.user,
        )

    def test_get_absolute_url_returns_correct_url(self):
        """Test that get_absolute_url returns the correct URL."""
        expected_url = reverse("characters:wraith:wraith", kwargs={"pk": self.wraith.pk})
        self.assertEqual(self.wraith.get_absolute_url(), expected_url)


class TestWraithGetUpdateUrl(TestCase):
    """Test get_update_url method for Wraith."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.wraith = Wraith.objects.create(
            name="Test Wraith",
            owner=self.user,
        )

    def test_get_update_url_returns_correct_url(self):
        """Test that get_update_url returns the correct URL."""
        expected_url = reverse("characters:wraith:update:wraith", kwargs={"pk": self.wraith.pk})
        self.assertEqual(self.wraith.get_update_url(), expected_url)


class TestWraithGetCreationUrl(TestCase):
    """Test get_creation_url classmethod for Wraith."""

    def test_get_creation_url_returns_correct_url(self):
        """Test that get_creation_url returns the correct URL."""
        expected_url = reverse("characters:wraith:create:wraith")
        self.assertEqual(Wraith.get_creation_url(), expected_url)
