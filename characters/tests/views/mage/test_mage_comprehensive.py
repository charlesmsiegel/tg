"""Comprehensive tests for mage views module - XP spending, rote creation, and creation workflow."""

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from characters.models.core.ability_block import Ability
from characters.models.core.archetype import Archetype
from characters.models.core.attribute_block import Attribute
from characters.models.core.human import Human
from characters.models.mage.faction import MageFaction
from characters.models.mage.focus import Tenet
from characters.models.mage.mage import Mage
from characters.models.mage.sphere import Sphere
from characters.tests.utils import mage_setup
from game.models import Chronicle, XPSpendingRequest


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
        strength = Attribute.objects.get(property_name="strength")

        response = self.client.post(
            reverse("characters:mage:spend_xp", kwargs={"pk": self.mage.pk}),
            {
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
            reverse("characters:mage:spend_xp", kwargs={"pk": self.mage.pk}),
            {
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
            reverse("characters:mage:spend_xp", kwargs={"pk": self.mage.pk}),
            {
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
            reverse("characters:mage:spend_xp", kwargs={"pk": self.mage.pk}),
            {
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
        self.st.is_staff = True
        self.st.save(update_fields=["is_staff"])
        self.client.force_login(self.st)
        self.mage.arete = 4  # Must be >= sphere ratings
        self.mage.forces = 4  # Needs specialty
        self.mage.save()

        response = self.client.post(
            reverse("characters:add_specialties", kwargs={"pk": self.mage.pk}),
            {"forces": "Fire"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.mage.specialties.filter(stat="forces", name="Fire").exists())

    def test_retire_character(self):
        """Test retiring a character from detail view."""
        self.client.login(username="owner", password="password")

        response = self.client.post(reverse("characters:retire", kwargs={"pk": self.mage.pk}))
        self.assertEqual(response.status_code, 302)
        self.mage.refresh_from_db()
        self.assertEqual(self.mage.status, "Ret")

    def test_decease_character(self):
        """An owner cannot mark an approved character deceased."""
        self.client.login(username="owner", password="password")

        response = self.client.post(reverse("characters:decease", kwargs={"pk": self.mage.pk}))
        self.assertEqual(response.status_code, 403)
        self.mage.refresh_from_db()
        self.assertEqual(self.mage.status, "App")


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


class TestMageXPSpendAction(TestCase):
    """The Mage spend endpoint (Step 5): audience, errors on the sheet, old URL."""

    def setUp(self):
        mage_setup()
        users = User.objects
        self.owner = users.create_user("spend_owner")
        self.player = users.create_user("spend_player")
        self.staff = users.create_user("spend_staff", is_staff=True)
        self.mage = Mage.objects.create(
            name="Spend Mage", owner=self.owner, status="App", arete=3, xp=50, willpower=5
        )
        self.url = reverse("characters:mage:spend_xp", kwargs={"pk": self.mage.pk})

    def willpower(self):
        return {"category": "Willpower", "example": "", "value": "", "note": "", "resonance": ""}

    def test_audience(self):
        for user, status in ((None, 401), (self.player, 404), (self.owner, 302)):
            with self.subTest(user=user):
                self.client.logout()
                if user is not None:
                    self.client.force_login(user)
                response = self.client.post(self.url, self.willpower())
                self.assertEqual(response.status_code, status)
        self.assertEqual(XPSpendingRequest.objects.filter(character=self.mage).count(), 1)

    def test_get_is_rejected(self):
        self.client.force_login(self.owner)
        self.assertEqual(self.client.get(self.url).status_code, 405)

    def test_non_mage_is_404(self):
        human = Human.objects.create(name="Plain", owner=self.owner, status="App", xp=50)
        self.client.force_login(self.owner)
        response = self.client.post(
            reverse("characters:mage:spend_xp", kwargs={"pk": human.pk}), self.willpower()
        )
        self.assertEqual(response.status_code, 404)

    def test_invalid_rote_rerenders_the_sheet_with_the_rote_form(self):
        self.client.force_login(self.owner)
        response = self.client.post(
            self.url, {"category": "Rote", "example": "", "value": "", "note": ""}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "characters/mage/mage/detail.html")
        self.assertTrue(response.context["rote_form"].errors)

    def test_old_spend_button_on_the_sheet_is_rejected(self):
        self.client.force_login(self.owner)
        response = self.client.post(
            self.mage.get_absolute_url(), {"spend_xp": "true", **self.willpower()}
        )
        self.assertEqual(response.status_code, 405)
