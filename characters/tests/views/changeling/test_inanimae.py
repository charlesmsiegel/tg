"""Tests for Inanimae views."""

from characters.models.changeling.inanimae import Inanimae
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from game.models import Chronicle


class TestInanimaeDetailView(TestCase):
    """Test Inanimae detail view."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.inanimae = Inanimae.objects.create(
            name="Test Inanimae",
            owner=self.user,
            chronicle=self.chronicle,
            kingdom="kubera",
            inanimae_seeming="naturae",
            season="summer",
        )

    def test_detail_view_returns_200(self):
        """Test that detail view returns 200 for authenticated user."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(
            reverse("characters:changeling:inanimae", kwargs={"pk": self.inanimae.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_detail_view_uses_correct_template(self):
        """Test that detail view uses the correct template."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(
            reverse("characters:changeling:inanimae", kwargs={"pk": self.inanimae.pk})
        )
        self.assertTemplateUsed(response, "characters/changeling/inanimae/detail.html")


class TestInanimaeCreateView(TestCase):
    """Test Inanimae create view."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")

    def test_create_view_returns_200(self):
        """Test that create view returns 200 for authenticated user."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("characters:changeling:create:inanimae"))
        self.assertEqual(response.status_code, 200)

    def test_create_view_uses_correct_template(self):
        """Test that create view uses the correct template."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("characters:changeling:create:inanimae"))
        self.assertTemplateUsed(response, "characters/changeling/inanimae/form.html")

    def test_create_view_post_creates_object(self):
        """Test that posting to create view creates an Inanimae."""
        self.client.login(username="testuser", password="password")
        data = {
            "name": "New Inanimae",
            "kingdom": "ondine",
            "inanimae_seeming": "glimmer",
            "season": "spring",
            "npc": False,
        }
        response = self.client.post(
            reverse("characters:changeling:create:inanimae"), data=data
        )
        self.assertTrue(Inanimae.objects.filter(name="New Inanimae").exists())


class TestInanimaeUpdateView(TestCase):
    """Test Inanimae update view."""

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
        self.inanimae = Inanimae.objects.create(
            name="Test Inanimae",
            owner=self.user,
            chronicle=self.chronicle,
            kingdom="kubera",
            inanimae_seeming="naturae",
            season="summer",
        )

    def test_update_view_returns_200_for_admin(self):
        """Test that update view returns 200 for admin user."""
        self.client.login(username="adminuser", password="password")
        response = self.client.get(
            reverse(
                "characters:changeling:update:inanimae", kwargs={"pk": self.inanimae.pk}
            )
        )
        self.assertEqual(response.status_code, 200)

    def test_update_view_uses_correct_template(self):
        """Test that update view uses the correct template."""
        self.client.login(username="adminuser", password="password")
        response = self.client.get(
            reverse(
                "characters:changeling:update:inanimae", kwargs={"pk": self.inanimae.pk}
            )
        )
        self.assertTemplateUsed(response, "characters/changeling/inanimae/form.html")

    def test_update_view_denies_regular_user(self):
        """Test that update view denies access to regular users (requires EDIT_FULL)."""
        self.client.login(username="otheruser", password="password")
        response = self.client.get(
            reverse(
                "characters:changeling:update:inanimae", kwargs={"pk": self.inanimae.pk}
            )
        )
        self.assertEqual(response.status_code, 403)

    def test_update_view_denies_owner(self):
        """Test that update view denies access to owner (requires EDIT_FULL which owners don't have)."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(
            reverse(
                "characters:changeling:update:inanimae", kwargs={"pk": self.inanimae.pk}
            )
        )
        self.assertEqual(response.status_code, 403)


class TestInanimaeURLs(TestCase):
    """Test that Inanimae URLs resolve correctly."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.inanimae = Inanimae.objects.create(
            name="Test Inanimae",
            owner=self.user,
            chronicle=self.chronicle,
            kingdom="kubera",
            inanimae_seeming="naturae",
            season="summer",
        )

    def test_get_absolute_url(self):
        """Test that Inanimae.get_absolute_url() returns the correct URL."""
        expected_url = reverse(
            "characters:changeling:inanimae", kwargs={"pk": self.inanimae.pk}
        )
        self.assertEqual(self.inanimae.get_absolute_url(), expected_url)

    def test_get_update_url(self):
        """Test that Inanimae.get_update_url() returns the correct URL."""
        expected_url = reverse(
            "characters:changeling:update:inanimae", kwargs={"pk": self.inanimae.pk}
        )
        self.assertEqual(self.inanimae.get_update_url(), expected_url)

    def test_get_creation_url(self):
        """Test that Inanimae.get_creation_url() returns the correct URL."""
        expected_url = reverse("characters:changeling:create:inanimae")
        self.assertEqual(Inanimae.get_creation_url(), expected_url)
