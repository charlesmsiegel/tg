"""Tests for wtohuman views module."""

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from characters.models.core.archetype import Archetype
from characters.models.wraith.wtohuman import WtOHuman
from game.models import Chronicle


class TestWtOHumanBasicsView(TestCase):
    """Test WtOHumanBasicsView for character creation."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="player", email="player@test.com", password="password"
        )
        self.nature = Archetype.objects.create(name="Survivor")
        self.demeanor = Archetype.objects.create(name="Caregiver")

    def test_basics_view_requires_login(self):
        """Test that basics view requires login."""
        url = reverse("characters:wraith:create:wto_human")
        response = self.client.get(url)
        # App returns 401 for unauthenticated users instead of redirect
        self.assertEqual(response.status_code, 401)

    def test_basics_view_accessible_when_logged_in(self):
        """Test that WtOHuman basics view is accessible when logged in."""
        self.client.login(username="player", password="password")
        url = reverse("characters:wraith:create:wto_human")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_basics_view_uses_correct_template(self):
        """Test that correct template is used for WtOHuman basics view."""
        self.client.login(username="player", password="password")
        url = reverse("characters:wraith:create:wto_human")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "characters/wraith/wtohuman/basics.html")

    def test_basics_view_has_storyteller_context(self):
        """Test that storyteller context is passed to template."""
        self.client.login(username="player", password="password")
        url = reverse("characters:wraith:create:wto_human")
        response = self.client.get(url)
        self.assertIn("storyteller", response.context)

    def test_basics_view_storyteller_context_for_st(self):
        """Test that storyteller context is True for STs."""
        st = User.objects.create_user(username="st", email="st@test.com", password="password")
        chronicle = Chronicle.objects.create(name="Test Chronicle")
        chronicle.storytellers.add(st)

        self.client.login(username="st", password="password")
        url = reverse("characters:wraith:create:wto_human")
        response = self.client.get(url)
        self.assertTrue(response.context["storyteller"])


class TestWtOHumanTemplateSelectView(TestCase):
    """Test WtOHumanTemplateSelectView for template selection."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="player", email="player@test.com", password="password"
        )
        self.wtohuman = WtOHuman.objects.create(
            name="Test WtOHuman",
            owner=self.user,
            creation_status=0,
        )

    def test_template_select_view_requires_login(self):
        """Test that template select view requires login."""
        url = reverse("characters:wraith:wtohuman_template", kwargs={"pk": self.wtohuman.pk})
        response = self.client.get(url)
        # AuthErrorHandlerMiddleware converts login redirects to 401
        self.assertEqual(response.status_code, 401)

    def test_template_select_view_accessible_to_owner(self):
        """Test that template select view is accessible to owner."""
        self.client.login(username="player", password="password")
        url = reverse("characters:wraith:wtohuman_template", kwargs={"pk": self.wtohuman.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_template_select_redirects_if_creation_started(self):
        """Test that template select redirects if character creation has started."""
        self.wtohuman.creation_status = 1
        self.wtohuman.save()

        self.client.login(username="player", password="password")
        url = reverse("characters:wraith:wtohuman_template", kwargs={"pk": self.wtohuman.pk})
        response = self.client.get(url)
        # Should redirect to creation view
        self.assertEqual(response.status_code, 302)

    def test_template_select_view_returns_404_for_other_user(self):
        """Test that template select returns 404 for non-owners."""
        other_user = User.objects.create_user(
            username="other", email="other@test.com", password="password"
        )
        self.client.login(username="other", password="password")
        url = reverse("characters:wraith:wtohuman_template", kwargs={"pk": self.wtohuman.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class TestWtOHumanCharacterCreationView(TestCase):
    """Test WtOHumanCharacterCreationView workflow."""

    def setUp(self):
        self.client = Client()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="password"
        )
        self.other_user = User.objects.create_user(
            username="other", email="other@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")

        self.wtohuman = WtOHuman.objects.create(
            name="Test WtOHuman",
            owner=self.owner,
            chronicle=self.chronicle,
            creation_status=1,  # At attribute step
        )

    def test_creation_view_accessible_to_owner(self):
        """Test that character creation view is accessible to owner."""
        self.client.login(username="owner", password="password")
        url = reverse("characters:wraith:wtohuman_creation", kwargs={"pk": self.wtohuman.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_creation_view_denied_to_other_users(self):
        """Test that character creation view is denied to non-owners."""
        self.client.login(username="other", password="password")
        url = reverse("characters:wraith:wtohuman_creation", kwargs={"pk": self.wtohuman.pk})
        response = self.client.get(url)
        self.assertIn(response.status_code, [403, 302, 404])


class TestWtOHumanAbilityView(TestCase):
    """Test WtOHumanAbilityView for ability allocation."""

    def setUp(self):
        self.client = Client()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="password"
        )
        self.wtohuman = WtOHuman.objects.create(
            name="Test WtOHuman",
            owner=self.owner,
            creation_status=2,  # At ability step
        )

    def test_ability_view_accessible_to_owner(self):
        """Test that ability view is accessible to owner."""
        self.client.login(username="owner", password="password")
        url = reverse("characters:wraith:wtohuman_creation", kwargs={"pk": self.wtohuman.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestWtOHumanBackgroundsView(TestCase):
    """Test WtOHumanBackgroundsView for background allocation."""

    def setUp(self):
        self.client = Client()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="password"
        )
        self.wtohuman = WtOHuman.objects.create(
            name="Test WtOHuman",
            owner=self.owner,
            creation_status=3,  # At backgrounds step
        )

    def test_backgrounds_view_accessible_to_owner(self):
        """Test that backgrounds view is accessible to owner."""
        self.client.login(username="owner", password="password")
        url = reverse("characters:wraith:wtohuman_creation", kwargs={"pk": self.wtohuman.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestWtOHumanExtrasView(TestCase):
    """Test WtOHumanExtrasView for description and history."""

    def setUp(self):
        self.client = Client()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="password"
        )
        self.wtohuman = WtOHuman.objects.create(
            name="Test WtOHuman",
            owner=self.owner,
            creation_status=4,  # At extras step
        )

    def test_extras_view_accessible_to_owner(self):
        """Test that extras view is accessible to owner."""
        self.client.login(username="owner", password="password")
        url = reverse("characters:wraith:wtohuman_creation", kwargs={"pk": self.wtohuman.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestWtOHumanFreebiesView(TestCase):
    """Test WtOHumanFreebiesView for freebie point allocation."""

    def setUp(self):
        self.client = Client()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="password"
        )
        self.wtohuman = WtOHuman.objects.create(
            name="Test WtOHuman",
            owner=self.owner,
            creation_status=5,  # At freebies step
            freebies=15,
        )

    def test_freebies_view_accessible_to_owner(self):
        """Test that freebies view is accessible to owner."""
        self.client.login(username="owner", password="password")
        url = reverse("characters:wraith:wtohuman_creation", kwargs={"pk": self.wtohuman.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestWtOHumanUpdateView(TestCase):
    """Test WtOHumanUpdateView permissions and functionality."""

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

        self.wtohuman = WtOHuman.objects.create(
            name="Test WtOHuman",
            owner=self.owner,
            chronicle=self.chronicle,
            status="App",
        )

    def test_update_view_accessible_to_st(self):
        """Test that WtOHuman update view is accessible to storytellers."""
        self.client.login(username="st", password="password")
        url = reverse("characters:wraith:update:wto_human_full", kwargs={"pk": self.wtohuman.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_denied_to_other_users(self):
        """Test that WtOHuman update view is denied to other users."""
        self.client.login(username="other", password="password")
        url = reverse("characters:wraith:update:wto_human_full", kwargs={"pk": self.wtohuman.pk})
        response = self.client.get(url)
        self.assertIn(response.status_code, [403, 302])


class TestWtOHumanView404Handling(TestCase):
    """Test 404 error handling for WtOHuman views with invalid IDs."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.chronicle.storytellers.add(self.user)

    def test_template_select_returns_404_for_invalid_pk(self):
        """Test that template select returns 404 for non-existent character."""
        self.client.login(username="testuser", password="password")
        url = reverse("characters:wraith:wtohuman_template", kwargs={"pk": 99999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_creation_view_returns_404_for_invalid_pk(self):
        """Test that creation view returns 404 for non-existent character."""
        self.client.login(username="testuser", password="password")
        url = reverse("characters:wraith:wtohuman_creation", kwargs={"pk": 99999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
