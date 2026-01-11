"""Comprehensive tests for mage views module - XP spending, rote creation, and creation workflow."""

import unittest

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from characters.models.core.ability_block import Ability
from characters.models.core.archetype import Archetype
from characters.models.core.attribute_block import Attribute
from characters.models.core.merit_flaw_block import MeritFlaw
from characters.models.mage.faction import MageFaction
from characters.models.mage.focus import Practice, Tenet
from characters.models.mage.mage import Mage
from characters.models.mage.sphere import Sphere
from characters.tests.utils import mage_setup
from game.models import Chronicle


class TestMageDetailViewPost(TestCase):
    """Test MageDetailView POST functionality for XP spending."""

    def setUp(self):
        mage_setup()
        self.client = Client()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="password"
        )
        self.st = User.objects.create_user(username="st", email="st@test.com", password="password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.chronicle.storytellers.add(self.st)

        # Set up tenets for mage
        self.met_tenet = Tenet.objects.filter(tenet_type="met").first()
        self.per_tenet = Tenet.objects.filter(tenet_type="per").first()
        self.asc_tenet = Tenet.objects.filter(tenet_type="asc").first()

        self.mage = Mage.objects.create(
            name="Test Mage",
            owner=self.owner,
            chronicle=self.chronicle,
            status="App",
            arete=3,
            xp=50,
            willpower=5,
            metaphysical_tenet=self.met_tenet,
            personal_tenet=self.per_tenet,
            ascension_tenet=self.asc_tenet,
        )
        # Set some initial sphere values
        self.mage.forces = 2
        self.mage.prime = 1
        self.mage.save()

    def test_spend_xp_on_attribute(self):
        """Test spending XP to increase an attribute."""
        self.client.login(username="owner", password="password")
        initial_xp = self.mage.xp
        strength = Attribute.objects.get(property_name="strength")

        response = self.client.post(
            self.mage.get_absolute_url(),
            {
                "spend_xp": "true",
                "category": "Attribute",
                "example": strength.id,
                "value": "",
                "note": "",
                "pooled": False,
                "resonance": "",
            },
        )
        # Should redirect after successful submission
        self.assertEqual(response.status_code, 302)

    def test_spend_xp_on_ability(self):
        """Test spending XP to increase an ability."""
        self.client.login(username="owner", password="password")
        # Set initial ability value
        self.mage.occult = 2
        self.mage.save()
        occult = Ability.objects.get(property_name="occult")

        response = self.client.post(
            self.mage.get_absolute_url(),
            {
                "spend_xp": "true",
                "category": "Ability",
                "example": occult.id,
                "value": "",
                "note": "",
                "pooled": False,
                "resonance": "",
            },
        )
        self.assertEqual(response.status_code, 302)

    def test_spend_xp_on_willpower(self):
        """Test spending XP to increase willpower."""
        self.client.login(username="owner", password="password")

        response = self.client.post(
            self.mage.get_absolute_url(),
            {
                "spend_xp": "true",
                "category": "Willpower",
                "example": "",
                "value": "",
                "note": "",
                "pooled": False,
                "resonance": "",
            },
        )
        self.assertEqual(response.status_code, 302)

    def test_spend_xp_on_sphere(self):
        """Test spending XP to increase a sphere."""
        self.client.login(username="owner", password="password")
        forces = Sphere.objects.get(property_name="forces")

        response = self.client.post(
            self.mage.get_absolute_url(),
            {
                "spend_xp": "true",
                "category": "Sphere",
                "example": forces.id,
                "value": "",
                "note": "",
                "pooled": False,
                "resonance": "",
            },
        )
        self.assertEqual(response.status_code, 302)

    def test_specialties_submission(self):
        """Test submitting specialties from detail view."""
        self.client.login(username="owner", password="password")
        self.mage.arete = 4  # Must be >= sphere ratings
        self.mage.forces = 4  # Needs specialty
        self.mage.save()

        response = self.client.post(
            self.mage.get_absolute_url(),
            {
                "specialties": "true",
                "forces": "Fire",
            },
        )
        self.assertEqual(response.status_code, 302)

    def test_retire_character(self):
        """Test retiring a character from detail view."""
        self.client.login(username="owner", password="password")

        response = self.client.post(
            self.mage.get_absolute_url(),
            {"retire": "true"},
        )
        self.assertEqual(response.status_code, 302)
        self.mage.refresh_from_db()
        self.assertEqual(self.mage.status, "Ret")

    def test_decease_character(self):
        """Test marking a character as deceased from detail view."""
        self.client.login(username="owner", password="password")

        response = self.client.post(
            self.mage.get_absolute_url(),
            {"decease": "true"},
        )
        self.assertEqual(response.status_code, 302)
        self.mage.refresh_from_db()
        self.assertEqual(self.mage.status, "Dec")


class TestMageAjaxViews(TestCase):
    """Test AJAX views for mage character creation."""

    def setUp(self):
        mage_setup()
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )

    def test_load_mf_ratings_ajax(self):
        """Test loading merit/flaw ratings via AJAX."""
        self.client.login(username="testuser", password="password")
        mf = MeritFlaw.objects.filter(ratings__isnull=False).first()
        if mf:
            response = self.client.get(
                reverse("characters:mage:ajax:load_mf_ratings"),
                {"mf": mf.id},
            )
            self.assertEqual(response.status_code, 200)


@unittest.skip("URL 'load_freebie_examples' not implemented yet")
class TestMageFreebieFormPopulationView(TestCase):
    """Test the freebie form population AJAX view."""

    def setUp(self):
        mage_setup()
        self.client = Client()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="password"
        )
        self.met_tenet = Tenet.objects.filter(tenet_type="met").first()
        self.per_tenet = Tenet.objects.filter(tenet_type="per").first()
        self.asc_tenet = Tenet.objects.filter(tenet_type="asc").first()

        self.mage = Mage.objects.create(
            name="Test Mage",
            owner=self.owner,
            arete=2,
            metaphysical_tenet=self.met_tenet,
            personal_tenet=self.per_tenet,
            ascension_tenet=self.asc_tenet,
        )

    def test_load_freebie_examples_attribute(self):
        """Test loading attribute examples for freebie spending."""
        self.client.login(username="owner", password="password")
        response = self.client.get(
            reverse("characters:mage:ajax:load_freebie_examples"),
            {"category": "Attribute", "object": self.mage.id},
        )
        self.assertEqual(response.status_code, 200)

    def test_load_freebie_examples_ability(self):
        """Test loading ability examples for freebie spending."""
        self.client.login(username="owner", password="password")
        response = self.client.get(
            reverse("characters:mage:ajax:load_freebie_examples"),
            {"category": "Ability", "object": self.mage.id},
        )
        self.assertEqual(response.status_code, 200)

    def test_load_freebie_examples_sphere(self):
        """Test loading sphere examples for freebie spending."""
        self.client.login(username="owner", password="password")
        response = self.client.get(
            reverse("characters:mage:ajax:load_freebie_examples"),
            {"category": "Sphere", "object": self.mage.id},
        )
        self.assertEqual(response.status_code, 200)

    def test_load_freebie_examples_resonance(self):
        """Test loading resonance examples for freebie spending."""
        self.client.login(username="owner", password="password")
        response = self.client.get(
            reverse("characters:mage:ajax:load_freebie_examples"),
            {"category": "Resonance", "object": self.mage.id},
        )
        self.assertEqual(response.status_code, 200)


class TestMageXPExamplesView(TestCase):
    """Test loading XP spending examples."""

    def setUp(self):
        mage_setup()
        self.client = Client()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="password"
        )
        self.met_tenet = Tenet.objects.filter(tenet_type="met").first()
        self.per_tenet = Tenet.objects.filter(tenet_type="per").first()
        self.asc_tenet = Tenet.objects.filter(tenet_type="asc").first()

        self.mage = Mage.objects.create(
            name="Test Mage",
            owner=self.owner,
            arete=3,
            xp=50,
            metaphysical_tenet=self.met_tenet,
            personal_tenet=self.per_tenet,
            ascension_tenet=self.asc_tenet,
        )
        self.mage.forces = 2
        self.mage.prime = 1
        self.mage.occult = 3
        self.mage.save()

    def test_load_xp_examples_attribute(self):
        """Test loading attribute XP examples."""
        self.client.login(username="owner", password="password")
        response = self.client.get(
            reverse("characters:mage:ajax:load_xp_examples"),
            {"category": "Attribute", "object": self.mage.id},
        )
        self.assertEqual(response.status_code, 200)

    def test_load_xp_examples_ability(self):
        """Test loading ability XP examples."""
        self.client.login(username="owner", password="password")
        response = self.client.get(
            reverse("characters:mage:ajax:load_xp_examples"),
            {"category": "Ability", "object": self.mage.id},
        )
        self.assertEqual(response.status_code, 200)

    def test_load_xp_examples_sphere(self):
        """Test loading sphere XP examples."""
        self.client.login(username="owner", password="password")
        response = self.client.get(
            reverse("characters:mage:ajax:load_xp_examples"),
            {"category": "Sphere", "object": self.mage.id},
        )
        self.assertEqual(response.status_code, 200)

    def test_load_xp_examples_new_background(self):
        """Test loading new background XP examples."""
        self.client.login(username="owner", password="password")
        response = self.client.get(
            reverse("characters:mage:ajax:load_xp_examples"),
            {"category": "New Background", "object": self.mage.id},
        )
        self.assertEqual(response.status_code, 200)

    def test_load_xp_examples_tenet(self):
        """Test loading tenet XP examples."""
        self.client.login(username="owner", password="password")
        response = self.client.get(
            reverse("characters:mage:ajax:load_xp_examples"),
            {"category": "Tenet", "object": self.mage.id},
        )
        self.assertEqual(response.status_code, 200)

    def test_load_xp_examples_practice(self):
        """Test loading practice XP examples."""
        self.client.login(username="owner", password="password")
        # Set up practice prerequisites
        self.mage.occult = 4
        self.mage.save()
        response = self.client.get(
            reverse("characters:mage:ajax:load_xp_examples"),
            {"category": "Practice", "object": self.mage.id},
        )
        self.assertEqual(response.status_code, 200)


class TestMageCharacterCreationWorkflow(TestCase):
    """Test the complete mage character creation workflow."""

    def setUp(self):
        mage_setup()
        self.client = Client()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")

        # Create required objects
        self.nature = Archetype.objects.first()
        self.demeanor = Archetype.objects.last()
        self.affiliation = MageFaction.objects.filter(parent=None).first()
        self.faction = MageFaction.objects.filter(parent=self.affiliation).first()

    def test_creation_workflow_step_by_step(self):
        """Test progressing through creation steps."""
        self.client.login(username="owner", password="password")

        # Step 1: Create basics
        response = self.client.post(
            reverse("characters:mage:create:mage"),
            {
                "name": "Test Mage",
                "nature": self.nature.id,
                "demeanor": self.demeanor.id,
                "concept": "Test Concept",
                "affiliation": self.affiliation.id,
                "faction": self.faction.id,
                "essence": "Dynamic",
            },
        )
        self.assertEqual(response.status_code, 302)
        mage = Mage.objects.filter(name="Test Mage").first()
        self.assertIsNotNone(mage)
        self.assertEqual(mage.creation_status, 1)

    def test_mage_attribute_view_accessible(self):
        """Test that attribute view is accessible during creation."""
        self.client.login(username="owner", password="password")
        mage = Mage.objects.create(
            name="Test Mage",
            owner=self.owner,
            creation_status=1,
        )
        response = self.client.get(reverse("characters:mage:update:mage", kwargs={"pk": mage.pk}))
        self.assertEqual(response.status_code, 200)

    def test_mage_ability_view_accessible(self):
        """Test that ability view is accessible during creation."""
        self.client.login(username="owner", password="password")
        mage = Mage.objects.create(
            name="Test Mage",
            owner=self.owner,
            creation_status=2,
        )
        response = self.client.get(reverse("characters:mage:update:mage", kwargs={"pk": mage.pk}))
        self.assertEqual(response.status_code, 200)

    def test_mage_backgrounds_view_accessible(self):
        """Test that backgrounds view is accessible during creation."""
        self.client.login(username="owner", password="password")
        mage = Mage.objects.create(
            name="Test Mage",
            owner=self.owner,
            creation_status=3,
        )
        response = self.client.get(reverse("characters:mage:update:mage", kwargs={"pk": mage.pk}))
        self.assertEqual(response.status_code, 200)


class TestMageFocusView(TestCase):
    """Test MageFocusView for tenet and practice selection."""

    def setUp(self):
        mage_setup()
        self.client = Client()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="password"
        )
        self.mage = Mage.objects.create(
            name="Test Mage",
            owner=self.owner,
            creation_status=5,
            arete=2,
        )
        # Set up abilities for practice requirements
        self.mage.occult = 4
        self.mage.save()

    def test_focus_view_accessible(self):
        """Test that focus view is accessible."""
        self.client.login(username="owner", password="password")
        response = self.client.get(
            reverse("characters:mage:update:mage", kwargs={"pk": self.mage.pk})
        )
        self.assertEqual(response.status_code, 200)


class TestMageExtrasView(TestCase):
    """Test MageExtrasView for description and history."""

    def setUp(self):
        mage_setup()
        self.client = Client()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="password"
        )
        self.mage = Mage.objects.create(
            name="Test Mage",
            owner=self.owner,
            creation_status=6,
            arete=1,
        )

    def test_extras_view_accessible(self):
        """Test that extras view is accessible."""
        self.client.login(username="owner", password="password")
        response = self.client.get(
            reverse("characters:mage:update:mage", kwargs={"pk": self.mage.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_extras_view_post(self):
        """Test posting to extras view."""
        self.client.login(username="owner", password="password")
        response = self.client.post(
            reverse("characters:mage:update:mage", kwargs={"pk": self.mage.pk}),
            {
                "date_of_birth": "1990-01-01",
                "apparent_age": 30,
                "age_of_awakening": 20,
                "age": 30,
                "description": "A test mage",
                "history": "Born to test",
                "avatar_description": "A glowing orb",
                "goals": "To pass tests",
                "notes": "Notes here",
                "public_info": "Public info",
            },
        )
        self.assertEqual(response.status_code, 302)


class TestGetAbilitiesView(TestCase):
    """Test the GetAbilitiesView AJAX endpoint."""

    def setUp(self):
        mage_setup()
        self.client = Client()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="password"
        )
        self.mage = Mage.objects.create(
            name="Test Mage",
            owner=self.owner,
            arete=2,
        )
        self.mage.occult = 3
        self.mage.save()
        self.practice = Practice.objects.first()

    def test_get_abilities_returns_json(self):
        """Test that get_abilities returns JSON data."""
        self.client.login(username="owner", password="password")
        response = self.client.get(
            reverse("characters:mage:ajax:get_abilities"),
            {"object": self.mage.id, "practice_id": self.practice.id},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
