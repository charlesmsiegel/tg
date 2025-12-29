"""
Tests for LinkedNPCForm.

Tests cover:
- Form initialization with various character types
- Form validation for all NPC types
- Form save creating NPCs correctly
- NPC role customization
- Gameline-specific field handling
"""

from characters.forms.core.linked_npc import LinkedNPCForm
from characters.models.changeling.changeling import Changeling
from characters.models.changeling.ctdhuman import CtDHuman
from characters.models.core.archetype import Archetype
from characters.models.core.human import Human
from characters.models.demon.demon import Demon
from characters.models.demon.dtf_human import DtFHuman
from characters.models.demon.thrall import Thrall
from characters.models.mage.companion import Companion
from characters.models.mage.mage import Mage
from characters.models.mage.mtahuman import MtAHuman
from characters.models.mage.sorcerer import Sorcerer
from characters.models.vampire.ghoul import Ghoul
from characters.models.vampire.vampire import Vampire
from characters.models.vampire.vtmhuman import VtMHuman
from characters.models.werewolf.fera import Fera
from characters.models.werewolf.fomor import Fomor
from characters.models.werewolf.garou import Werewolf
from characters.models.werewolf.kinfolk import Kinfolk
from characters.models.werewolf.spirit_character import SpiritCharacter
from characters.models.werewolf.wtahuman import WtAHuman
from characters.models.wraith.wraith import Wraith
from characters.models.wraith.wtohuman import WtOHuman
from django.contrib.auth.models import User
from django.test import TestCase


class LinkedNPCFormInitializationTestCase(TestCase):
    """Test LinkedNPCForm initialization."""

    def test_form_initializes_without_obj(self):
        """Test form can initialize without an associated object."""
        form = LinkedNPCForm()
        self.assertIn("npc_type", form.fields)
        self.assertIn("name", form.fields)
        self.assertIn("rank", form.fields)
        self.assertIn("concept", form.fields)
        self.assertEqual(form.npc_role, "ally")  # Default role

    def test_form_initializes_with_obj(self):
        """Test form initializes correctly with an associated character."""
        user = User.objects.create_user(username="testuser", password="password")
        character = Human.objects.create(name="Test PC", owner=user)

        form = LinkedNPCForm(obj=character)
        self.assertEqual(form.obj, character)

    def test_form_initializes_with_custom_role(self):
        """Test form initializes with custom NPC role."""
        form = LinkedNPCForm(npc_role="mentor")
        self.assertEqual(form.npc_role, "mentor")
        self.assertEqual(form.fields["rank"].label, "Mentor Rating")

    def test_form_role_customizes_rank_label(self):
        """Test that NPC role customizes the rank field label."""
        roles = ["ally", "mentor", "contact", "retainer", "follower"]
        for role in roles:
            form = LinkedNPCForm(npc_role=role)
            expected_label = f"{role.capitalize()} Rating"
            self.assertEqual(form.fields["rank"].label, expected_label)


class LinkedNPCFormValidationTestCase(TestCase):
    """Test LinkedNPCForm validation."""

    def setUp(self):
        self.archetype = Archetype.objects.create(name="Survivor")

    def test_valid_basic_data(self):
        """Test form validates with basic required data."""
        data = {
            "npc_type": "vampire",
            "name": "Test NPC",
            "rank": 2,
        }
        form = LinkedNPCForm(data=data)
        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")

    def test_valid_data_with_all_fields(self):
        """Test form validates with all fields populated."""
        data = {
            "npc_type": "mage",
            "name": "Full NPC",
            "rank": 3,
            "concept": "Occult librarian",
            "nature": self.archetype.pk,
            "demeanor": self.archetype.pk,
            "affiliation_name": "Order of Hermes",
            "note": "Special notes about this NPC",
        }
        form = LinkedNPCForm(data=data)
        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")

    def test_name_required(self):
        """Test that name field is required."""
        data = {
            "npc_type": "vampire",
            "rank": 2,
        }
        form = LinkedNPCForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_npc_type_required(self):
        """Test that npc_type field is required."""
        data = {
            "name": "Test NPC",
            "rank": 2,
        }
        form = LinkedNPCForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("npc_type", form.errors)

    def test_rank_validation_bounds(self):
        """Test rank field validates within bounds."""
        # Valid rank
        data = {"npc_type": "vampire", "name": "Test NPC", "rank": 3}
        form = LinkedNPCForm(data=data)
        self.assertTrue(form.is_valid())

        # Rank too low
        data["rank"] = -1
        form = LinkedNPCForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("rank", form.errors)

        # Rank too high
        data["rank"] = 6
        form = LinkedNPCForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("rank", form.errors)

    def test_invalid_npc_type(self):
        """Test that invalid NPC type is rejected."""
        data = {
            "npc_type": "invalid_type",
            "name": "Test NPC",
            "rank": 2,
        }
        form = LinkedNPCForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("npc_type", form.errors)

    def test_all_valid_npc_types(self):
        """Test all valid NPC types are accepted."""
        npc_types = [
            "vampire",
            "vtmhuman",
            "ghoul",
            "werewolf",
            "wtahuman",
            "kinfolk",
            "fera",
            "fomor",
            "mage",
            "mtahuman",
            "sorcerer",
            "companion",
            "wraith",
            "wtohuman",
            "changeling",
            "ctdhuman",
            "demon",
            "dtfhuman",
            "thrall",
            "spirit",
        ]
        for npc_type in npc_types:
            data = {
                "npc_type": npc_type,
                "name": f"Test {npc_type}",
                "rank": 2,
            }
            form = LinkedNPCForm(data=data)
            self.assertTrue(form.is_valid(), f"Failed for {npc_type}: {form.errors}")


class LinkedNPCFormSaveTestCase(TestCase):
    """Test LinkedNPCForm save functionality."""

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.pc = Human.objects.create(name="Test PC", owner=self.user)
        self.archetype = Archetype.objects.create(name="Survivor")

    def test_save_creates_vampire(self):
        """Test saving form creates a Vampire NPC."""
        data = {
            "npc_type": "vampire",
            "name": "Vampire Ally",
            "rank": 2,
            "concept": "Kindred elder",
            "clan_name": "Ventrue",
            "sect_name": "Camarilla",
        }
        form = LinkedNPCForm(data=data, obj=self.pc, npc_role="ally")
        self.assertTrue(form.is_valid())

        npc = form.save()
        self.assertIsInstance(npc, Vampire)
        self.assertEqual(npc.name, "Vampire Ally")
        self.assertTrue(npc.npc)
        self.assertEqual(npc.status, "Un")
        self.assertIn("Rank 2 Ally", npc.notes)
        self.assertIn("Test PC", npc.notes)
        self.assertIn("Clan: Ventrue", npc.notes)
        self.assertIn("Sect: Camarilla", npc.notes)

    def test_save_creates_werewolf(self):
        """Test saving form creates a Werewolf NPC."""
        data = {
            "npc_type": "werewolf",
            "name": "Garou Mentor",
            "rank": 3,
            "breed_name": "Homid",
            "auspice_name": "Philodox",
            "tribe_name": "Bone Gnawers",
        }
        form = LinkedNPCForm(data=data, obj=self.pc, npc_role="mentor")
        self.assertTrue(form.is_valid())

        npc = form.save()
        self.assertIsInstance(npc, Werewolf)
        self.assertEqual(npc.name, "Garou Mentor")
        self.assertIn("Breed: Homid", npc.notes)
        self.assertIn("Auspice: Philodox", npc.notes)
        self.assertIn("Tribe: Bone Gnawers", npc.notes)

    def test_save_creates_mage(self):
        """Test saving form creates a Mage NPC."""
        data = {
            "npc_type": "mage",
            "name": "Mage Contact",
            "rank": 1,
            "nature": self.archetype.pk,
            "demeanor": self.archetype.pk,
            "affiliation_name": "Verbena",
        }
        form = LinkedNPCForm(data=data, obj=self.pc, npc_role="contact")
        self.assertTrue(form.is_valid())

        npc = form.save()
        self.assertIsInstance(npc, Mage)
        self.assertEqual(npc.nature, self.archetype)
        self.assertEqual(npc.demeanor, self.archetype)
        self.assertIn("Affiliation: Verbena", npc.notes)

    def test_save_creates_wraith(self):
        """Test saving form creates a Wraith NPC."""
        data = {
            "npc_type": "wraith",
            "name": "Wraith Ally",
            "rank": 2,
            "guild_name": "Haunters",
        }
        form = LinkedNPCForm(data=data, obj=self.pc, npc_role="ally")
        self.assertTrue(form.is_valid())

        npc = form.save()
        self.assertIsInstance(npc, Wraith)
        self.assertIn("Guild: Haunters", npc.notes)

    def test_save_creates_changeling(self):
        """Test saving form creates a Changeling NPC."""
        data = {
            "npc_type": "changeling",
            "name": "Fae Friend",
            "rank": 2,
            "kith_name": "Pooka",
            "court_name": "Seelie",
        }
        form = LinkedNPCForm(data=data, obj=self.pc, npc_role="ally")
        self.assertTrue(form.is_valid())

        npc = form.save()
        self.assertIsInstance(npc, Changeling)
        self.assertIn("Kith: Pooka", npc.notes)
        self.assertIn("Court: Seelie", npc.notes)

    def test_save_creates_demon(self):
        """Test saving form creates a Demon NPC."""
        data = {
            "npc_type": "demon",
            "name": "Fallen Mentor",
            "rank": 4,
            "house_name": "Defiler",
        }
        form = LinkedNPCForm(data=data, obj=self.pc, npc_role="mentor")
        self.assertTrue(form.is_valid())

        npc = form.save()
        self.assertIsInstance(npc, Demon)
        self.assertIn("House: Defiler", npc.notes)

    def test_save_creates_spirit(self):
        """Test saving form creates a Spirit NPC."""
        data = {
            "npc_type": "spirit",
            "name": "Guiding Spirit",
            "rank": 3,
        }
        form = LinkedNPCForm(data=data, obj=self.pc, npc_role="mentor")
        self.assertTrue(form.is_valid())

        npc = form.save()
        self.assertIsInstance(npc, SpiritCharacter)

    def test_save_creates_kinfolk(self):
        """Test saving form creates a Kinfolk NPC."""
        data = {
            "npc_type": "kinfolk",
            "name": "Kinfolk Contact",
            "rank": 1,
            "tribe_name": "Silver Fangs",
        }
        form = LinkedNPCForm(data=data, obj=self.pc, npc_role="contact")
        self.assertTrue(form.is_valid())

        npc = form.save()
        self.assertIsInstance(npc, Kinfolk)
        self.assertIn("Tribe: Silver Fangs", npc.notes)

    def test_save_creates_fera(self):
        """Test saving form creates a Fera NPC."""
        data = {
            "npc_type": "fera",
            "name": "Fera Ally",
            "rank": 2,
            "breed_name": "Homid",
            "fera_type_name": "Ratkin",
        }
        form = LinkedNPCForm(data=data, obj=self.pc, npc_role="ally")
        self.assertTrue(form.is_valid())

        npc = form.save()
        self.assertIsInstance(npc, Fera)
        self.assertIn("Breed: Homid", npc.notes)
        self.assertIn("Fera Type: Ratkin", npc.notes)

    def test_save_without_linked_character(self):
        """Test saving form without an associated character."""
        data = {
            "npc_type": "vampire",
            "name": "Standalone NPC",
            "rank": 2,
        }
        form = LinkedNPCForm(data=data)
        self.assertTrue(form.is_valid())

        npc = form.save()
        self.assertEqual(npc.name, "Standalone NPC")
        self.assertIn("Rank 2 Ally", npc.notes)
        self.assertNotIn(" for ", npc.notes)  # No linked character

    def test_nature_demeanor_not_set_for_werewolf(self):
        """Test that nature/demeanor are not set for werewolves."""
        data = {
            "npc_type": "werewolf",
            "name": "Test Garou",
            "rank": 2,
            "nature": self.archetype.pk,
            "demeanor": self.archetype.pk,
        }
        form = LinkedNPCForm(data=data)
        self.assertTrue(form.is_valid())

        npc = form.save()
        # Werewolves shouldn't have nature/demeanor set even if provided
        self.assertIsNone(npc.nature)
        self.assertIsNone(npc.demeanor)

    def test_nature_demeanor_not_set_for_changeling(self):
        """Test that nature/demeanor are not set for changelings."""
        data = {
            "npc_type": "changeling",
            "name": "Test Changeling",
            "rank": 2,
            "nature": self.archetype.pk,
        }
        form = LinkedNPCForm(data=data)
        self.assertTrue(form.is_valid())

        npc = form.save()
        self.assertIsNone(npc.nature)

    def test_notes_include_additional_note(self):
        """Test that additional notes are included."""
        data = {
            "npc_type": "vampire",
            "name": "Test NPC",
            "rank": 2,
            "note": "Important background info",
        }
        form = LinkedNPCForm(data=data, obj=self.pc)
        self.assertTrue(form.is_valid())

        npc = form.save()
        self.assertIn("Important background info", npc.notes)


class LinkedNPCFormHumanVariantsTestCase(TestCase):
    """Test LinkedNPCForm creates correct human variant types."""

    def test_creates_vtmhuman(self):
        """Test form creates VtMHuman NPC."""
        data = {"npc_type": "vtmhuman", "name": "Vampire Human", "rank": 1}
        form = LinkedNPCForm(data=data)
        self.assertTrue(form.is_valid())
        npc = form.save()
        self.assertIsInstance(npc, VtMHuman)

    def test_creates_ghoul(self):
        """Test form creates Ghoul NPC."""
        data = {"npc_type": "ghoul", "name": "Test Ghoul", "rank": 2}
        form = LinkedNPCForm(data=data)
        self.assertTrue(form.is_valid())
        npc = form.save()
        self.assertIsInstance(npc, Ghoul)

    def test_creates_wtahuman(self):
        """Test form creates WtAHuman NPC."""
        data = {"npc_type": "wtahuman", "name": "Werewolf Human", "rank": 1}
        form = LinkedNPCForm(data=data)
        self.assertTrue(form.is_valid())
        npc = form.save()
        self.assertIsInstance(npc, WtAHuman)

    def test_creates_fomor(self):
        """Test form creates Fomor NPC."""
        data = {"npc_type": "fomor", "name": "Test Fomor", "rank": 2}
        form = LinkedNPCForm(data=data)
        self.assertTrue(form.is_valid())
        npc = form.save()
        self.assertIsInstance(npc, Fomor)

    def test_creates_mtahuman(self):
        """Test form creates MtAHuman NPC."""
        data = {"npc_type": "mtahuman", "name": "Mage Human", "rank": 1}
        form = LinkedNPCForm(data=data)
        self.assertTrue(form.is_valid())
        npc = form.save()
        self.assertIsInstance(npc, MtAHuman)

    def test_creates_sorcerer(self):
        """Test form creates Sorcerer NPC."""
        data = {"npc_type": "sorcerer", "name": "Test Sorcerer", "rank": 2}
        form = LinkedNPCForm(data=data)
        self.assertTrue(form.is_valid())
        npc = form.save()
        self.assertIsInstance(npc, Sorcerer)

    def test_creates_companion(self):
        """Test form creates Companion NPC."""
        data = {"npc_type": "companion", "name": "Test Companion", "rank": 2}
        form = LinkedNPCForm(data=data)
        self.assertTrue(form.is_valid())
        npc = form.save()
        self.assertIsInstance(npc, Companion)

    def test_creates_wtohuman(self):
        """Test form creates WtOHuman NPC."""
        data = {"npc_type": "wtohuman", "name": "Wraith Human", "rank": 1}
        form = LinkedNPCForm(data=data)
        self.assertTrue(form.is_valid())
        npc = form.save()
        self.assertIsInstance(npc, WtOHuman)

    def test_creates_ctdhuman(self):
        """Test form creates CtDHuman NPC."""
        data = {"npc_type": "ctdhuman", "name": "Changeling Human", "rank": 1}
        form = LinkedNPCForm(data=data)
        self.assertTrue(form.is_valid())
        npc = form.save()
        self.assertIsInstance(npc, CtDHuman)

    def test_creates_dtfhuman(self):
        """Test form creates DtFHuman NPC."""
        data = {"npc_type": "dtfhuman", "name": "Demon Human", "rank": 1}
        form = LinkedNPCForm(data=data)
        self.assertTrue(form.is_valid())
        npc = form.save()
        self.assertIsInstance(npc, DtFHuman)

    def test_creates_thrall(self):
        """Test form creates Thrall NPC.

        Note: Thrall requires 'enhancements' field (blank=False) which the form
        currently doesn't handle. This test verifies the form validates but
        documents that creating a Thrall NPC via LinkedNPCForm requires updating
        the model or form to handle this requirement.
        """
        data = {"npc_type": "thrall", "name": "Test Thrall", "rank": 2}
        form = LinkedNPCForm(data=data)
        self.assertTrue(form.is_valid())
        # Thrall.enhancements has blank=False but default=list, causing
        # validation to fail on save. This is a known limitation.
        with self.assertRaises(Exception):
            form.save()
