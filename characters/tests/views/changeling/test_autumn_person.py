"""Tests for AutumnPerson views."""

from characters.models.changeling.autumn_person import AutumnPerson
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from game.models import Chronicle


class TestAutumnPersonDetailView(TestCase):
    """Test AutumnPerson detail view."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.autumn_person = AutumnPerson.objects.create(
            name="Test Autumn Person",
            owner=self.user,
            chronicle=self.chronicle,
            archetype="bureaucrat",
            awareness="unaware",
            banality_rating=8,
        )

    def test_detail_view_returns_200(self):
        """Test that detail view returns 200 for authenticated user."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(
            reverse(
                "characters:changeling:autumn_person",
                kwargs={"pk": self.autumn_person.pk},
            )
        )
        self.assertEqual(response.status_code, 200)

    def test_detail_view_uses_correct_template(self):
        """Test that detail view uses the correct template."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(
            reverse(
                "characters:changeling:autumn_person",
                kwargs={"pk": self.autumn_person.pk},
            )
        )
        self.assertTemplateUsed(
            response, "characters/changeling/autumn_person/detail.html"
        )


class TestAutumnPersonCreateView(TestCase):
    """Test AutumnPerson create view."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")

    def test_create_view_returns_200(self):
        """Test that create view returns 200 for authenticated user."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("characters:changeling:create:autumn_person"))
        self.assertEqual(response.status_code, 200)

    def test_create_view_uses_correct_template(self):
        """Test that create view uses the correct template."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("characters:changeling:create:autumn_person"))
        self.assertTemplateUsed(
            response, "characters/changeling/autumn_person/form.html"
        )

    def test_create_view_post_creates_object(self):
        """Test that posting to create view creates an AutumnPerson."""
        self.client.login(username="testuser", password="password")
        data = {
            "name": "New Autumn Person",
            "archetype": "cynic",
            "awareness": "suspicious",
            "banality_rating": 9,
            "npc": True,
        }
        response = self.client.post(
            reverse("characters:changeling:create:autumn_person"), data=data
        )
        self.assertTrue(AutumnPerson.objects.filter(name="New Autumn Person").exists())


class TestAutumnPersonUpdateView(TestCase):
    """Test AutumnPerson update view."""

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
        self.autumn_person = AutumnPerson.objects.create(
            name="Test Autumn Person",
            owner=self.user,
            chronicle=self.chronicle,
            archetype="bureaucrat",
            awareness="unaware",
            banality_rating=8,
        )

    def test_update_view_returns_200_for_admin(self):
        """Test that update view returns 200 for admin user."""
        self.client.login(username="adminuser", password="password")
        response = self.client.get(
            reverse(
                "characters:changeling:update:autumn_person",
                kwargs={"pk": self.autumn_person.pk},
            )
        )
        self.assertEqual(response.status_code, 200)

    def test_update_view_uses_correct_template(self):
        """Test that update view uses the correct template."""
        self.client.login(username="adminuser", password="password")
        response = self.client.get(
            reverse(
                "characters:changeling:update:autumn_person",
                kwargs={"pk": self.autumn_person.pk},
            )
        )
        self.assertTemplateUsed(
            response, "characters/changeling/autumn_person/form.html"
        )

    def test_update_view_denies_regular_user(self):
        """Test that update view denies access to regular users (requires EDIT_FULL)."""
        self.client.login(username="otheruser", password="password")
        response = self.client.get(
            reverse(
                "characters:changeling:update:autumn_person",
                kwargs={"pk": self.autumn_person.pk},
            )
        )
        self.assertEqual(response.status_code, 403)


class TestAutumnPersonURLs(TestCase):
    """Test that AutumnPerson URLs resolve correctly."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.autumn_person = AutumnPerson.objects.create(
            name="Test Autumn Person",
            owner=self.user,
            chronicle=self.chronicle,
            archetype="bureaucrat",
        )

    def test_get_absolute_url(self):
        """Test that AutumnPerson.get_absolute_url() returns the correct URL."""
        expected_url = reverse(
            "characters:changeling:autumn_person", kwargs={"pk": self.autumn_person.pk}
        )
        self.assertEqual(self.autumn_person.get_absolute_url(), expected_url)

    def test_get_update_url(self):
        """Test that AutumnPerson.get_update_url() returns the correct URL."""
        expected_url = reverse(
            "characters:changeling:update:autumn_person",
            kwargs={"pk": self.autumn_person.pk},
        )
        self.assertEqual(self.autumn_person.get_update_url(), expected_url)

    def test_get_creation_url(self):
        """Test that AutumnPerson.get_creation_url() returns the correct URL."""
        expected_url = reverse("characters:changeling:create:autumn_person")
        self.assertEqual(AutumnPerson.get_creation_url(), expected_url)
