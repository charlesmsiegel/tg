"""Tests for sorcerer views module."""

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from characters.models.core.archetype import Archetype
from characters.models.mage.fellowship import SorcererFellowship
from characters.models.mage.sorcerer import LinearMagicPath, Sorcerer
from game.models import Chronicle


class TestSorcererDetailView(TestCase):
    """Test SorcererDetailView permissions and functionality."""

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

        self.sorcerer = Sorcerer.objects.create(
            name="Test Sorcerer",
            owner=self.owner,
            chronicle=self.chronicle,
            status="App",
            sorcerer_type="hedge_mage",
        )

    def test_detail_view_accessible_to_owner(self):
        """Test that sorcerer detail view is accessible to the owner."""
        self.client.login(username="owner", password="password")
        response = self.client.get(self.sorcerer.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_detail_view_accessible_to_st(self):
        """Test that sorcerer detail view is accessible to storytellers."""
        self.client.login(username="st", password="password")
        response = self.client.get(self.sorcerer.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_detail_view_hidden_from_other_users(self):
        """Test that characters are hidden from other users (404)."""
        self.client.login(username="other", password="password")
        response = self.client.get(self.sorcerer.get_absolute_url())
        self.assertEqual(response.status_code, 404)

    def test_detail_view_returns_404_without_login(self):
        """Test that unauthenticated users get 404."""
        response = self.client.get(self.sorcerer.get_absolute_url())
        self.assertEqual(response.status_code, 404)

    def test_detail_view_template_used(self):
        """Test that correct template is used for sorcerer detail view."""
        self.client.login(username="owner", password="password")
        response = self.client.get(self.sorcerer.get_absolute_url())
        self.assertTemplateUsed(response, "characters/mage/sorcerer/detail.html")

    def test_detail_view_unapproved_hidden_from_others(self):
        """Test that unapproved characters are hidden from non-owners."""
        unapproved = Sorcerer.objects.create(
            name="Unapproved Sorcerer",
            owner=self.owner,
            chronicle=self.chronicle,
            status="Un",
            sorcerer_type="hedge_mage",
        )
        self.client.login(username="other", password="password")
        response = self.client.get(unapproved.get_absolute_url())
        # Should be 403 or 404 (denied/hidden from other users)
        self.assertIn(response.status_code, [403, 404])

    def test_detail_view_unapproved_visible_to_owner(self):
        """Test that unapproved characters are visible to owners."""
        unapproved = Sorcerer.objects.create(
            name="Unapproved Sorcerer",
            owner=self.owner,
            chronicle=self.chronicle,
            status="Un",
            sorcerer_type="hedge_mage",
        )
        self.client.login(username="owner", password="password")
        response = self.client.get(unapproved.get_absolute_url())
        self.assertEqual(response.status_code, 200)


class TestSorcererBasicsView(TestCase):
    """Test SorcererBasicsView for character creation."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="player", email="player@test.com", password="password"
        )
        self.nature = Archetype.objects.create(name="Survivor")
        self.demeanor = Archetype.objects.create(name="Caregiver")
        self.fellowship = SorcererFellowship.objects.create(name="Test Fellowship")

    def test_basics_view_accessible_when_logged_in(self):
        """Test that sorcerer basics view is accessible when logged in."""
        self.client.login(username="player", password="password")
        url = reverse("characters:mage:create:sorcerer")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_basics_view_uses_correct_template(self):
        """Test that correct template is used for sorcerer basics view."""
        self.client.login(username="player", password="password")
        url = reverse("characters:mage:create:sorcerer")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "characters/mage/sorcerer/basics.html")


class TestSorcererUpdateView(TestCase):
    """Test SorcererUpdateView permissions and functionality."""

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

        self.sorcerer = Sorcerer.objects.create(
            name="Test Sorcerer",
            owner=self.owner,
            chronicle=self.chronicle,
            status="App",
            sorcerer_type="hedge_mage",
        )

    def test_full_update_view_denied_to_owner(self):
        """Test that full update is denied to owners (ST-only)."""
        self.client.login(username="owner", password="password")
        url = reverse(
            "characters:mage:update:sorcerer_full", kwargs={"pk": self.sorcerer.pk}
        )
        response = self.client.get(url)
        # Owners don't have EDIT_FULL permission
        self.assertEqual(response.status_code, 403)

    def test_full_update_view_accessible_to_st(self):
        """Test that full sorcerer update view is accessible to storytellers."""
        self.client.login(username="st", password="password")
        url = reverse(
            "characters:mage:update:sorcerer_full", kwargs={"pk": self.sorcerer.pk}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_full_update_view_denied_to_other_users(self):
        """Test that full sorcerer update view is denied to other users."""
        self.client.login(username="other", password="password")
        url = reverse(
            "characters:mage:update:sorcerer_full", kwargs={"pk": self.sorcerer.pk}
        )
        response = self.client.get(url)
        # Should be forbidden
        self.assertIn(response.status_code, [403, 302])


class TestSorcererCharacterCreationView(TestCase):
    """Test SorcererCharacterCreationView workflow."""

    def setUp(self):
        self.client = Client()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="password"
        )
        self.other_user = User.objects.create_user(
            username="other", email="other@test.com", password="password"
        )
        self.sorcerer = Sorcerer.objects.create(
            name="Test Sorcerer",
            owner=self.owner,
            creation_status=1,  # At attribute step
            sorcerer_type="hedge_mage",
        )

    def test_creation_view_accessible_to_owner(self):
        """Test that creation view is accessible to owner."""
        self.client.login(username="owner", password="password")
        url = self.sorcerer.get_absolute_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_creation_view_denied_to_other_users(self):
        """Test that creation view is denied to non-owners."""
        self.client.login(username="other", password="password")
        url = self.sorcerer.get_absolute_url()
        response = self.client.get(url)
        self.assertIn(response.status_code, [403, 302])


class TestSorcererPathView(TestCase):
    """Test SorcererPathView for path selection."""

    def setUp(self):
        self.client = Client()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="password"
        )
        self.sorcerer = Sorcerer.objects.create(
            name="Test Sorcerer",
            owner=self.owner,
            creation_status=5,  # At path step
            sorcerer_type="hedge_mage",
            willpower=5,
        )
        self.path = LinearMagicPath.objects.create(
            name="Alchemy", numina_type="hedge_magic"
        )

    def test_path_view_accessible_to_owner(self):
        """Test that path view is accessible to owner."""
        self.client.login(username="owner", password="password")
        url = self.sorcerer.get_absolute_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestPsychicViews(TestCase):
    """Test views specific to psychic characters."""

    def setUp(self):
        self.client = Client()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="password"
        )
        self.psychic_path = LinearMagicPath.objects.create(
            name="Telepathy", numina_type="psychic"
        )
        self.psychic = Sorcerer.objects.create(
            name="Test Psychic",
            owner=self.owner,
            creation_status=4,  # At psychic step
            sorcerer_type="psychic",
            willpower=5,
        )

    def test_psychic_path_view_accessible_to_owner(self):
        """Test that psychic path view is accessible to owner."""
        self.client.login(username="owner", password="password")
        url = self.psychic.get_absolute_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
