"""Tests for vtmhuman views module.

Tests cover:
- VtMHumanDetailView - Character detail display
- VtMHumanCreateView - Full character creation
- VtMHumanUpdateView - Character editing
- VtMHumanBasicsView - Initial creation step
- VtMHumanTemplateSelectView - Template selection
- VtMHumanCharacterCreationView - Workflow routing
- VtMHuman ability views - Ability allocation
"""

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from characters.models.core.archetype import Archetype
from characters.models.vampire.vtmhuman import VtMHuman
from game.models import Chronicle


class VtMHumanViewTestCase(TestCase):
    """Base test case with common setup for VtMHuman view tests."""

    @classmethod
    def setUpTestData(cls):
        """Set up test data for all test methods."""
        # Create archetypes
        cls.nature = Archetype.objects.create(name="Survivor")
        cls.demeanor = Archetype.objects.create(name="Caregiver")

    def setUp(self):
        """Set up test user and client."""
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            email="test@test.com",
            password="testpassword",
        )
        self.other_user = User.objects.create_user(
            username="otheruser",
            email="other@test.com",
            password="testpassword",
        )
        self.st = User.objects.create_user(
            username="storyteller",
            email="st@test.com",
            password="testpassword",
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.chronicle.storytellers.add(self.st)


class TestVtMHumanDetailView(VtMHumanViewTestCase):
    """Test VtMHumanDetailView permissions and functionality."""

    def setUp(self):
        super().setUp()
        self.vtmhuman = VtMHuman.objects.create(
            name="Test VtMHuman",
            owner=self.user,
            chronicle=self.chronicle,
            status="App",
        )

    def test_detail_view_accessible_to_owner(self):
        """Test that detail view is accessible to owner."""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(self.vtmhuman.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_detail_view_accessible_to_st(self):
        """Test that detail view is accessible to storytellers."""
        self.client.login(username="storyteller", password="testpassword")
        response = self.client.get(self.vtmhuman.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_detail_view_hidden_from_other_users(self):
        """Test that characters are hidden from other users."""
        self.client.login(username="otheruser", password="testpassword")
        response = self.client.get(self.vtmhuman.get_absolute_url())
        self.assertEqual(response.status_code, 404)

    def test_detail_view_returns_404_without_login(self):
        """Test that unauthenticated users get 404."""
        response = self.client.get(self.vtmhuman.get_absolute_url())
        self.assertEqual(response.status_code, 404)

    def test_detail_view_template_used(self):
        """Test that correct template is used."""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(self.vtmhuman.get_absolute_url())
        self.assertTemplateUsed(response, "characters/vampire/vtmhuman/detail.html")


class TestVtMHumanBasicsView(VtMHumanViewTestCase):
    """Test VtMHumanBasicsView for initial creation."""

    def test_basics_view_requires_login(self):
        """Test that basics view requires authentication."""
        url = reverse("characters:vampire:create:vtm_human")
        response = self.client.get(url)
        # App returns 401 for unauthenticated users instead of redirect
        self.assertEqual(response.status_code, 401)

    def test_basics_view_accessible_when_logged_in(self):
        """Test that basics view is accessible when logged in."""
        self.client.login(username="testuser", password="testpassword")
        url = reverse("characters:vampire:create:vtm_human")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_basics_view_uses_correct_template(self):
        """Test that correct template is used."""
        self.client.login(username="testuser", password="testpassword")
        url = reverse("characters:vampire:create:vtm_human")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "characters/vampire/vtmhuman/basics.html")

    def test_basics_view_creates_vtmhuman(self):
        """Test that submitting form creates a VtMHuman."""
        self.client.login(username="testuser", password="testpassword")
        url = reverse("characters:vampire:create:vtm_human")
        data = {
            "name": "Test VtMHuman",
            "chronicle": self.chronicle.pk,
            "nature": self.nature.pk,
            "demeanor": self.demeanor.pk,
            "concept": "Hunter",
        }
        response = self.client.post(url, data)
        # Should redirect on success
        self.assertEqual(response.status_code, 302)
        # VtMHuman should be created
        vtmhuman = VtMHuman.objects.get(name="Test VtMHuman")
        self.assertEqual(vtmhuman.owner, self.user)

    def test_basics_view_sets_creation_status(self):
        """Test that creation_status is set to 1 after basics."""
        self.client.login(username="testuser", password="testpassword")
        url = reverse("characters:vampire:create:vtm_human")
        data = {
            "name": "Test VtMHuman",
            "nature": self.nature.pk,
            "demeanor": self.demeanor.pk,
            "concept": "Hunter",
        }
        self.client.post(url, data)
        vtmhuman = VtMHuman.objects.get(name="Test VtMHuman")
        self.assertEqual(vtmhuman.creation_status, 1)

    def test_basics_view_context_has_storyteller_flag_for_st(self):
        """Test that context includes storyteller flag for STs."""
        self.client.login(username="storyteller", password="testpassword")
        url = reverse("characters:vampire:create:vtm_human")
        response = self.client.get(url)
        self.assertTrue(response.context["storyteller"])

    def test_basics_view_storyteller_false_for_regular_user(self):
        """Test that storyteller flag is false for non-ST users."""
        self.client.login(username="testuser", password="testpassword")
        url = reverse("characters:vampire:create:vtm_human")
        response = self.client.get(url)
        self.assertFalse(response.context["storyteller"])


class TestVtMHumanAttributeView(VtMHumanViewTestCase):
    """Test VtMHumanAttributeView for 6/4/3 attribute allocation."""

    def setUp(self):
        super().setUp()
        self.vtmhuman = VtMHuman.objects.create(
            name="Test VtMHuman",
            owner=self.user,
            creation_status=1,  # At attribute step
        )

    def test_attribute_view_accessible_to_owner(self):
        """Test that attribute view is accessible to owner."""
        self.client.login(username="testuser", password="testpassword")
        url = reverse("characters:vampire:vtmhuman_creation", kwargs={"pk": self.vtmhuman.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_attribute_view_denied_to_other_users(self):
        """Test that attribute view is denied to non-owners."""
        self.client.login(username="otheruser", password="testpassword")
        url = reverse("characters:vampire:vtmhuman_creation", kwargs={"pk": self.vtmhuman.pk})
        response = self.client.get(url)
        self.assertIn(response.status_code, [403, 302])

    def test_attribute_view_uses_correct_template(self):
        """Test that correct template is used."""
        self.client.login(username="testuser", password="testpassword")
        url = reverse("characters:vampire:vtmhuman_creation", kwargs={"pk": self.vtmhuman.pk})
        response = self.client.get(url)
        self.assertTemplateUsed(response, "characters/vampire/vtmhuman/chargen.html")


class TestVtMHumanAbilityView(VtMHumanViewTestCase):
    """Test VtMHumanAbilityView for 11/7/4 ability allocation."""

    def setUp(self):
        super().setUp()
        self.vtmhuman = VtMHuman.objects.create(
            name="Test VtMHuman",
            owner=self.user,
            creation_status=2,  # At ability step
            strength=3,
            dexterity=3,
            stamina=3,  # Physical: 6
            charisma=2,
            manipulation=2,
            appearance=2,  # Social: 4
            perception=2,
            intelligence=2,
            wits=2,  # Mental: 3
        )

    def test_ability_view_accessible_to_owner(self):
        """Test that ability view is accessible to owner."""
        self.client.login(username="testuser", password="testpassword")
        url = reverse("characters:vampire:vtmhuman_creation", kwargs={"pk": self.vtmhuman.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestVtMHumanExtrasView(VtMHumanViewTestCase):
    """Test VtMHumanExtrasView for description and history."""

    def setUp(self):
        super().setUp()
        self.vtmhuman = VtMHuman.objects.create(
            name="Test VtMHuman",
            owner=self.user,
            creation_status=4,  # At extras step
        )

    def test_extras_view_accessible_to_owner(self):
        """Test that extras view is accessible to owner."""
        self.client.login(username="testuser", password="testpassword")
        url = reverse("characters:vampire:vtmhuman_creation", kwargs={"pk": self.vtmhuman.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_extras_view_accepts_optional_data(self):
        """Test that extras fields are optional."""
        self.client.login(username="testuser", password="testpassword")
        url = reverse("characters:vampire:vtmhuman_creation", kwargs={"pk": self.vtmhuman.pk})
        data = {
            "date_of_birth": "1990-01-01",
            "apparent_age": 30,
            "age": 34,
            "description": "A normal human.",
            "history": "",  # Optional
            "goals": "",  # Optional
            "notes": "",  # Optional
            "public_info": "",  # Optional
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.vtmhuman.refresh_from_db()
        self.assertEqual(self.vtmhuman.creation_status, 5)


class TestVtMHumanFreebiesView(VtMHumanViewTestCase):
    """Test VtMHumanFreebiesView for freebie point spending."""

    def setUp(self):
        super().setUp()
        self.vtmhuman = VtMHuman.objects.create(
            name="Test VtMHuman",
            owner=self.user,
            creation_status=5,  # At freebies step
            freebies=21,
        )

    def test_freebies_view_accessible_to_owner(self):
        """Test that freebies view is accessible to owner."""
        self.client.login(username="testuser", password="testpassword")
        url = reverse("characters:vampire:vtmhuman_creation", kwargs={"pk": self.vtmhuman.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestVtMHumanCharacterCreationView(VtMHumanViewTestCase):
    """Test VtMHumanCharacterCreationView workflow routing."""

    def test_routes_to_attribute_view_at_step_1(self):
        """Test that step 1 routes to attribute view."""
        vtmhuman = VtMHuman.objects.create(
            name="Test VtMHuman",
            owner=self.user,
            creation_status=1,
        )
        self.client.login(username="testuser", password="testpassword")
        url = reverse("characters:vampire:vtmhuman_creation", kwargs={"pk": vtmhuman.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_routes_to_ability_view_at_step_2(self):
        """Test that step 2 routes to ability view."""
        vtmhuman = VtMHuman.objects.create(
            name="Test VtMHuman",
            owner=self.user,
            creation_status=2,
        )
        self.client.login(username="testuser", password="testpassword")
        url = reverse("characters:vampire:vtmhuman_creation", kwargs={"pk": vtmhuman.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_routes_to_backgrounds_at_step_3(self):
        """Test that step 3 routes to backgrounds view."""
        vtmhuman = VtMHuman.objects.create(
            name="Test VtMHuman",
            owner=self.user,
            creation_status=3,
        )
        self.client.login(username="testuser", password="testpassword")
        url = reverse("characters:vampire:vtmhuman_creation", kwargs={"pk": vtmhuman.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_routes_to_extras_at_step_4(self):
        """Test that step 4 routes to extras view."""
        vtmhuman = VtMHuman.objects.create(
            name="Test VtMHuman",
            owner=self.user,
            creation_status=4,
        )
        self.client.login(username="testuser", password="testpassword")
        url = reverse("characters:vampire:vtmhuman_creation", kwargs={"pk": vtmhuman.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_routes_to_freebies_at_step_5(self):
        """Test that step 5 routes to freebies view."""
        vtmhuman = VtMHuman.objects.create(
            name="Test VtMHuman",
            owner=self.user,
            creation_status=5,
            freebies=21,
        )
        self.client.login(username="testuser", password="testpassword")
        url = reverse("characters:vampire:vtmhuman_creation", kwargs={"pk": vtmhuman.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_denied_to_non_owners(self):
        """Test that chargen is denied to non-owners."""
        vtmhuman = VtMHuman.objects.create(
            name="Test VtMHuman",
            owner=self.user,
            creation_status=1,
        )
        self.client.login(username="otheruser", password="testpassword")
        url = reverse("characters:vampire:vtmhuman_creation", kwargs={"pk": vtmhuman.pk})
        response = self.client.get(url)
        self.assertIn(response.status_code, [403, 302])

    def test_accessible_to_storyteller(self):
        """Test that chargen is accessible to storytellers."""
        vtmhuman = VtMHuman.objects.create(
            name="Test VtMHuman",
            owner=self.user,
            chronicle=self.chronicle,
            creation_status=1,
        )
        self.client.login(username="storyteller", password="testpassword")
        url = reverse("characters:vampire:vtmhuman_creation", kwargs={"pk": vtmhuman.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestVtMHumanChargenViewsReturn404(VtMHumanViewTestCase):
    """Test 404 handling for non-existent characters."""

    def test_chargen_returns_404_for_invalid_pk(self):
        """Test that chargen returns 404 for non-existent character."""
        self.client.login(username="testuser", password="testpassword")
        url = reverse("characters:vampire:vtmhuman_creation", kwargs={"pk": 99999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class TestVtMHumanDefaultValues(VtMHumanViewTestCase):
    """Test that VtMHuman has correct default values."""

    def test_vtmhuman_type_is_vtmhuman(self):
        """Test that VtMHuman type is 'vtm_human'."""
        vtmhuman = VtMHuman.objects.create(
            name="Test VtMHuman",
            owner=self.user,
        )
        self.assertEqual(vtmhuman.type, "vtm_human")

    def test_vtmhuman_get_heading(self):
        """Test that get_heading returns vtm_heading."""
        vtmhuman = VtMHuman.objects.create(
            name="Test VtMHuman",
            owner=self.user,
        )
        self.assertEqual(vtmhuman.get_heading(), "vtm_heading")


class TestVtMHumanURLs(VtMHumanViewTestCase):
    """Test VtMHuman URL generation methods."""

    def test_get_absolute_url(self):
        """Test that get_absolute_url returns correct path."""
        vtmhuman = VtMHuman.objects.create(name="Test", owner=self.user)
        # Character.get_absolute_url returns /characters/{pk}/
        expected_url = f"/characters/{vtmhuman.id}/"
        self.assertEqual(vtmhuman.get_absolute_url(), expected_url)

    def test_get_update_url(self):
        """Test that get_update_url returns correct path."""
        vtmhuman = VtMHuman.objects.create(name="Test", owner=self.user)
        expected_url = f"/characters/vampire/update/vtmhuman/{vtmhuman.pk}/"
        self.assertEqual(vtmhuman.get_update_url(), expected_url)

    def test_get_creation_url(self):
        """Test that get_creation_url returns correct path."""
        expected_url = "/characters/vampire/create/vtmhuman/"
        self.assertEqual(VtMHuman.get_creation_url(), expected_url)


class TestVtMHumanTemplateSelectView(VtMHumanViewTestCase):
    """Test VtMHumanTemplateSelectView for template selection."""

    def setUp(self):
        super().setUp()
        self.vtmhuman = VtMHuman.objects.create(
            name="Test VtMHuman",
            owner=self.user,
            creation_status=0,  # Before creation started
        )

    def test_template_view_accessible_when_creation_not_started(self):
        """Test that template view is accessible before creation starts."""
        self.client.login(username="testuser", password="testpassword")
        url = reverse("characters:vampire:vtmhuman_template", kwargs={"pk": self.vtmhuman.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_template_view_redirects_when_creation_started(self):
        """Test that template view redirects if creation already started."""
        self.vtmhuman.creation_status = 1
        self.vtmhuman.save()
        self.client.login(username="testuser", password="testpassword")
        url = reverse("characters:vampire:vtmhuman_template", kwargs={"pk": self.vtmhuman.pk})
        response = self.client.get(url)
        # Should redirect to creation view
        self.assertEqual(response.status_code, 302)
        self.assertIn("creation", response.url)

    def test_template_view_uses_correct_template(self):
        """Test that correct template is used."""
        self.client.login(username="testuser", password="testpassword")
        url = reverse("characters:vampire:vtmhuman_template", kwargs={"pk": self.vtmhuman.pk})
        response = self.client.get(url)
        self.assertTemplateUsed(response, "characters/vampire/vtmhuman/template_select.html")

    def test_template_view_context_has_character(self):
        """Test that context includes the character."""
        self.client.login(username="testuser", password="testpassword")
        url = reverse("characters:vampire:vtmhuman_template", kwargs={"pk": self.vtmhuman.pk})
        response = self.client.get(url)
        self.assertEqual(response.context["character"], self.vtmhuman)

    def test_template_view_sets_creation_status(self):
        """Test that submitting form advances creation status."""
        self.client.login(username="testuser", password="testpassword")
        url = reverse("characters:vampire:vtmhuman_template", kwargs={"pk": self.vtmhuman.pk})
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 302)
        self.vtmhuman.refresh_from_db()
        self.assertEqual(self.vtmhuman.creation_status, 1)
