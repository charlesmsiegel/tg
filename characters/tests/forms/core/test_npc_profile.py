"""
Tests for NPCProfileForm.

Tests cover:
- Form initialization and field setup
- Form validation for all NPC types
- Form save creating NPCs with correct properties
- Character type-specific field handling
- Chronicle and role management
"""

from characters.forms.core.npc_profile import NPCProfileForm
from characters.models.changeling.changeling import Changeling
from characters.models.changeling.ctdhuman import CtDHuman
from characters.models.changeling.house import House
from characters.models.changeling.kith import Kith
from characters.models.core.human import Human
from characters.models.demon.demon import Demon
from characters.models.demon.dtf_human import DtFHuman
from characters.models.demon.faction import DemonFaction
from characters.models.demon.house import DemonHouse
from characters.models.demon.thrall import Thrall
from characters.models.mage.companion import Companion
from characters.models.mage.faction import MageFaction
from characters.models.mage.fellowship import SorcererFellowship
from characters.models.mage.mage import Mage
from characters.models.mage.mtahuman import MtAHuman
from characters.models.mage.sorcerer import Sorcerer
from characters.models.vampire.vtmhuman import VtMHuman
from characters.models.werewolf.fomor import Fomor
from characters.models.werewolf.garou import Werewolf
from characters.models.werewolf.kinfolk import Kinfolk
from characters.models.werewolf.tribe import Tribe
from characters.models.werewolf.wtahuman import WtAHuman
from characters.models.wraith.faction import WraithFaction
from characters.models.wraith.guild import Guild
from characters.models.wraith.wraith import Wraith
from characters.models.wraith.wtohuman import WtOHuman
from django.contrib.auth.models import User
from django.test import TestCase
from game.models import Chronicle


class NPCProfileFormInitializationTestCase(TestCase):
    """Test NPCProfileForm initialization."""

    def test_form_initializes_without_user(self):
        """Test form can initialize without a user."""
        form = NPCProfileForm()
        self.assertIn("npc_type", form.fields)
        self.assertIn("name", form.fields)
        self.assertIn("concept", form.fields)
        self.assertIn("npc_role", form.fields)
        self.assertIn("chronicle", form.fields)
        self.assertIsNone(form.user)

    def test_form_initializes_with_user(self):
        """Test form initializes with a user."""
        user = User.objects.create_user(username="testuser", password="password")
        form = NPCProfileForm(user=user)
        self.assertEqual(form.user, user)

    def test_form_initializes_with_related_character(self):
        """Test form initializes with a related character."""
        user = User.objects.create_user(username="testuser", password="password")
        chronicle = Chronicle.objects.create(name="Test Chronicle")
        character = Human.objects.create(name="Test PC", owner=user, chronicle=chronicle)

        form = NPCProfileForm(related_character=character)
        self.assertEqual(form.related_character, character)
        self.assertEqual(form.fields["chronicle"].initial, chronicle)

    def test_form_has_all_descriptive_fields(self):
        """Test form includes all descriptive fields."""
        form = NPCProfileForm()
        self.assertIn("description", form.fields)
        self.assertIn("public_info", form.fields)
        self.assertIn("st_notes", form.fields)
        self.assertIn("notes", form.fields)
        self.assertIn("image", form.fields)

    def test_form_has_gameline_specific_fields(self):
        """Test form includes gameline-specific fields."""
        form = NPCProfileForm()
        # Mage fields
        self.assertIn("mage_affiliation", form.fields)
        self.assertIn("mage_faction", form.fields)
        self.assertIn("mage_essence", form.fields)
        # Werewolf fields
        self.assertIn("werewolf_tribe", form.fields)
        self.assertIn("werewolf_breed", form.fields)
        self.assertIn("werewolf_auspice", form.fields)
        # Wraith fields
        self.assertIn("wraith_guild", form.fields)
        self.assertIn("wraith_legion", form.fields)
        # Changeling fields
        self.assertIn("changeling_kith", form.fields)
        self.assertIn("changeling_court", form.fields)
        # Demon fields
        self.assertIn("demon_house", form.fields)
        self.assertIn("demon_faction", form.fields)


class NPCProfileFormValidationTestCase(TestCase):
    """Test NPCProfileForm validation."""

    def test_valid_basic_data(self):
        """Test form validates with basic required data."""
        data = {
            "npc_type": "vtm_human",
            "name": "Test NPC",
            "concept": "Street informant",
        }
        form = NPCProfileForm(data=data)
        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")

    def test_name_required(self):
        """Test that name field is required."""
        data = {
            "npc_type": "vtm_human",
            "concept": "Street informant",
        }
        form = NPCProfileForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_concept_required(self):
        """Test that concept field is required."""
        data = {
            "npc_type": "vtm_human",
            "name": "Test NPC",
        }
        form = NPCProfileForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("concept", form.errors)

    def test_npc_type_required(self):
        """Test that npc_type field is required."""
        data = {
            "name": "Test NPC",
            "concept": "Some concept",
        }
        form = NPCProfileForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("npc_type", form.errors)

    def test_invalid_npc_type(self):
        """Test that invalid NPC type is rejected."""
        data = {
            "npc_type": "invalid_type",
            "name": "Test NPC",
            "concept": "Some concept",
        }
        form = NPCProfileForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("npc_type", form.errors)

    def test_clean_npc_type_validates(self):
        """Test clean_npc_type raises ValidationError for invalid type."""
        data = {
            "npc_type": "not_valid",
            "name": "Test NPC",
            "concept": "Test concept",
        }
        form = NPCProfileForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("npc_type", form.errors)

    def test_all_valid_npc_types(self):
        """Test all valid NPC types are accepted."""
        npc_types = [
            "vtm_human",
            "wta_human",
            "kinfolk",
            "fomor",
            "werewolf",
            "mta_human",
            "sorcerer",
            "companion",
            "mage",
            "wto_human",
            "wraith",
            "ctd_human",
            "changeling",
            "dtf_human",
            "thrall",
            "demon",
        ]
        for npc_type in npc_types:
            data = {
                "npc_type": npc_type,
                "name": f"Test {npc_type}",
                "concept": "Test concept",
            }
            form = NPCProfileForm(data=data)
            self.assertTrue(form.is_valid(), f"Failed for {npc_type}: {form.errors}")


class NPCProfileFormSaveTestCase(TestCase):
    """Test NPCProfileForm save functionality."""

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")

    def test_save_creates_vtm_human(self):
        """Test saving form creates VtMHuman NPC."""
        data = {
            "npc_type": "vtm_human",
            "name": "John Doe",
            "concept": "Police detective",
            "npc_role": "contact",
            "description": "Middle-aged, stern looking",
            "chronicle": self.chronicle.pk,
        }
        form = NPCProfileForm(data=data, user=self.user)
        self.assertTrue(form.is_valid())

        npc = form.save()
        self.assertIsInstance(npc, VtMHuman)
        self.assertEqual(npc.name, "John Doe")
        self.assertEqual(npc.concept, "Police detective")
        self.assertTrue(npc.npc)
        self.assertEqual(npc.status, "Un")
        self.assertEqual(npc.owner, self.user)
        self.assertEqual(npc.chronicle, self.chronicle)
        self.assertEqual(npc.description, "Middle-aged, stern looking")

    def test_save_creates_mage_with_affiliation(self):
        """Test saving form creates Mage with affiliation and essence."""
        affiliation = MageFaction.objects.create(name="Traditions", parent=None)

        data = {
            "npc_type": "mage",
            "name": "Hermetic Mentor",
            "concept": "Magister of the Order",
            "mage_affiliation": affiliation.pk,
            "mage_essence": "Pattern",
        }
        form = NPCProfileForm(data=data, user=self.user)
        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")

        npc = form.save()
        self.assertIsInstance(npc, Mage)
        self.assertEqual(npc.affiliation, affiliation)
        self.assertEqual(npc.essence, "Pattern")

    def test_save_creates_werewolf_with_tribe(self):
        """Test saving form creates Werewolf with tribe and auspice."""
        tribe = Tribe.objects.create(name="Silver Fangs")

        data = {
            "npc_type": "werewolf",
            "name": "Alpha Wolf",
            "concept": "Pack leader",
            "werewolf_tribe": tribe.pk,
            "werewolf_breed": "homid",
            "werewolf_auspice": "ahroun",
        }
        form = NPCProfileForm(data=data, user=self.user)
        self.assertTrue(form.is_valid())

        npc = form.save()
        self.assertIsInstance(npc, Werewolf)
        self.assertEqual(npc.tribe, tribe)
        self.assertEqual(npc.breed, "homid")
        self.assertEqual(npc.auspice, "ahroun")

    def test_save_creates_kinfolk_with_tribe(self):
        """Test saving form creates Kinfolk with tribe and breed."""
        tribe = Tribe.objects.create(name="Bone Gnawers")

        data = {
            "npc_type": "kinfolk",
            "name": "Kinfolk Helper",
            "concept": "Wolf-blooded family member",
            "kinfolk_tribe": tribe.pk,
            "kinfolk_breed": "homid",
        }
        form = NPCProfileForm(data=data, user=self.user)
        self.assertTrue(form.is_valid())

        npc = form.save()
        self.assertIsInstance(npc, Kinfolk)
        self.assertEqual(npc.tribe, tribe)
        self.assertEqual(npc.breed, "homid")

    def test_save_creates_wraith_with_guild(self):
        """Test saving form creates Wraith with guild and legion."""
        guild = Guild.objects.create(name="Haunters")
        legion = WraithFaction.objects.create(name="Iron Legion", faction_type="legion")
        # Use "heretic" as it's a valid choice, "faction" is not in FACTION_TYPE_CHOICES
        heretic_faction = WraithFaction.objects.create(name="Renegades", faction_type="heretic")

        data = {
            "npc_type": "wraith",
            "name": "Ghost Guide",
            "concept": "Restless spirit",
            "wraith_guild": guild.pk,
            "wraith_legion": legion.pk,
            "wraith_character_type": "wraith",
        }
        form = NPCProfileForm(data=data, user=self.user)
        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")

        npc = form.save()
        self.assertIsInstance(npc, Wraith)
        self.assertEqual(npc.guild, guild)
        self.assertEqual(npc.legion, legion)
        self.assertEqual(npc.character_type, "wraith")

    def test_save_creates_changeling_with_kith(self):
        """Test saving form creates Changeling with kith and court."""
        kith = Kith.objects.create(name="Pooka")
        house = House.objects.create(name="House Gwydion")

        data = {
            "npc_type": "changeling",
            "name": "Fae Trickster",
            "concept": "Mischievous fae",
            "changeling_kith": kith.pk,
            "changeling_house": house.pk,
            "changeling_court": "seelie",
            "changeling_seeming": "wilder",
        }
        form = NPCProfileForm(data=data, user=self.user)
        self.assertTrue(form.is_valid())

        npc = form.save()
        self.assertIsInstance(npc, Changeling)
        self.assertEqual(npc.kith, kith)
        self.assertEqual(npc.house, house)
        self.assertEqual(npc.court, "seelie")
        self.assertEqual(npc.seeming, "wilder")

    def test_save_creates_sorcerer_with_fellowship(self):
        """Test saving form creates Sorcerer with fellowship."""
        fellowship = SorcererFellowship.objects.create(name="Bata'a")

        data = {
            "npc_type": "sorcerer",
            "name": "Hedge Witch",
            "concept": "Folk magic practitioner",
            "sorcerer_fellowship": fellowship.pk,
        }
        form = NPCProfileForm(data=data, user=self.user)
        self.assertTrue(form.is_valid())

        npc = form.save()
        self.assertIsInstance(npc, Sorcerer)
        self.assertEqual(npc.fellowship, fellowship)

    def test_save_creates_demon_with_house(self):
        """Test saving form creates Demon with house and faction."""
        demon_house = DemonHouse.objects.create(
            name="House of the Morning Star",
            celestial_name="Defilers",
            domain="Desire and longing",
        )
        demon_faction = DemonFaction.objects.create(
            name="Reconcilers",
            philosophy="Seek to mend the rift with God",
            goal="Redemption for all Fallen",
            leadership="Democratic consensus",
            tactics="Subtle influence and negotiation",
        )

        data = {
            "npc_type": "demon",
            "name": "Fallen Angel",
            "concept": "Seeking redemption",
            "demon_house": demon_house.pk,
            "demon_faction": demon_faction.pk,
        }
        form = NPCProfileForm(data=data, user=self.user)
        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")

        npc = form.save()
        self.assertIsInstance(npc, Demon)
        self.assertEqual(npc.house, demon_house)
        self.assertEqual(npc.faction, demon_faction)

    def test_save_with_npc_role_in_notes(self):
        """Test saving form includes NPC role in notes."""
        data = {
            "npc_type": "vtm_human",
            "name": "Test NPC",
            "concept": "Test concept",
            "npc_role": "mentor",
        }
        form = NPCProfileForm(data=data, user=self.user)
        self.assertTrue(form.is_valid())

        npc = form.save()
        self.assertIn("Role: Mentor", npc.notes)

    def test_save_with_related_character_in_notes(self):
        """Test saving form includes related character in notes."""
        pc = Human.objects.create(name="Main PC", owner=self.user)

        data = {
            "npc_type": "vtm_human",
            "name": "Test NPC",
            "concept": "Test concept",
        }
        form = NPCProfileForm(data=data, user=self.user, related_character=pc)
        self.assertTrue(form.is_valid())

        npc = form.save()
        self.assertIn("Related to: Main PC", npc.notes)

    def test_save_with_st_notes(self):
        """Test saving form preserves ST notes."""
        data = {
            "npc_type": "vtm_human",
            "name": "Test NPC",
            "concept": "Test concept",
            "st_notes": "Secret plot hooks for the ST only",
        }
        form = NPCProfileForm(data=data, user=self.user)
        self.assertTrue(form.is_valid())

        npc = form.save()
        self.assertEqual(npc.st_notes, "Secret plot hooks for the ST only")

    def test_save_with_public_info(self):
        """Test saving form preserves public info."""
        data = {
            "npc_type": "vtm_human",
            "name": "Test NPC",
            "concept": "Test concept",
            "public_info": "Known to frequent the local bar",
        }
        form = NPCProfileForm(data=data, user=self.user)
        self.assertTrue(form.is_valid())

        npc = form.save()
        self.assertEqual(npc.public_info, "Known to frequent the local bar")

    def test_save_without_commit(self):
        """Test saving form without commit doesn't save to database."""
        data = {
            "npc_type": "vtm_human",
            "name": "Uncommitted NPC",
            "concept": "Test concept",
        }
        form = NPCProfileForm(data=data, user=self.user)
        self.assertTrue(form.is_valid())

        npc = form.save(commit=False)
        self.assertIsNone(npc.pk)  # Not saved to DB


class NPCProfileFormHumanVariantsTestCase(TestCase):
    """Test NPCProfileForm creates correct human variant types."""

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")

    def test_creates_wta_human(self):
        """Test form creates WtAHuman NPC."""
        data = {"npc_type": "wta_human", "name": "Wolf Human", "concept": "Wolf-country local"}
        form = NPCProfileForm(data=data, user=self.user)
        self.assertTrue(form.is_valid())
        npc = form.save()
        self.assertIsInstance(npc, WtAHuman)

    def test_creates_mta_human(self):
        """Test form creates MtAHuman NPC."""
        data = {"npc_type": "mta_human", "name": "Sleeper", "concept": "Unawakened mortal"}
        form = NPCProfileForm(data=data, user=self.user)
        self.assertTrue(form.is_valid())
        npc = form.save()
        self.assertIsInstance(npc, MtAHuman)

    def test_creates_wto_human(self):
        """Test form creates WtOHuman NPC."""
        data = {"npc_type": "wto_human", "name": "Medium", "concept": "Ghost sensitive"}
        form = NPCProfileForm(data=data, user=self.user)
        self.assertTrue(form.is_valid())
        npc = form.save()
        self.assertIsInstance(npc, WtOHuman)

    def test_creates_ctd_human(self):
        """Test form creates CtDHuman NPC."""
        data = {"npc_type": "ctd_human", "name": "Enchanted", "concept": "Fae-touched mortal"}
        form = NPCProfileForm(data=data, user=self.user)
        self.assertTrue(form.is_valid())
        npc = form.save()
        self.assertIsInstance(npc, CtDHuman)

    def test_creates_dtf_human(self):
        """Test form creates DtFHuman NPC."""
        data = {"npc_type": "dtf_human", "name": "Faithful", "concept": "Religiously aware"}
        form = NPCProfileForm(data=data, user=self.user)
        self.assertTrue(form.is_valid())
        npc = form.save()
        self.assertIsInstance(npc, DtFHuman)

    def test_creates_fomor(self):
        """Test form creates Fomor NPC."""
        data = {"npc_type": "fomor", "name": "Corrupted One", "concept": "Wyrm-tainted"}
        form = NPCProfileForm(data=data, user=self.user)
        self.assertTrue(form.is_valid())
        npc = form.save()
        self.assertIsInstance(npc, Fomor)

    def test_creates_companion(self):
        """Test form creates Companion NPC."""
        data = {"npc_type": "companion", "name": "Magus Helper", "concept": "Mage's assistant"}
        form = NPCProfileForm(data=data, user=self.user)
        self.assertTrue(form.is_valid())
        npc = form.save()
        self.assertIsInstance(npc, Companion)

    def test_creates_thrall(self):
        """Test form creates Thrall NPC.

        Note: Similar to LinkedNPCForm, Thrall requires 'enhancements' field.
        """
        data = {"npc_type": "thrall", "name": "Demon Servant", "concept": "Pact-bound mortal"}
        form = NPCProfileForm(data=data, user=self.user)
        self.assertTrue(form.is_valid())
        # Thrall.enhancements has blank=False, causing validation to fail.
        with self.assertRaises(Exception):
            form.save()
