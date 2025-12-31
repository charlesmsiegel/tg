"""Tests for mage views module."""

from characters.models.core.archetype import Archetype
from characters.models.mage.faction import MageFaction
from characters.models.mage.focus import Tenet
from characters.models.mage.mage import Mage
from characters.models.mage.resonance import Resonance
from characters.models.mage.sphere import Sphere
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from game.models import Chronicle


class TestMageDetailView(TestCase):
    """Test MageDetailView permissions and functionality."""

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

        self.mage = Mage.objects.create(
            name="Test Mage",
            owner=self.owner,
            chronicle=self.chronicle,
            status="App",
            arete=1,
        )

    def test_detail_view_accessible_to_owner(self):
        """Test that mage detail view is accessible to the owner."""
        self.client.login(username="owner", password="password")
        response = self.client.get(self.mage.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_detail_view_accessible_to_st(self):
        """Test that mage detail view is accessible to storytellers."""
        self.client.login(username="st", password="password")
        response = self.client.get(self.mage.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_detail_view_hidden_from_other_users(self):
        """Test that characters are hidden from other users (404)."""
        self.client.login(username="other", password="password")
        response = self.client.get(self.mage.get_absolute_url())
        self.assertEqual(response.status_code, 404)

    def test_detail_view_returns_404_without_login(self):
        """Test that unauthenticated users get 404 (not login redirect)."""
        response = self.client.get(self.mage.get_absolute_url())
        self.assertEqual(response.status_code, 404)

    def test_detail_view_template_used(self):
        """Test that correct template is used for mage detail view."""
        self.client.login(username="owner", password="password")
        response = self.client.get(self.mage.get_absolute_url())
        self.assertTemplateUsed(response, "characters/mage/mage/detail.html")

    def test_detail_view_unapproved_hidden_from_others(self):
        """Test that unapproved characters are hidden from non-owners."""
        unapproved = Mage.objects.create(
            name="Unapproved Mage",
            owner=self.owner,
            chronicle=self.chronicle,
            status="Un",
            arete=1,
        )
        self.client.login(username="other", password="password")
        response = self.client.get(unapproved.get_absolute_url())
        # Should be 403 or 404 (denied/hidden from other users)
        self.assertIn(response.status_code, [403, 404])

    def test_detail_view_unapproved_visible_to_owner(self):
        """Test that unapproved characters are visible to owners."""
        unapproved = Mage.objects.create(
            name="Unapproved Mage",
            owner=self.owner,
            chronicle=self.chronicle,
            status="Un",
            arete=1,
        )
        self.client.login(username="owner", password="password")
        response = self.client.get(unapproved.get_absolute_url())
        self.assertEqual(response.status_code, 200)


class TestMageCreateView(TestCase):
    """Test MageCreateView functionality."""

    def setUp(self):
        self.client = Client()
        self.st = User.objects.create_user(username="st", email="st@test.com", password="password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.chronicle.storytellers.add(self.st)

        # Create required objects
        self.nature = Archetype.objects.create(name="Survivor")
        self.demeanor = Archetype.objects.create(name="Caregiver")
        self.affiliation = MageFaction.objects.create(name="Traditions")

    def test_full_create_view_accessible_when_logged_in(self):
        """Test that mage full create view is accessible when logged in."""
        self.client.login(username="st", password="password")
        url = reverse("characters:mage:create:mage_full")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_full_create_view_uses_correct_template(self):
        """Test that correct template is used for mage create view."""
        self.client.login(username="st", password="password")
        url = reverse("characters:mage:create:mage_full")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "characters/mage/mage/form.html")


class TestMageBasicsView(TestCase):
    """Test MageBasicsView for character creation."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="player", email="player@test.com", password="password"
        )
        self.nature = Archetype.objects.create(name="Survivor")
        self.demeanor = Archetype.objects.create(name="Caregiver")
        self.affiliation = MageFaction.objects.create(name="Traditions")
        self.faction = MageFaction.objects.create(name="Order of Hermes", parent=self.affiliation)

    def test_basics_view_accessible_when_logged_in(self):
        """Test that mage basics view is accessible when logged in."""
        self.client.login(username="player", password="password")
        url = reverse("characters:mage:create:mage")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_basics_view_uses_correct_template(self):
        """Test that correct template is used for mage basics view."""
        self.client.login(username="player", password="password")
        url = reverse("characters:mage:create:mage")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "characters/mage/mage/magebasics.html")


class TestMageUpdateView(TestCase):
    """Test MageUpdateView permissions and functionality."""

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

        self.mage = Mage.objects.create(
            name="Test Mage",
            owner=self.owner,
            chronicle=self.chronicle,
            status="App",
            arete=1,
        )

    def test_full_update_view_denied_to_owner(self):
        """Test that full update is denied to owners (ST-only)."""
        self.client.login(username="owner", password="password")
        url = reverse("characters:mage:update:mage_full", kwargs={"pk": self.mage.pk})
        response = self.client.get(url)
        # Owners don't have EDIT_FULL permission
        self.assertEqual(response.status_code, 403)

    def test_full_update_view_accessible_to_st(self):
        """Test that full mage update view is accessible to storytellers."""
        self.client.login(username="st", password="password")
        url = reverse("characters:mage:update:mage_full", kwargs={"pk": self.mage.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_full_update_view_denied_to_other_users(self):
        """Test that full mage update view is denied to other users."""
        self.client.login(username="other", password="password")
        url = reverse("characters:mage:update:mage_full", kwargs={"pk": self.mage.pk})
        response = self.client.get(url)
        # Should be forbidden
        self.assertIn(response.status_code, [403, 302])


class TestMageCharacterCreationView(TestCase):
    """Test MageCharacterCreationView workflow."""

    def setUp(self):
        self.client = Client()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="password"
        )
        self.other_user = User.objects.create_user(
            username="other", email="other@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")

        self.mage = Mage.objects.create(
            name="Test Mage",
            owner=self.owner,
            chronicle=self.chronicle,
            creation_status=1,  # At attribute step
            arete=1,
        )

    def test_creation_view_accessible_to_owner(self):
        """Test that character creation view is accessible to owner."""
        self.client.login(username="owner", password="password")
        url = reverse("characters:mage:update:mage", kwargs={"pk": self.mage.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_creation_view_denied_to_other_users(self):
        """Test that character creation view is denied to non-owners."""
        self.client.login(username="other", password="password")
        url = reverse("characters:mage:update:mage", kwargs={"pk": self.mage.pk})
        response = self.client.get(url)
        self.assertIn(response.status_code, [403, 302])


class TestMageSpheresView(TestCase):
    """Test MageSpheresView for sphere allocation."""

    def setUp(self):
        self.client = Client()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="password"
        )
        self.affiliation = MageFaction.objects.create(name="Traditions")
        self.faction = MageFaction.objects.create(
            name="Order of Hermes",
            parent=self.affiliation,
        )
        self.mage = Mage.objects.create(
            name="Test Mage",
            owner=self.owner,
            creation_status=4,  # At spheres step
            arete=1,
            affiliation=self.affiliation,
            faction=self.faction,
        )

        # Create spheres
        self.forces = Sphere.objects.create(name="Forces", property_name="forces")
        self.prime = Sphere.objects.create(name="Prime", property_name="prime")

    def test_spheres_view_accessible_to_owner(self):
        """Test that spheres view is accessible to owner."""
        self.client.login(username="owner", password="password")
        url = reverse("characters:mage:update:mage", kwargs={"pk": self.mage.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestMageAjaxViews(TestCase):
    """Test Mage AJAX views."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.affiliation = MageFaction.objects.create(name="Traditions")
        self.faction = MageFaction.objects.create(
            name="Order of Hermes",
            parent=self.affiliation,
        )

    def test_load_factions_returns_data_when_authenticated(self):
        """Test that load_factions returns data when authenticated."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(
            reverse("characters:mage:ajax:load_factions"),
            {"affiliation": self.affiliation.id},
        )
        self.assertEqual(response.status_code, 200)

    def test_load_subfactions_returns_data_when_authenticated(self):
        """Test that load_subfactions returns data when authenticated."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(
            reverse("characters:mage:ajax:load_subfactions"),
            {"faction": self.faction.id},
        )
        self.assertEqual(response.status_code, 200)


class TestMageFocusView(TestCase):
    """Test MageFocusView for focus selection."""

    def setUp(self):
        self.client = Client()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="password"
        )
        self.mage = Mage.objects.create(
            name="Test Mage",
            owner=self.owner,
            creation_status=5,  # At focus step
            arete=1,
        )

    def test_focus_view_accessible_to_owner(self):
        """Test that focus view is accessible to owner."""
        self.client.login(username="owner", password="password")
        url = reverse("characters:mage:update:mage", kwargs={"pk": self.mage.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestMageFreebiesView(TestCase):
    """Test MageFreebiesView for freebie point allocation."""

    def setUp(self):
        self.client = Client()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="password"
        )
        self.met_tenet = Tenet.objects.create(name="Everything is Data", tenet_type="met")
        self.per_tenet = Tenet.objects.create(name="Self-Empowerment", tenet_type="per")
        self.asc_tenet = Tenet.objects.create(
            name="Enlightenment Through Technology", tenet_type="asc"
        )
        self.mage = Mage.objects.create(
            name="Test Mage",
            owner=self.owner,
            creation_status=7,  # At freebies step
            freebies=15,
            arete=1,
            metaphysical_tenet=self.met_tenet,
            personal_tenet=self.per_tenet,
            ascension_tenet=self.asc_tenet,
        )

    def test_freebies_view_accessible_to_owner(self):
        """Test that freebies view is accessible to owner."""
        self.client.login(username="owner", password="password")
        url = reverse("characters:mage:update:mage", kwargs={"pk": self.mage.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestMageExtrasView(TestCase):
    """Test MageExtrasView for description and history."""

    def setUp(self):
        self.client = Client()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="password"
        )
        self.mage = Mage.objects.create(
            name="Test Mage",
            owner=self.owner,
            creation_status=6,  # At extras step
            arete=1,
        )

    def test_extras_view_accessible_to_owner(self):
        """Test that extras view is accessible to owner."""
        self.client.login(username="owner", password="password")
        url = reverse("characters:mage:update:mage", kwargs={"pk": self.mage.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestMageRoteView(TestCase):
    """Test MageRoteView for rote creation."""

    def setUp(self):
        self.client = Client()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="password"
        )
        self.mage = Mage.objects.create(
            name="Test Mage",
            owner=self.owner,
            creation_status=9,  # At rote step
            arete=1,
            rote_points=5,
        )

    def test_rote_view_accessible_to_owner(self):
        """Test that rote view is accessible to owner."""
        self.client.login(username="owner", password="password")
        url = reverse("characters:mage:update:mage", kwargs={"pk": self.mage.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestMageView404Handling(TestCase):
    """Test 404 error handling for mage views with invalid IDs."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.chronicle.storytellers.add(self.user)

    def test_mage_detail_returns_404_for_invalid_pk(self):
        """Test that mage detail returns 404 for non-existent character."""
        self.client.login(username="testuser", password="password")
        # Uses the generic character detail view which maps to specific views
        response = self.client.get(reverse("characters:character", kwargs={"pk": 99999}))
        self.assertEqual(response.status_code, 404)

    def test_mage_update_returns_404_for_invalid_pk(self):
        """Test that mage update returns 404 for non-existent character."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("characters:mage:update:mage", kwargs={"pk": 99999}))
        self.assertEqual(response.status_code, 404)

    def test_mage_full_update_returns_404_for_invalid_pk(self):
        """Test that mage full update returns 404 for non-existent character."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(
            reverse("characters:mage:update:mage_full", kwargs={"pk": 99999})
        )
        self.assertEqual(response.status_code, 404)
