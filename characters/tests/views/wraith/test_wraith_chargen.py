"""Tests for wraith_chargen views module."""

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from characters.models.core.archetype import Archetype
from characters.models.wraith.guild import Guild
from characters.models.wraith.shadow_archetype import ShadowArchetype
from characters.models.wraith.thorn import Thorn
from characters.models.wraith.wraith import Wraith
from game.models import Chronicle


class TestWraithBasicsView(TestCase):
    """Test WraithBasicsView for character creation."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="player", email="player@test.com", password="password"
        )
        self.nature = Archetype.objects.create(name="Survivor")
        self.demeanor = Archetype.objects.create(name="Caregiver")
        self.guild = Guild.objects.create(name="Usurers", willpower=5)

    def test_basics_view_requires_login(self):
        """Test that basics view requires login."""
        url = reverse("characters:wraith:create:wraith")
        response = self.client.get(url)
        # Should return 401 Unauthorized for unauthenticated users
        self.assertEqual(response.status_code, 401)

    def test_basics_view_accessible_when_logged_in(self):
        """Test that wraith basics view is accessible when logged in."""
        self.client.login(username="player", password="password")
        url = reverse("characters:wraith:create:wraith")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_basics_view_uses_correct_template(self):
        """Test that correct template is used for wraith basics view."""
        self.client.login(username="player", password="password")
        url = reverse("characters:wraith:create:wraith")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "characters/wraith/wraith/basics.html")

    def test_basics_view_has_storyteller_context(self):
        """Test that storyteller context is passed to template."""
        self.client.login(username="player", password="password")
        url = reverse("characters:wraith:create:wraith")
        response = self.client.get(url)
        self.assertIn("storyteller", response.context)


class TestWraithCharacterCreationView(TestCase):
    """Test WraithCharacterCreationView workflow."""

    def setUp(self):
        self.client = Client()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="password"
        )
        self.other_user = User.objects.create_user(
            username="other", email="other@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")

        self.wraith = Wraith.objects.create(
            name="Test Wraith",
            owner=self.owner,
            chronicle=self.chronicle,
            creation_status=1,  # At attribute step
        )

    def test_creation_view_accessible_to_owner(self):
        """Test that character creation view is accessible to owner."""
        self.client.login(username="owner", password="password")
        url = reverse("characters:wraith:wraith_chargen", kwargs={"pk": self.wraith.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_creation_view_denied_to_other_users(self):
        """Test that character creation view is denied to non-owners."""
        self.client.login(username="other", password="password")
        url = reverse("characters:wraith:wraith_chargen", kwargs={"pk": self.wraith.pk})
        response = self.client.get(url)
        self.assertIn(response.status_code, [403, 302, 404])


class TestWraithAttributeView(TestCase):
    """Test WraithAttributeView for attribute allocation."""

    def setUp(self):
        self.client = Client()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="password"
        )
        self.wraith = Wraith.objects.create(
            name="Test Wraith",
            owner=self.owner,
            creation_status=1,  # At attribute step
        )

    def test_attribute_view_accessible_to_owner(self):
        """Test that attribute view is accessible to owner."""
        self.client.login(username="owner", password="password")
        url = reverse("characters:wraith:wraith_chargen", kwargs={"pk": self.wraith.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestWraithAbilityView(TestCase):
    """Test WraithAbilityView for ability allocation."""

    def setUp(self):
        self.client = Client()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="password"
        )
        self.wraith = Wraith.objects.create(
            name="Test Wraith",
            owner=self.owner,
            creation_status=2,  # At ability step
        )

    def test_ability_view_accessible_to_owner(self):
        """Test that ability view is accessible to owner."""
        self.client.login(username="owner", password="password")
        url = reverse("characters:wraith:wraith_chargen", kwargs={"pk": self.wraith.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestWraithBackgroundsView(TestCase):
    """Test WraithBackgroundsView for background allocation."""

    def setUp(self):
        self.client = Client()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="password"
        )
        self.wraith = Wraith.objects.create(
            name="Test Wraith",
            owner=self.owner,
            creation_status=3,  # At backgrounds step
        )

    def test_backgrounds_view_accessible_to_owner(self):
        """Test that backgrounds view is accessible to owner."""
        self.client.login(username="owner", password="password")
        url = reverse("characters:wraith:wraith_chargen", kwargs={"pk": self.wraith.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestWraithArcanosView(TestCase):
    """Test WraithArcanosView for arcanos allocation."""

    def setUp(self):
        self.client = Client()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="password"
        )
        self.wraith = Wraith.objects.create(
            name="Test Wraith",
            owner=self.owner,
            creation_status=4,  # At arcanos step
        )

    def test_arcanos_view_accessible_to_owner(self):
        """Test that arcanos view is accessible to owner."""
        self.client.login(username="owner", password="password")
        url = reverse("characters:wraith:wraith_chargen", kwargs={"pk": self.wraith.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_arcanos_form_validation_requires_5_dots(self):
        """Test that arcanos allocation requires exactly 5 dots."""
        self.client.login(username="owner", password="password")
        url = reverse("characters:wraith:wraith_chargen", kwargs={"pk": self.wraith.pk})

        # Submit with wrong total (only 3 dots)
        data = {
            "argos": 1,
            "castigate": 1,
            "embody": 1,
            "fatalism": 0,
            "flux": 0,
            "inhabit": 0,
            "keening": 0,
            "lifeweb": 0,
            "moliate": 0,
            "mnemosynis": 0,
            "outrage": 0,
            "pandemonium": 0,
            "phantasm": 0,
            "usury": 0,
            "intimation": 0,
        }
        response = self.client.post(url, data)
        # Should not advance creation status
        self.wraith.refresh_from_db()
        self.assertEqual(self.wraith.creation_status, 4)

    def test_arcanos_allocation_advances_creation(self):
        """Test that valid arcanos allocation advances creation status."""
        self.client.login(username="owner", password="password")
        url = reverse("characters:wraith:wraith_chargen", kwargs={"pk": self.wraith.pk})

        # Submit with correct total (5 dots)
        data = {
            "argos": 2,
            "castigate": 2,
            "embody": 1,
            "fatalism": 0,
            "flux": 0,
            "inhabit": 0,
            "keening": 0,
            "lifeweb": 0,
            "moliate": 0,
            "mnemosynis": 0,
            "outrage": 0,
            "pandemonium": 0,
            "phantasm": 0,
            "usury": 0,
            "intimation": 0,
        }
        response = self.client.post(url, data)
        self.wraith.refresh_from_db()
        self.assertEqual(self.wraith.creation_status, 5)


class TestWraithShadowView(TestCase):
    """Test WraithShadowView for shadow archetype selection."""

    def setUp(self):
        self.client = Client()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="password"
        )
        self.shadow_archetype = ShadowArchetype.objects.create(
            name="The Parent",
            description="Protective but controlling",
            point_cost=2,
        )
        self.wraith = Wraith.objects.create(
            name="Test Wraith",
            owner=self.owner,
            creation_status=5,  # At shadow step
        )

    def test_shadow_view_accessible_to_owner(self):
        """Test that shadow view is accessible to owner."""
        self.client.login(username="owner", password="password")
        url = reverse("characters:wraith:wraith_chargen", kwargs={"pk": self.wraith.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_shadow_view_has_archetypes_in_context(self):
        """Test that shadow archetypes are in context."""
        self.client.login(username="owner", password="password")
        url = reverse("characters:wraith:wraith_chargen", kwargs={"pk": self.wraith.pk})
        response = self.client.get(url)
        self.assertIn("shadow_archetypes", response.context)

    def test_shadow_view_has_thorns_in_context(self):
        """Test that thorns are in context."""
        Thorn.objects.create(name="Test Thorn", point_cost=1)
        self.client.login(username="owner", password="password")
        url = reverse("characters:wraith:wraith_chargen", kwargs={"pk": self.wraith.pk})
        response = self.client.get(url)
        self.assertIn("thorns", response.context)


class TestWraithPassionsView(TestCase):
    """Test WraithPassionsView for passion allocation."""

    def setUp(self):
        self.client = Client()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="password"
        )
        self.wraith = Wraith.objects.create(
            name="Test Wraith",
            owner=self.owner,
            creation_status=6,  # At passions step
        )

    def test_passions_view_accessible_to_owner(self):
        """Test that passions view is accessible to owner."""
        self.client.login(username="owner", password="password")
        url = reverse("characters:wraith:wraith_chargen", kwargs={"pk": self.wraith.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_passions_context_has_points_info(self):
        """Test that passions context has point information."""
        self.client.login(username="owner", password="password")
        url = reverse("characters:wraith:wraith_chargen", kwargs={"pk": self.wraith.pk})
        response = self.client.get(url)
        self.assertIn("passion_points_total", response.context)
        self.assertIn("passion_points_spent", response.context)
        self.assertIn("passion_points_remaining", response.context)


class TestWraithFettersView(TestCase):
    """Test WraithFettersView for fetter allocation."""

    def setUp(self):
        self.client = Client()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="password"
        )
        self.wraith = Wraith.objects.create(
            name="Test Wraith",
            owner=self.owner,
            creation_status=7,  # At fetters step
        )

    def test_fetters_view_accessible_to_owner(self):
        """Test that fetters view is accessible to owner."""
        self.client.login(username="owner", password="password")
        url = reverse("characters:wraith:wraith_chargen", kwargs={"pk": self.wraith.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_fetters_context_has_points_info(self):
        """Test that fetters context has point information."""
        self.client.login(username="owner", password="password")
        url = reverse("characters:wraith:wraith_chargen", kwargs={"pk": self.wraith.pk})
        response = self.client.get(url)
        self.assertIn("fetter_points_total", response.context)
        self.assertIn("fetter_points_spent", response.context)
        self.assertIn("fetter_points_remaining", response.context)


class TestWraithExtrasView(TestCase):
    """Test WraithExtrasView for description and history."""

    def setUp(self):
        self.client = Client()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="password"
        )
        self.wraith = Wraith.objects.create(
            name="Test Wraith",
            owner=self.owner,
            creation_status=8,  # At extras step
        )

    def test_extras_view_accessible_to_owner(self):
        """Test that extras view is accessible to owner."""
        self.client.login(username="owner", password="password")
        url = reverse("characters:wraith:wraith_chargen", kwargs={"pk": self.wraith.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_extras_requires_death_info(self):
        """Test that death info is required for wraith extras."""
        self.client.login(username="owner", password="password")
        url = reverse("characters:wraith:wraith_chargen", kwargs={"pk": self.wraith.pk})

        # Submit without death info
        data = {
            "date_of_birth": "1990-01-01",
            "apparent_age": 30,
            "age": 30,
            "age_at_death": "",  # Missing
            "death_description": "",  # Missing
            "description": "A ghostly figure",
            "history": "Lived a normal life",
            "goals": "Find peace",
            "notes": "",
            "public_info": "",
        }
        response = self.client.post(url, data)
        # Should not advance creation status
        self.wraith.refresh_from_db()
        self.assertEqual(self.wraith.creation_status, 8)


class TestWraithFreebiesView(TestCase):
    """Test WraithFreebiesView for freebie point allocation."""

    def setUp(self):
        self.client = Client()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="password"
        )
        self.wraith = Wraith.objects.create(
            name="Test Wraith",
            owner=self.owner,
            creation_status=9,  # At freebies step
            freebies=15,
        )

    def test_freebies_view_accessible_to_owner(self):
        """Test that freebies view is accessible to owner."""
        self.client.login(username="owner", password="password")
        url = reverse("characters:wraith:wraith_chargen", kwargs={"pk": self.wraith.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestWraithFreebieFormPopulationView(TestCase):
    """Test WraithFreebieFormPopulationView for populating freebie options."""

    def setUp(self):
        self.client = Client()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="password"
        )
        self.wraith = Wraith.objects.create(
            name="Test Wraith",
            owner=self.owner,
            creation_status=9,
            freebies=15,
        )


class TestWraithLanguagesView(TestCase):
    """Test WraithLanguagesView for language selection."""

    def setUp(self):
        self.client = Client()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="password"
        )
        self.wraith = Wraith.objects.create(
            name="Test Wraith",
            owner=self.owner,
            creation_status=10,  # At languages step
        )

    def test_languages_view_accessible_to_owner(self):
        """Test that languages view is accessible to owner."""
        self.client.login(username="owner", password="password")
        url = reverse("characters:wraith:wraith_chargen", kwargs={"pk": self.wraith.pk})
        response = self.client.get(url)
        # May redirect if no Language merit
        self.assertIn(response.status_code, [200, 302])


class TestWraithAlliesView(TestCase):
    """Test WraithAlliesView for NPC allies."""

    def setUp(self):
        self.client = Client()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="password"
        )
        self.wraith = Wraith.objects.create(
            name="Test Wraith",
            owner=self.owner,
            creation_status=11,  # At allies step
        )

    def test_allies_view_accessible_to_owner(self):
        """Test that allies view is accessible to owner."""
        self.client.login(username="owner", password="password")
        url = reverse("characters:wraith:wraith_chargen", kwargs={"pk": self.wraith.pk})
        response = self.client.get(url)
        # May redirect if no allies background
        self.assertIn(response.status_code, [200, 302])


class TestWraithSpecialtiesView(TestCase):
    """Test WraithSpecialtiesView for specialty assignment."""

    def setUp(self):
        self.client = Client()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="password"
        )
        self.wraith = Wraith.objects.create(
            name="Test Wraith",
            owner=self.owner,
            creation_status=14,  # At specialties step
        )

    def test_specialties_view_accessible_to_owner(self):
        """Test that specialties view is accessible to owner."""
        self.client.login(username="owner", password="password")
        url = reverse("characters:wraith:wraith_chargen", kwargs={"pk": self.wraith.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestWraithChargenView404Handling(TestCase):
    """Test 404 error handling for Wraith chargen views with invalid IDs."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.chronicle.storytellers.add(self.user)

    def test_chargen_returns_404_for_invalid_pk(self):
        """Test that chargen returns 404 for non-existent character."""
        self.client.login(username="testuser", password="password")
        url = reverse("characters:wraith:wraith_chargen", kwargs={"pk": 99999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
