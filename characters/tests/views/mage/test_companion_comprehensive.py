"""Comprehensive tests for companion views module."""

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from characters.models.core.ability_block import Ability
from characters.models.core.archetype import Archetype
from characters.models.core.attribute_block import Attribute
from characters.models.core.background_block import Background, BackgroundRating
from characters.models.core.merit_flaw_block import MeritFlaw
from characters.models.mage.companion import Advantage, Companion
from characters.models.mage.mage import Mage
from characters.tests.utils import mage_setup
from game.models import Chronicle, ObjectType


class TestCompanionCreationWorkflow(TestCase):
    """Test the companion character creation workflow."""

    def setUp(self):
        mage_setup()
        self.client = Client()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.nature = Archetype.objects.first()
        self.demeanor = Archetype.objects.last()
        self.mage = Mage.objects.create(
            name="Master Mage",
            owner=self.owner,
            chronicle=self.chronicle,
            status="App",
        )

    def test_companion_basics_view_get(self):
        """Test GET request to companion basics view."""
        self.client.login(username="owner", password="password")
        response = self.client.get(reverse("characters:mage:create:companion"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "characters/mage/companion/basics.html")

    def test_companion_basics_view_post_familiar(self):
        """Test creating a familiar companion."""
        self.client.login(username="owner", password="password")
        response = self.client.post(
            reverse("characters:mage:create:companion"),
            {
                "name": "Test Familiar",
                "nature": self.nature.id,
                "demeanor": self.demeanor.id,
                "concept": "Magical Cat",
                "companion_type": "familiar",
                "chronicle": self.chronicle.id,
                "companion_of": self.mage.id,
                "npc": True,
            },
        )
        self.assertEqual(response.status_code, 302)
        companion = Companion.objects.filter(name="Test Familiar").first()
        self.assertIsNotNone(companion)
        self.assertEqual(companion.companion_type, "familiar")

    def test_companion_basics_view_post_consor(self):
        """Test creating a consor companion."""
        self.client.login(username="owner", password="password")
        response = self.client.post(
            reverse("characters:mage:create:companion"),
            {
                "name": "Test Consor",
                "nature": self.nature.id,
                "demeanor": self.demeanor.id,
                "concept": "Loyal Friend",
                "companion_type": "consor",
                "chronicle": self.chronicle.id,
                "companion_of": self.mage.id,
                "npc": False,
            },
        )
        self.assertEqual(response.status_code, 302)


class TestCompanionAttributeView(TestCase):
    """Test CompanionAttributeView."""

    def setUp(self):
        mage_setup()
        self.client = Client()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="password"
        )
        self.companion = Companion.objects.create(
            name="Test Companion",
            owner=self.owner,
            creation_status=1,
            companion_type="familiar",
        )

    def test_attribute_view_accessible(self):
        """Test that attribute view is accessible during creation."""
        self.client.login(username="owner", password="password")
        response = self.client.get(self.companion.get_absolute_url())
        self.assertEqual(response.status_code, 200)


class TestCompanionAbilityView(TestCase):
    """Test CompanionAbilityView."""

    def setUp(self):
        mage_setup()
        self.client = Client()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="password"
        )
        self.companion = Companion.objects.create(
            name="Test Companion",
            owner=self.owner,
            creation_status=2,
            companion_type="familiar",
        )

    def test_ability_view_accessible(self):
        """Test that ability view is accessible during creation."""
        self.client.login(username="owner", password="password")
        response = self.client.get(self.companion.get_absolute_url())
        self.assertEqual(response.status_code, 200)


class TestCompanionBackgroundsView(TestCase):
    """Test CompanionBackgroundsView."""

    def setUp(self):
        mage_setup()
        self.client = Client()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="password"
        )
        self.companion = Companion.objects.create(
            name="Test Companion",
            owner=self.owner,
            creation_status=3,
            companion_type="familiar",
        )

    def test_backgrounds_view_accessible(self):
        """Test that backgrounds view is accessible during creation."""
        self.client.login(username="owner", password="password")
        response = self.client.get(self.companion.get_absolute_url())
        self.assertEqual(response.status_code, 200)


class TestCompanionExtrasView(TestCase):
    """Test CompanionExtrasView."""

    def setUp(self):
        mage_setup()
        self.client = Client()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="password"
        )
        self.companion = Companion.objects.create(
            name="Test Companion",
            owner=self.owner,
            creation_status=4,
            companion_type="familiar",
        )

    def test_extras_view_accessible(self):
        """Test that extras view is accessible."""
        self.client.login(username="owner", password="password")
        response = self.client.get(self.companion.get_absolute_url())
        self.assertEqual(response.status_code, 200)


class TestCompanionFreebiesView(TestCase):
    """Test CompanionFreebiesView."""

    def setUp(self):
        mage_setup()
        self.client = Client()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="password"
        )
        self.companion = Companion.objects.create(
            name="Test Companion",
            owner=self.owner,
            creation_status=5,
            companion_type="familiar",
            freebies=25,
            willpower=5,
        )

    def test_freebies_view_accessible(self):
        """Test that freebies view is accessible."""
        self.client.login(username="owner", password="password")
        response = self.client.get(self.companion.get_absolute_url())
        self.assertEqual(response.status_code, 200)


class TestCompanionExamplesView(TestCase):
    """Test LoadExamplesView for companion freebie spending."""

    def setUp(self):
        mage_setup()
        self.client = Client()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="password"
        )
        self.companion = Companion.objects.create(
            name="Test Companion",
            owner=self.owner,
            companion_type="familiar",
            freebies=25,
            willpower=5,
        )

    def test_load_examples_attribute(self):
        """Test loading attribute examples."""
        self.client.login(username="owner", password="password")
        response = self.client.get(
            reverse("characters:mage:ajax:companion_load_examples"),
            {"category": "Attribute", "object": self.companion.id},
        )
        self.assertEqual(response.status_code, 200)

    def test_load_examples_ability(self):
        """Test loading ability examples."""
        self.client.login(username="owner", password="password")
        response = self.client.get(
            reverse("characters:mage:ajax:companion_load_examples"),
            {"category": "Ability", "object": self.companion.id},
        )
        self.assertEqual(response.status_code, 200)

    def test_load_examples_new_background(self):
        """Test loading new background examples."""
        self.client.login(username="owner", password="password")
        response = self.client.get(
            reverse("characters:mage:ajax:companion_load_examples"),
            {"category": "New Background", "object": self.companion.id},
        )
        self.assertEqual(response.status_code, 200)

    def test_load_examples_meritflaw(self):
        """Test loading merit/flaw examples."""
        self.client.login(username="owner", password="password")
        response = self.client.get(
            reverse("characters:mage:ajax:companion_load_examples"),
            {"category": "MeritFlaw", "object": self.companion.id},
        )
        self.assertEqual(response.status_code, 200)

    def test_load_examples_advantage(self):
        """Test loading advantage examples."""
        self.client.login(username="owner", password="password")
        # Create an advantage for testing
        advantage = Advantage.objects.create(name="Test Advantage", min_rating=1)
        response = self.client.get(
            reverse("characters:mage:ajax:companion_load_examples"),
            {"category": "Advantage", "object": self.companion.id},
        )
        self.assertEqual(response.status_code, 200)


class TestCompanionValuesView(TestCase):
    """Test LoadCompanionValuesView for advantage ratings."""

    def setUp(self):
        mage_setup()
        self.client = Client()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="password"
        )
        self.advantage = Advantage.objects.create(name="Test Advantage", min_rating=1)
        # Create ratings for the advantage
        from characters.models.mage.companion import AdvantageRating
        AdvantageRating.objects.create(advantage=self.advantage, value=1)
        AdvantageRating.objects.create(advantage=self.advantage, value=2)
        AdvantageRating.objects.create(advantage=self.advantage, value=3)

    def test_load_companion_values(self):
        """Test loading advantage rating values."""
        self.client.login(username="owner", password="password")
        response = self.client.get(
            reverse("characters:mage:ajax:load_companion_values"),
            {"example": self.advantage.id},
        )
        self.assertEqual(response.status_code, 200)


class TestCompanionLanguagesView(TestCase):
    """Test CompanionLanguagesView."""

    def setUp(self):
        mage_setup()
        self.client = Client()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="password"
        )
        # Add Language merit
        companion_type = ObjectType.objects.get_or_create(
            name="companion", type="char", gameline="mta"
        )[0]
        language_merit = MeritFlaw.objects.create(name="Language")
        language_merit.add_rating(1)
        language_merit.allowed_types.add(companion_type)

        self.companion = Companion.objects.create(
            name="Test Companion",
            owner=self.owner,
            creation_status=6,
            companion_type="familiar",
        )
        self.companion.merits_and_flaws.add(language_merit)

    def test_languages_view_accessible(self):
        """Test that languages view is accessible."""
        self.client.login(username="owner", password="password")
        response = self.client.get(self.companion.get_absolute_url())
        self.assertEqual(response.status_code, 200)


class TestCompanionSpecialtiesView(TestCase):
    """Test CompanionSpecialtiesView."""

    def setUp(self):
        mage_setup()
        self.client = Client()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="password"
        )
        self.companion = Companion.objects.create(
            name="Test Companion",
            owner=self.owner,
            creation_status=14,  # Specialties step
            companion_type="familiar",
        )
        # Set attribute to 4+ to require specialty
        self.companion.strength = 4
        self.companion.save()

    def test_specialties_view_accessible(self):
        """Test that specialties view is accessible."""
        self.client.login(username="owner", password="password")
        response = self.client.get(self.companion.get_absolute_url())
        self.assertEqual(response.status_code, 200)


class TestCompanionGenericBackgroundViews(TestCase):
    """Test generic background views for companions."""

    def setUp(self):
        mage_setup()
        self.client = Client()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="password"
        )
        self.companion = Companion.objects.create(
            name="Test Companion",
            owner=self.owner,
            creation_status=7,  # Node step
            companion_type="familiar",
        )
        # Add incomplete node background
        node_bg = Background.objects.get_or_create(
            property_name="node",
            defaults={"name": "Node"},
        )[0]
        BackgroundRating.objects.create(
            bg=node_bg,
            char=self.companion,
            rating=2,
            complete=False,
        )

    def test_node_view_accessible(self):
        """Test that node view is accessible when background exists."""
        self.client.login(username="owner", password="password")
        response = self.client.get(self.companion.get_absolute_url())
        self.assertEqual(response.status_code, 200)


class TestCompanionDetailViewWithOwnership(TestCase):
    """Test companion detail view with different ownership scenarios."""

    def setUp(self):
        mage_setup()
        self.client = Client()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="password"
        )
        self.other = User.objects.create_user(
            username="other", email="other@test.com", password="password"
        )
        self.st = User.objects.create_user(
            username="st", email="st@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.chronicle.storytellers.add(self.st)

        self.companion = Companion.objects.create(
            name="Test Companion",
            owner=self.owner,
            chronicle=self.chronicle,
            status="App",
            companion_type="familiar",
        )

    def test_owner_can_view_approved_companion(self):
        """Test that owner can view their approved companion."""
        self.client.login(username="owner", password="password")
        response = self.client.get(self.companion.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_st_can_view_companion(self):
        """Test that storyteller can view companion."""
        self.client.login(username="st", password="password")
        response = self.client.get(self.companion.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_other_user_cannot_view_companion(self):
        """Test that other users cannot view companion."""
        self.client.login(username="other", password="password")
        response = self.client.get(self.companion.get_absolute_url())
        self.assertEqual(response.status_code, 404)

    def test_unapproved_visible_to_owner(self):
        """Test that unapproved companion is visible to owner."""
        self.companion.status = "Un"
        self.companion.save()
        self.client.login(username="owner", password="password")
        response = self.client.get(self.companion.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_unapproved_hidden_from_others(self):
        """Test that unapproved companion is hidden from others."""
        self.companion.status = "Un"
        self.companion.save()
        self.client.login(username="other", password="password")
        response = self.client.get(self.companion.get_absolute_url())
        self.assertIn(response.status_code, [403, 404])
