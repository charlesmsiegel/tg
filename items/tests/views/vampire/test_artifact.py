"""Tests for vampire artifact views."""

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from items.models.vampire import VampireArtifact


class VampireArtifactCreateViewTest(TestCase):
    """Test the VampireArtifact create view."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.create_url = reverse("items:vampire:create:artifact")

    def test_create_view_requires_login(self):
        """Unauthenticated users are denied or redirected."""
        response = self.client.get(self.create_url)
        # Either redirect (302) or unauthorized (401) is acceptable
        self.assertIn(response.status_code, [302, 401])

    def test_create_view_authenticated(self):
        """Authenticated users can access the create view."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "items/vampire/artifact/form.html")

    def test_create_valid_artifact(self):
        """Valid form data creates an artifact."""
        self.client.login(username="testuser", password="password")
        response = self.client.post(
            self.create_url,
            {
                "name": "Test Artifact",
                "description": "A test artifact",
                "power_level": 3,
                "background_cost": 2,
                "is_cursed": False,
                "is_unique": True,
                "requires_blood": False,
                "powers": "Test powers",
                "history": "Test history",
            },
        )
        self.assertEqual(VampireArtifact.objects.count(), 1)
        artifact = VampireArtifact.objects.first()
        self.assertEqual(artifact.name, "Test Artifact")
        self.assertEqual(artifact.owner, self.user)

    def test_create_empty_name_shows_error(self):
        """Submitting empty name shows field error in template."""
        self.client.login(username="testuser", password="password")
        response = self.client.post(
            self.create_url,
            {
                "name": "",  # Empty name should trigger error
                "description": "A test artifact",
                "power_level": 3,
                "background_cost": 2,
            },
        )
        # Form should not be valid
        self.assertEqual(response.status_code, 200)
        self.assertEqual(VampireArtifact.objects.count(), 0)

        # Check the form has errors
        form = response.context["form"]
        self.assertTrue(form.errors)
        self.assertIn("name", form.errors)

        # Verify the error is rendered in the template
        self.assertContains(response, "text-danger")
        self.assertContains(response, "This field is required")


class VampireArtifactUpdateViewTest(TestCase):
    """Test the VampireArtifact update view."""

    def setUp(self):
        self.client = Client()
        # Create a superuser to have full edit permissions
        self.user = User.objects.create_superuser(
            username="adminuser", email="admin@test.com", password="password"
        )
        self.artifact = VampireArtifact.objects.create(
            name="Test Artifact",
            owner=self.user,
            power_level=3,
            background_cost=2,
        )
        self.update_url = reverse("items:vampire:update:artifact", kwargs={"pk": self.artifact.pk})

    def test_update_empty_name_shows_error(self):
        """Submitting empty name on update shows field error in template."""
        self.client.login(username="adminuser", password="password")
        response = self.client.post(
            self.update_url,
            {
                "name": "",  # Empty name should trigger error
                "description": "Updated description",
                "power_level": 3,
                "background_cost": 2,
            },
        )
        # Form should not be valid
        self.assertEqual(response.status_code, 200)

        # Check the form has errors
        form = response.context["form"]
        self.assertTrue(form.errors)
        self.assertIn("name", form.errors)

        # Verify the error is rendered in the template
        self.assertContains(response, "text-danger")
        self.assertContains(response, "This field is required")
