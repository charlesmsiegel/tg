"""
Tests for character utilities.

Tests cover:
- get_character_object_type function
- Human type normalization
- ObjectType creation
"""

from django.test import TestCase

from characters.utils import get_character_object_type
from game.models import ObjectType


class GetCharacterObjectTypeTests(TestCase):
    """Tests for get_character_object_type utility function."""

    def test_normalizes_vtm_human_to_human(self):
        """Test that vtm_human normalizes to human."""
        obj_type = get_character_object_type("vtm_human")
        self.assertEqual(obj_type.name, "human")

    def test_normalizes_mta_human_to_human(self):
        """Test that mta_human normalizes to human."""
        obj_type = get_character_object_type("mta_human")
        self.assertEqual(obj_type.name, "human")

    def test_normalizes_wta_human_to_human(self):
        """Test that wta_human normalizes to human."""
        obj_type = get_character_object_type("wta_human")
        self.assertEqual(obj_type.name, "human")

    def test_normalizes_ctd_human_to_human(self):
        """Test that ctd_human normalizes to human."""
        obj_type = get_character_object_type("ctd_human")
        self.assertEqual(obj_type.name, "human")

    def test_normalizes_wto_human_to_human(self):
        """Test that wto_human normalizes to human."""
        obj_type = get_character_object_type("wto_human")
        self.assertEqual(obj_type.name, "human")

    def test_normalizes_dtf_human_to_human(self):
        """Test that dtf_human normalizes to human."""
        obj_type = get_character_object_type("dtf_human")
        self.assertEqual(obj_type.name, "human")

    def test_normalizes_plain_human(self):
        """Test that plain 'human' stays as 'human'."""
        obj_type = get_character_object_type("human")
        self.assertEqual(obj_type.name, "human")

    def test_keeps_vampire_unchanged(self):
        """Test that vampire type is not normalized."""
        obj_type = get_character_object_type("vampire")
        self.assertEqual(obj_type.name, "vampire")

    def test_keeps_mage_unchanged(self):
        """Test that mage type is not normalized."""
        obj_type = get_character_object_type("mage")
        self.assertEqual(obj_type.name, "mage")

    def test_keeps_werewolf_unchanged(self):
        """Test that werewolf type is not normalized."""
        obj_type = get_character_object_type("werewolf")
        self.assertEqual(obj_type.name, "werewolf")

    def test_keeps_wraith_unchanged(self):
        """Test that wraith type is not normalized."""
        obj_type = get_character_object_type("wraith")
        self.assertEqual(obj_type.name, "wraith")

    def test_keeps_changeling_unchanged(self):
        """Test that changeling type is not normalized."""
        obj_type = get_character_object_type("changeling")
        self.assertEqual(obj_type.name, "changeling")

    def test_does_not_normalize_inhuman(self):
        """Test that 'inhuman' is NOT normalized to 'human'.

        This verifies the fix for the substring matching bug where
        'human' in 'inhuman' would incorrectly match.
        """
        obj_type = get_character_object_type("inhuman")
        self.assertEqual(obj_type.name, "inhuman")

    def test_does_not_normalize_superhuman(self):
        """Test that 'superhuman' is NOT normalized to 'human'."""
        obj_type = get_character_object_type("superhuman")
        self.assertEqual(obj_type.name, "superhuman")

    def test_respects_gameline_parameter(self):
        """Test that gameline parameter is used correctly for new types."""
        # Clear any existing vampire type
        ObjectType.objects.filter(name="test_vampire").delete()

        obj_type = get_character_object_type("test_vampire", gameline="vtm")
        self.assertEqual(obj_type.gameline, "vtm")

    def test_creates_object_type_if_not_exists(self):
        """Test that ObjectType is created if it doesn't exist."""
        # Ensure the type doesn't exist
        ObjectType.objects.filter(name="new_test_type").delete()

        obj_type = get_character_object_type("new_test_type")
        self.assertEqual(obj_type.name, "new_test_type")
        self.assertEqual(obj_type.type, "char")
        self.assertEqual(obj_type.gameline, "wod")

    def test_returns_existing_object_type(self):
        """Test that existing ObjectType is returned."""
        # Create the type first
        existing = ObjectType.objects.create(
            name="existing_type", type="char", gameline="vtm"
        )

        obj_type = get_character_object_type("existing_type")
        self.assertEqual(obj_type.pk, existing.pk)

    def test_multiple_human_variants_return_same_type(self):
        """Test that all human variants return the same ObjectType."""
        vtm_human = get_character_object_type("vtm_human")
        mta_human = get_character_object_type("mta_human")
        plain_human = get_character_object_type("human")

        self.assertEqual(vtm_human.pk, mta_human.pk)
        self.assertEqual(vtm_human.pk, plain_human.pk)
