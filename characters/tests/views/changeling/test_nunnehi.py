"""Tests for Nunnehi views."""

from characters.models.changeling.nunnehi import Nunnehi
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from game.models import Chronicle


class TestNunnehiDetailView(TestCase):
    """Test Nunnehi detail view."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.nunnehi = Nunnehi.objects.create(
            name="Test Nunnehi",
            owner=self.user,
            chronicle=self.chronicle,
            tribe="yunwi_tsundi",
            nunnehi_seeming="kohedan",
            path="warrior",
        )

    def test_detail_view_returns_200(self):
        """Test that detail view returns 200 for authenticated user."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(
            reverse("characters:changeling:nunnehi", kwargs={"pk": self.nunnehi.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_detail_view_uses_correct_template(self):
        """Test that detail view uses the correct template."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(
            reverse("characters:changeling:nunnehi", kwargs={"pk": self.nunnehi.pk})
        )
        self.assertTemplateUsed(response, "characters/changeling/nunnehi/detail.html")

    def test_detail_view_displays_tribe(self):
        """Test that detail view displays tribe correctly."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(
            reverse("characters:changeling:nunnehi", kwargs={"pk": self.nunnehi.pk})
        )
        self.assertContains(response, "Tribe")
        self.assertContains(response, "Yunwi Tsundi")

    def test_detail_view_displays_path(self):
        """Test that detail view displays path correctly."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(
            reverse("characters:changeling:nunnehi", kwargs={"pk": self.nunnehi.pk})
        )
        self.assertContains(response, "Path")
        self.assertContains(response, "Path of the Warrior")


class TestNunnehiCreateView(TestCase):
    """Test Nunnehi create view."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")

    def test_create_view_returns_200(self):
        """Test that create view returns 200 for authenticated user."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("characters:changeling:create:nunnehi"))
        self.assertEqual(response.status_code, 200)

    def test_create_view_uses_correct_template(self):
        """Test that create view uses the correct template."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("characters:changeling:create:nunnehi"))
        self.assertTemplateUsed(response, "characters/changeling/nunnehi/form.html")

    def test_create_view_has_tribe_field(self):
        """Test that create view has tribe field (not family)."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("characters:changeling:create:nunnehi"))
        self.assertContains(response, 'name="tribe"')

    def test_create_view_has_path_field(self):
        """Test that create view has path field (not camp)."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("characters:changeling:create:nunnehi"))
        self.assertContains(response, 'name="path"')

    def test_create_view_post_creates_object(self):
        """Test that posting to create view creates a Nunnehi."""
        self.client.login(username="testuser", password="password")
        data = {
            "name": "New Nunnehi",
            "tribe": "kachina",
            "nunnehi_seeming": "katchina",
            "path": "healer",
            "npc": False,
        }
        response = self.client.post(reverse("characters:changeling:create:nunnehi"), data=data)
        self.assertTrue(Nunnehi.objects.filter(name="New Nunnehi").exists())


class TestNunnehiUpdateView(TestCase):
    """Test Nunnehi update view."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.admin_user = User.objects.create_superuser(
            username="adminuser", email="admin@test.com", password="password"
        )
        self.other_user = User.objects.create_user(
            username="otheruser", email="other@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.nunnehi = Nunnehi.objects.create(
            name="Test Nunnehi",
            owner=self.user,
            chronicle=self.chronicle,
            tribe="yunwi_tsundi",
            nunnehi_seeming="kohedan",
            path="warrior",
        )

    def test_update_view_returns_200_for_admin(self):
        """Test that update view returns 200 for admin user."""
        self.client.login(username="adminuser", password="password")
        response = self.client.get(
            reverse("characters:changeling:update:nunnehi", kwargs={"pk": self.nunnehi.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_update_view_uses_correct_template(self):
        """Test that update view uses the correct template."""
        self.client.login(username="adminuser", password="password")
        response = self.client.get(
            reverse("characters:changeling:update:nunnehi", kwargs={"pk": self.nunnehi.pk})
        )
        self.assertTemplateUsed(response, "characters/changeling/nunnehi/form.html")

    def test_update_view_denies_regular_user(self):
        """Test that update view denies access to regular users (requires EDIT_FULL)."""
        self.client.login(username="otheruser", password="password")
        response = self.client.get(
            reverse("characters:changeling:update:nunnehi", kwargs={"pk": self.nunnehi.pk})
        )
        self.assertEqual(response.status_code, 403)

    def test_update_view_has_spirit_guide_field(self):
        """Test that update view has spirit_guide field."""
        self.client.login(username="adminuser", password="password")
        response = self.client.get(
            reverse("characters:changeling:update:nunnehi", kwargs={"pk": self.nunnehi.pk})
        )
        self.assertContains(response, 'name="spirit_guide"')


class TestNunnehiURLs(TestCase):
    """Test that Nunnehi URLs resolve correctly."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.nunnehi = Nunnehi.objects.create(
            name="Test Nunnehi",
            owner=self.user,
            chronicle=self.chronicle,
            tribe="yunwi_tsundi",
            nunnehi_seeming="kohedan",
            path="warrior",
        )

    def test_get_absolute_url(self):
        """Test that Nunnehi.get_absolute_url() returns the correct URL."""
        expected_url = reverse("characters:changeling:nunnehi", kwargs={"pk": self.nunnehi.pk})
        self.assertEqual(self.nunnehi.get_absolute_url(), expected_url)

    def test_get_update_url(self):
        """Test that Nunnehi.get_update_url() returns the correct URL."""
        expected_url = reverse(
            "characters:changeling:update:nunnehi", kwargs={"pk": self.nunnehi.pk}
        )
        self.assertEqual(self.nunnehi.get_update_url(), expected_url)

    def test_get_creation_url(self):
        """Test that Nunnehi.get_creation_url() returns the correct URL."""
        expected_url = reverse("characters:changeling:create:nunnehi")
        self.assertEqual(Nunnehi.get_creation_url(), expected_url)
