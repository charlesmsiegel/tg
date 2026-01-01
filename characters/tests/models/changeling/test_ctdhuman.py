import unittest

from characters.models.changeling.changeling import Changeling
from characters.models.changeling.ctdhuman import CtDHuman
from characters.tests.utils import changeling_setup
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from game.models import Chronicle


class TestCtDHuman(TestCase):
    def setUp(self) -> None:
        self.player = User.objects.create_user(username="User1", password="12345")
        self.character = Changeling.objects.create(owner=self.player, name="Test Changeling")
        changeling_setup()

    def set_abilities(self):
        self.character.kenning = 3
        self.character.leadership = 2
        self.character.crafts = 3
        self.character.animal_ken = 2
        self.character.larceny = 2
        self.character.enigmas = 2
        self.character.gremayre = 3

    def test_ctdhuman_type(self):
        """Test that CtDHuman has correct type attribute."""
        ctdhuman = CtDHuman.objects.create(owner=self.player, name="Test CtDHuman")
        self.assertEqual(ctdhuman.type, "ctd_human")

    def test_ctdhuman_gameline(self):
        """Test that CtDHuman has correct gameline."""
        ctdhuman = CtDHuman.objects.create(owner=self.player, name="Test CtDHuman")
        self.assertEqual(ctdhuman.gameline, "ctd")

    def test_ctdhuman_freebie_step(self):
        """Test that CtDHuman has correct freebie step."""
        self.assertEqual(CtDHuman.freebie_step, 5)

    def test_ctdhuman_talents_list(self):
        """Test that talents list includes CtD-specific abilities."""
        self.assertIn("kenning", CtDHuman.talents)
        self.assertIn("leadership", CtDHuman.talents)

    def test_ctdhuman_skills_list(self):
        """Test that skills list includes CtD-specific abilities."""
        self.assertIn("animal_ken", CtDHuman.skills)
        self.assertIn("larceny", CtDHuman.skills)
        self.assertIn("performance", CtDHuman.skills)
        self.assertIn("survival", CtDHuman.skills)

    def test_ctdhuman_knowledges_list(self):
        """Test that knowledges list includes CtD-specific abilities."""
        self.assertIn("enigmas", CtDHuman.knowledges)
        self.assertIn("gremayre", CtDHuman.knowledges)
        self.assertIn("law", CtDHuman.knowledges)
        self.assertIn("politics", CtDHuman.knowledges)
        self.assertIn("technology", CtDHuman.knowledges)

    def test_ctdhuman_allowed_backgrounds(self):
        """Test that allowed backgrounds includes CtD-specific backgrounds."""
        self.assertIn("chimera", CtDHuman.allowed_backgrounds)
        self.assertIn("dreamers", CtDHuman.allowed_backgrounds)
        self.assertIn("holdings", CtDHuman.allowed_backgrounds)
        self.assertIn("remembrance", CtDHuman.allowed_backgrounds)
        self.assertIn("retinue", CtDHuman.allowed_backgrounds)
        self.assertIn("title", CtDHuman.allowed_backgrounds)
        self.assertIn("treasure", CtDHuman.allowed_backgrounds)

    def test_get_talents(self):
        self.assertEqual(
            self.character.get_talents(),
            {
                "alertness": 0,
                "athletics": 0,
                "brawl": 0,
                "empathy": 0,
                "expression": 0,
                "intimidation": 0,
                "kenning": 0,
                "leadership": 0,
                "streetwise": 0,
                "subterfuge": 0,
            },
        )
        self.set_abilities()
        self.assertEqual(
            self.character.get_talents(),
            {
                "alertness": 0,
                "athletics": 0,
                "brawl": 0,
                "empathy": 0,
                "expression": 0,
                "intimidation": 0,
                "streetwise": 0,
                "subterfuge": 0,
                "kenning": 3,
                "leadership": 2,
            },
        )

    def test_get_skills(self):
        self.assertEqual(
            self.character.get_skills(),
            {
                "animal_ken": 0,
                "crafts": 0,
                "drive": 0,
                "etiquette": 0,
                "firearms": 0,
                "larceny": 0,
                "melee": 0,
                "performance": 0,
                "stealth": 0,
                "survival": 0,
            },
        )
        self.set_abilities()
        self.assertEqual(
            self.character.get_skills(),
            {
                "crafts": 3,
                "drive": 0,
                "etiquette": 0,
                "firearms": 0,
                "melee": 0,
                "stealth": 0,
                "animal_ken": 2,
                "larceny": 2,
                "performance": 0,
                "survival": 0,
            },
        )

    def test_get_knowledges(self):
        self.assertEqual(
            self.character.get_knowledges(),
            {
                "academics": 0,
                "computer": 0,
                "enigmas": 0,
                "gremayre": 0,
                "investigation": 0,
                "law": 0,
                "medicine": 0,
                "politics": 0,
                "science": 0,
                "technology": 0,
            },
        )
        self.set_abilities()
        self.assertEqual(
            self.character.get_knowledges(),
            {
                "academics": 0,
                "computer": 0,
                "investigation": 0,
                "medicine": 0,
                "science": 0,
                "enigmas": 2,
                "gremayre": 3,
                "law": 0,
                "politics": 0,
                "technology": 0,
            },
        )

    def test_get_backgrounds(self):
        self.assertEqual(
            self.character.get_backgrounds(),
            {
                "chimera": 0,
                "contacts": 0,
                "dreamers": 0,
                "holdings": 0,
                "mentor": 0,
                "remembrance": 0,
                "resources": 0,
                "retinue": 0,
                "title": 0,
                "treasure": 0,
            },
        )
        self.character.contacts = 2
        self.character.title = 3
        self.character.dreamers = 4
        self.character.resources = 5
        self.assertEqual(
            self.character.get_backgrounds(),
            {
                "contacts": 2,
                "mentor": 0,
                "chimera": 0,
                "dreamers": 4,
                "holdings": 0,
                "remembrance": 0,
                "resources": 5,
                "retinue": 0,
                "title": 3,
                "treasure": 0,
            },
        )


class TestCtDHumanDetailView(TestCase):
    def setUp(self) -> None:
        self.player = User.objects.create_user(username="Player", password="password")
        self.ctdhuman = CtDHuman.objects.create(
            name="Test CtDHuman", owner=self.player, status="App"
        )
        self.url = self.ctdhuman.get_absolute_url()

    def test_ctdhuman_detail_view_status_code(self):
        self.client.login(username="Player", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_ctdhuman_detail_view_templates(self):
        self.client.login(username="Player", password="password")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/changeling/ctdhuman/detail.html")


class TestCtDHumanCreateView(TestCase):
    def setUp(self):
        self.st = User.objects.create_user(username="ST", password="password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.chronicle.storytellers.add(self.st)
        self.valid_data = {
            "name": "CtDHuman",
            "owner": self.st.id,
            "description": "Test",
            "strength": 1,
            "dexterity": 1,
            "stamina": 1,
            "perception": 1,
            "intelligence": 1,
            "wits": 1,
            "charisma": 1,
            "manipulation": 1,
            "appearance": 1,
            "alertness": 1,
            "athletics": 1,
            "brawl": 1,
            "empathy": 1,
            "expression": 1,
            "intimidation": 1,
            "streetwise": 1,
            "subterfuge": 1,
            "crafts": 1,
            "drive": 1,
            "etiquette": 1,
            "firearms": 1,
            "melee": 1,
            "stealth": 1,
            "academics": 1,
            "computer": 1,
            "investigation": 1,
            "medicine": 1,
            "science": 1,
            "contacts": 1,
            "mentor": 1,
            "willpower": 3,
            "temporary_willpower": 3,
            "age": 1,
            "apparent_age": 1,
            "history": "ava",
            "goals": "ava",
            "notes": "ava",
            "kenning": 1,
            "leadership": 1,
            "animal_ken": 1,
            "larceny": 1,
            "performance": 1,
            "survival": 1,
            "enigmas": 1,
            "gremayre": 1,
            "law": 1,
            "politics": 1,
            "technology": 1,
            "chimera": 1,
            "dreamers": 1,
            "holdings": 1,
            "remembrance": 1,
            "resources": 1,
            "retinue": 1,
            "title": 1,
            "treasure": 1,
        }
        self.url = CtDHuman.get_creation_url()

    def test_create_view_status_code(self):
        self.client.login(username="ST", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        self.client.login(username="ST", password="password")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/changeling/ctdhuman/basics.html")

    def test_create_view_successful_post(self):
        # Test basic creation with name only - the basics form
        self.client.login(username="ST", password="password")
        response = self.client.post(self.url, data={"name": "Test CtDHuman"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(CtDHuman.objects.count(), 1)
        self.assertEqual(CtDHuman.objects.first().name, "Test CtDHuman")


class TestCtDHumanUpdateView(TestCase):
    def setUp(self):
        self.st = User.objects.create_user(username="ST", password="password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.chronicle.storytellers.add(self.st)
        self.ctdhuman = CtDHuman.objects.create(
            name="Test CtDHuman",
            description="Test description",
            owner=self.st,
            chronicle=self.chronicle,
        )
        self.valid_data = {
            "name": "CtDHuman Updated",
            "owner": self.st.id,
            "description": "Test",
            "strength": 1,
            "dexterity": 1,
            "stamina": 1,
            "perception": 1,
            "intelligence": 1,
            "wits": 1,
            "charisma": 1,
            "manipulation": 1,
            "appearance": 1,
            "alertness": 1,
            "athletics": 1,
            "brawl": 1,
            "empathy": 1,
            "expression": 1,
            "intimidation": 1,
            "streetwise": 1,
            "subterfuge": 1,
            "crafts": 1,
            "drive": 1,
            "etiquette": 1,
            "firearms": 1,
            "melee": 1,
            "stealth": 1,
            "academics": 1,
            "computer": 1,
            "investigation": 1,
            "medicine": 1,
            "science": 1,
            "contacts": 1,
            "mentor": 1,
            "willpower": 3,
            "temporary_willpower": 3,
            "age": 1,
            "apparent_age": 1,
            "history": "ava",
            "goals": "ava",
            "notes": "ava",
            "kenning": 1,
            "leadership": 1,
            "animal_ken": 1,
            "larceny": 1,
            "performance": 1,
            "survival": 1,
            "enigmas": 1,
            "gremayre": 1,
            "law": 1,
            "politics": 1,
            "technology": 1,
            "chimera": 1,
            "dreamers": 1,
            "holdings": 1,
            "remembrance": 1,
            "resources": 1,
            "retinue": 1,
            "title": 1,
            "treasure": 1,
        }
        self.url = self.ctdhuman.get_update_url()

    def test_update_view_status_code(self):
        self.client.login(username="ST", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        self.client.login(username="ST", password="password")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/changeling/ctdhuman/form.html")

    def test_update_view_successful_post(self):
        self.client.login(username="ST", password="password")
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.ctdhuman.refresh_from_db()
        self.assertEqual(self.ctdhuman.name, "CtDHuman Updated")
        self.assertEqual(self.ctdhuman.description, "Test")


class TestCtDHumanBasicsView(TestCase):
    """Tests for the CtDHumanBasicsView."""

    def setUp(self):
        self.player = User.objects.create_user(username="User1", password="12345")
        self.st = User.objects.create_user(username="ST", password="12345")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.chronicle.storytellers.add(self.st)

    def test_basics_view_requires_login(self):
        """Test that the basics view requires login."""
        response = self.client.get(CtDHuman.get_creation_url())
        # App returns 401 for unauthenticated users instead of redirect
        self.assertEqual(response.status_code, 401)

    def test_basics_view_logged_in(self):
        """Test that logged in users can access the basics view."""
        self.client.login(username="User1", password="12345")
        response = self.client.get(CtDHuman.get_creation_url())
        self.assertEqual(response.status_code, 200)

    def test_basics_view_shows_storyteller_context_for_st(self):
        """Test that storyteller context is True for storytellers."""
        self.client.login(username="ST", password="12345")
        response = self.client.get(CtDHuman.get_creation_url())
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["storyteller"])

    def test_basics_view_shows_storyteller_context_for_player(self):
        """Test that storyteller context is False for regular players."""
        self.client.login(username="User1", password="12345")
        response = self.client.get(CtDHuman.get_creation_url())
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["storyteller"])


@unittest.skip("URL 'ctdhuman_extras' not implemented yet")
class TestCtDHumanExtrasView(TestCase):
    """Tests for the CtDHumanExtrasView."""

    def setUp(self):
        self.st = User.objects.create_user(username="ST", password="password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.chronicle.storytellers.add(self.st)
        changeling_setup()
        self.ctdhuman = CtDHuman.objects.create(
            name="Test CtDHuman",
            owner=self.st,
            chronicle=self.chronicle,
            creation_status=4,  # At extras step
        )

    def test_extras_view_form_valid(self):
        """Test that extras view form submission works."""
        self.client.login(username="ST", password="password")
        url = reverse("characters:changeling:ctdhuman_extras", kwargs={"pk": self.ctdhuman.pk})
        data = {
            "date_of_birth": "1990-01-01",
            "apparent_age": "30",
            "age": "35",
            "description": "A test character",
            "history": "Test history",
            "goals": "Test goals",
            "notes": "Test notes",
            "public_info": "Public information",
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)
        self.ctdhuman.refresh_from_db()
        self.assertEqual(self.ctdhuman.creation_status, 5)

    def test_extras_view_form_has_date_widgets(self):
        """Test that extras view has date input widgets."""
        self.client.login(username="ST", password="password")
        url = reverse("characters:changeling:ctdhuman_extras", kwargs={"pk": self.ctdhuman.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Check that form has date_of_birth field
        self.assertIn("date_of_birth", response.context["form"].fields)


class TestCtDHumanCharacterCreationView(TestCase):
    """Tests for the CtDHumanCharacterCreationView."""

    def setUp(self):
        self.st = User.objects.create_user(username="ST", password="password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.chronicle.storytellers.add(self.st)
        changeling_setup()

    def test_creation_view_dispatches_to_correct_step(self):
        """Test that character creation dispatches to the correct step based on creation_status."""
        ctdhuman = CtDHuman.objects.create(
            name="Test CtDHuman",
            owner=self.st,
            chronicle=self.chronicle,
            creation_status=1,  # Attribute step
        )
        self.client.login(username="ST", password="password")
        url = reverse("characters:changeling:ctdhuman_creation", kwargs={"pk": ctdhuman.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_creation_view_shows_detail_on_completed(self):
        """Test that character creation shows detail view when complete."""
        ctdhuman = CtDHuman.objects.create(
            name="Test CtDHuman",
            owner=self.st,
            chronicle=self.chronicle,
            creation_status=100,  # Past all steps
            status="App",
        )
        self.client.login(username="ST", password="password")
        url = reverse("characters:changeling:ctdhuman_creation", kwargs={"pk": ctdhuman.pk})
        response = self.client.get(url)
        # When creation is complete, DictView renders the detail view directly
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "characters/changeling/ctdhuman/detail.html")


class TestCtDHumanTemplateSelectView(TestCase):
    """Tests for the CtDHumanTemplateSelectView."""

    def setUp(self):
        self.player = User.objects.create_user(username="User1", password="12345")
        changeling_setup()
        self.ctdhuman = CtDHuman.objects.create(
            name="Test CtDHuman",
            owner=self.player,
            creation_status=0,  # Before template selection
        )

    def test_template_select_view_requires_login(self):
        """Test that template select view requires login."""
        url = reverse("characters:changeling:ctdhuman_template", kwargs={"pk": self.ctdhuman.pk})
        response = self.client.get(url)
        # AuthErrorHandlerMiddleware converts login redirects to 401
        self.assertEqual(response.status_code, 401)

    def test_template_select_view_accessible(self):
        """Test that template select view is accessible for character owner."""
        self.client.login(username="User1", password="12345")
        url = reverse("characters:changeling:ctdhuman_template", kwargs={"pk": self.ctdhuman.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_template_select_view_redirects_if_creation_started(self):
        """Test that template select redirects if creation has started."""
        self.ctdhuman.creation_status = 1
        self.ctdhuman.save()
        self.client.login(username="User1", password="12345")
        url = reverse("characters:changeling:ctdhuman_template", kwargs={"pk": self.ctdhuman.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_template_select_no_template_choice(self):
        """Test submitting without selecting a template."""
        self.client.login(username="User1", password="12345")
        url = reverse("characters:changeling:ctdhuman_template", kwargs={"pk": self.ctdhuman.pk})
        response = self.client.post(url, data={})
        self.assertEqual(response.status_code, 302)
        self.ctdhuman.refresh_from_db()
        self.assertEqual(self.ctdhuman.creation_status, 1)
