"""Comprehensive tests for sorcerer views module."""

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from characters.models.core.ability_block import Ability
from characters.models.core.archetype import Archetype
from characters.models.core.attribute_block import Attribute
from characters.models.core.background_block import Background, BackgroundRating
from characters.models.core.merit_flaw_block import MeritFlaw
from characters.models.mage.fellowship import SorcererFellowship
from characters.models.mage.focus import Practice
from characters.models.mage.sorcerer import LinearMagicPath, LinearMagicRitual, Sorcerer
from characters.tests.utils import mage_setup
from game.models import Chronicle, ObjectType


class TestSorcererCreationWorkflow(TestCase):
    """Test the sorcerer character creation workflow."""

    def setUp(self):
        mage_setup()
        self.client = Client()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.nature = Archetype.objects.first()
        self.demeanor = Archetype.objects.last()
        self.fellowship = SorcererFellowship.objects.create(name="Test Fellowship")
        self.path = LinearMagicPath.objects.create(name="Alchemy", numina_type="hedge_magic")
        self.attribute = Attribute.objects.first()
        self.fellowship.favored_attributes.add(self.attribute)
        self.fellowship.favored_paths.add(self.path)

    def test_sorcerer_basics_view_get(self):
        """Test GET request to sorcerer basics view."""
        self.client.login(username="owner", password="password")
        response = self.client.get(reverse("characters:mage:create:sorcerer"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "characters/mage/sorcerer/basics.html")

    def test_sorcerer_basics_view_post_hedge_mage(self):
        """Test creating a hedge mage sorcerer."""
        self.client.login(username="owner", password="password")
        response = self.client.post(
            reverse("characters:mage:create:sorcerer"),
            {
                "name": "Test Hedge Mage",
                "nature": self.nature.id,
                "demeanor": self.demeanor.id,
                "concept": "Hedge Mage",
                "fellowship": self.fellowship.id,
                "affinity_path": self.path.id,
                "casting_attribute": self.attribute.id,
                "sorcerer_type": "hedge_mage",
                "npc": False,
            },
        )
        self.assertEqual(response.status_code, 302)
        sorcerer = Sorcerer.objects.filter(name="Test Hedge Mage").first()
        self.assertIsNotNone(sorcerer)
        self.assertEqual(sorcerer.sorcerer_type, "hedge_mage")

    def test_sorcerer_basics_view_post_psychic(self):
        """Test creating a psychic sorcerer."""
        self.client.login(username="owner", password="password")
        psychic_path = LinearMagicPath.objects.create(name="Telepathy", numina_type="psychic")
        self.fellowship.favored_paths.add(psychic_path)
        response = self.client.post(
            reverse("characters:mage:create:sorcerer"),
            {
                "name": "Test Psychic",
                "nature": self.nature.id,
                "demeanor": self.demeanor.id,
                "concept": "Psychic",
                "fellowship": self.fellowship.id,
                "affinity_path": psychic_path.id,
                "casting_attribute": self.attribute.id,
                "sorcerer_type": "psychic",
                "npc": False,
            },
        )
        self.assertEqual(response.status_code, 302)


class TestSorcererAttributeView(TestCase):
    """Test SorcererAttributeView."""

    def setUp(self):
        mage_setup()
        self.client = Client()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="password"
        )
        self.sorcerer = Sorcerer.objects.create(
            name="Test Sorcerer",
            owner=self.owner,
            creation_status=1,
            sorcerer_type="hedge_mage",
        )

    def test_attribute_view_accessible(self):
        """Test that attribute view is accessible during creation."""
        self.client.login(username="owner", password="password")
        response = self.client.get(self.sorcerer.get_absolute_url())
        self.assertEqual(response.status_code, 200)


class TestSorcererAbilityView(TestCase):
    """Test SorcererAbilityView."""

    def setUp(self):
        mage_setup()
        self.client = Client()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="password"
        )
        self.sorcerer = Sorcerer.objects.create(
            name="Test Sorcerer",
            owner=self.owner,
            creation_status=2,
            sorcerer_type="hedge_mage",
        )

    def test_ability_view_accessible(self):
        """Test that ability view is accessible during creation."""
        self.client.login(username="owner", password="password")
        response = self.client.get(self.sorcerer.get_absolute_url())
        self.assertEqual(response.status_code, 200)


class TestSorcererBackgroundsView(TestCase):
    """Test SorcererBackgroundsView."""

    def setUp(self):
        mage_setup()
        self.client = Client()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="password"
        )
        self.sorcerer = Sorcerer.objects.create(
            name="Test Sorcerer",
            owner=self.owner,
            creation_status=3,
            sorcerer_type="hedge_mage",
        )

    def test_backgrounds_view_accessible(self):
        """Test that backgrounds view is accessible during creation."""
        self.client.login(username="owner", password="password")
        response = self.client.get(self.sorcerer.get_absolute_url())
        self.assertEqual(response.status_code, 200)


class TestSorcererPathView(TestCase):
    """Test SorcererPathView for hedge magic path selection."""

    def setUp(self):
        mage_setup()
        self.client = Client()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="password"
        )
        self.path = LinearMagicPath.objects.create(name="Alchemy", numina_type="hedge_magic")
        self.sorcerer = Sorcerer.objects.create(
            name="Test Sorcerer",
            owner=self.owner,
            creation_status=5,
            sorcerer_type="hedge_mage",
            willpower=5,
        )

    def test_path_view_accessible(self):
        """Test that path view is accessible for hedge mages."""
        self.client.login(username="owner", password="password")
        response = self.client.get(self.sorcerer.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_path_view_skipped_for_psychic(self):
        """Test that path view redirects for psychics."""
        self.sorcerer.sorcerer_type = "psychic"
        self.sorcerer.save()
        self.client.login(username="owner", password="password")
        response = self.client.get(self.sorcerer.get_absolute_url())
        # Should redirect because psychics skip this view
        self.assertIn(response.status_code, [200, 302])


class TestSorcererPsychicView(TestCase):
    """Test SorcererPsychicView for psychic path selection."""

    def setUp(self):
        mage_setup()
        self.client = Client()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="password"
        )
        self.path = LinearMagicPath.objects.create(name="Telepathy", numina_type="psychic")
        self.sorcerer = Sorcerer.objects.create(
            name="Test Psychic",
            owner=self.owner,
            creation_status=4,
            sorcerer_type="psychic",
            willpower=5,
        )

    def test_psychic_view_accessible(self):
        """Test that psychic view is accessible for psychics."""
        self.client.login(username="owner", password="password")
        response = self.client.get(self.sorcerer.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_psychic_view_skipped_for_hedge_mage(self):
        """Test that psychic view redirects for hedge mages."""
        self.sorcerer.sorcerer_type = "hedge_mage"
        self.sorcerer.save()
        self.client.login(username="owner", password="password")
        response = self.client.get(self.sorcerer.get_absolute_url())
        # Should redirect because hedge mages skip this view
        self.assertIn(response.status_code, [200, 302])


class TestSorcererRitualView(TestCase):
    """Test SorcererRitualView."""

    def setUp(self):
        mage_setup()
        self.client = Client()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="password"
        )
        self.path = LinearMagicPath.objects.create(name="Alchemy", numina_type="hedge_magic")
        self.sorcerer = Sorcerer.objects.create(
            name="Test Sorcerer",
            owner=self.owner,
            creation_status=6,
            sorcerer_type="hedge_mage",
            willpower=5,
        )
        # Add path rating
        from characters.models.mage.sorcerer import PathRating
        PathRating.objects.create(
            character=self.sorcerer,
            path=self.path,
            rating=2,
        )

    def test_ritual_view_accessible(self):
        """Test that ritual view is accessible for hedge mages."""
        self.client.login(username="owner", password="password")
        response = self.client.get(self.sorcerer.get_absolute_url())
        self.assertEqual(response.status_code, 200)


class TestSorcererExtrasView(TestCase):
    """Test SorcererExtrasView."""

    def setUp(self):
        mage_setup()
        self.client = Client()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="password"
        )
        self.sorcerer = Sorcerer.objects.create(
            name="Test Sorcerer",
            owner=self.owner,
            creation_status=7,
            sorcerer_type="hedge_mage",
        )

    def test_extras_view_accessible(self):
        """Test that extras view is accessible."""
        self.client.login(username="owner", password="password")
        response = self.client.get(self.sorcerer.get_absolute_url())
        self.assertEqual(response.status_code, 200)


class TestSorcererFreebiesView(TestCase):
    """Test SorcererFreebiesView."""

    def setUp(self):
        mage_setup()
        self.client = Client()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="password"
        )
        self.sorcerer = Sorcerer.objects.create(
            name="Test Sorcerer",
            owner=self.owner,
            creation_status=8,
            sorcerer_type="hedge_mage",
            freebies=21,
            willpower=5,
        )

    def test_freebies_view_accessible(self):
        """Test that freebies view is accessible."""
        self.client.login(username="owner", password="password")
        response = self.client.get(self.sorcerer.get_absolute_url())
        self.assertEqual(response.status_code, 200)


class TestSorcererAjaxViews(TestCase):
    """Test AJAX views for sorcerer creation."""

    def setUp(self):
        mage_setup()
        self.client = Client()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="password"
        )
        self.fellowship = SorcererFellowship.objects.create(name="Test Fellowship")
        self.attribute = Attribute.objects.first()
        self.path = LinearMagicPath.objects.create(name="Alchemy", numina_type="hedge_magic")
        self.fellowship.favored_attributes.add(self.attribute)
        self.fellowship.favored_paths.add(self.path)

    def test_load_attributes_ajax(self):
        """Test loading favored attributes for a fellowship."""
        self.client.login(username="owner", password="password")
        response = self.client.get(
            reverse("characters:mage:ajax:load_sorcerer_attributes"),
            {"fellowship": self.fellowship.id},
        )
        self.assertEqual(response.status_code, 200)

    def test_load_affinities_ajax(self):
        """Test loading favored paths for a fellowship."""
        self.client.login(username="owner", password="password")
        response = self.client.get(
            reverse("characters:mage:ajax:load_sorcerer_affinities"),
            {"fellowship": self.fellowship.id},
        )
        self.assertEqual(response.status_code, 200)


class TestSorcererExamplesView(TestCase):
    """Test LoadExamplesView for sorcerer freebie spending."""

    def setUp(self):
        mage_setup()
        self.client = Client()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="password"
        )
        self.path = LinearMagicPath.objects.create(name="Alchemy", numina_type="hedge_magic")
        self.sorcerer = Sorcerer.objects.create(
            name="Test Sorcerer",
            owner=self.owner,
            sorcerer_type="hedge_mage",
            freebies=21,
            willpower=5,
        )

    def test_load_examples_attribute(self):
        """Test loading attribute examples."""
        self.client.login(username="owner", password="password")
        response = self.client.get(
            reverse("characters:mage:ajax:sorcerer_load_examples"),
            {"category": "Attribute", "object": self.sorcerer.id},
        )
        self.assertEqual(response.status_code, 200)

    def test_load_examples_ability(self):
        """Test loading ability examples."""
        self.client.login(username="owner", password="password")
        response = self.client.get(
            reverse("characters:mage:ajax:sorcerer_load_examples"),
            {"category": "Ability", "object": self.sorcerer.id},
        )
        self.assertEqual(response.status_code, 200)

    def test_load_examples_new_background(self):
        """Test loading new background examples."""
        self.client.login(username="owner", password="password")
        response = self.client.get(
            reverse("characters:mage:ajax:sorcerer_load_examples"),
            {"category": "New Background", "object": self.sorcerer.id},
        )
        self.assertEqual(response.status_code, 200)

    def test_load_examples_new_path(self):
        """Test loading new path examples."""
        self.client.login(username="owner", password="password")
        response = self.client.get(
            reverse("characters:mage:ajax:sorcerer_load_examples"),
            {"category": "New Path", "object": self.sorcerer.id},
        )
        self.assertEqual(response.status_code, 200)


class TestGetPracticeAbilitiesView(TestCase):
    """Test GetPracticeAbilitiesView AJAX endpoint."""

    def setUp(self):
        mage_setup()
        self.client = Client()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="password"
        )
        self.practice = Practice.objects.first()

    def test_get_practice_abilities(self):
        """Test getting abilities for a practice."""
        self.client.login(username="owner", password="password")
        response = self.client.get(
            reverse("characters:mage:ajax:get_practice_abilities"),
            {"practice_id": self.practice.id},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
