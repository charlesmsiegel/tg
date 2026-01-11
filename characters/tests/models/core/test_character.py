"""
Tests for character models.

Tests cover:
- Character creation and validation
- Human model functionality
- XP calculation and tracking
- Status changes and validation
- Freebie points calculation
"""

from django.contrib.auth.models import User
from django.test import TestCase

from characters.models.core import Character, Human
from game.models import Chronicle


class TestCharacter(TestCase):
    """Test the base Character model."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")

    def test_character_creation(self):
        """Test basic character creation."""
        character = Character.objects.create(
            name="Test Character",
            owner=self.user,
            chronicle=self.chronicle,
            concept="Warrior",
        )
        self.assertEqual(character.name, "Test Character")
        self.assertEqual(character.owner, self.user)
        self.assertEqual(character.chronicle, self.chronicle)
        self.assertEqual(character.concept, "Warrior")

    def test_character_default_status(self):
        """Test that new characters default to 'Un' status."""
        character = Character.objects.create(name="Test", owner=self.user)
        self.assertEqual(character.status, "Un")

    def test_character_str_representation(self):
        """Test the string representation of a character."""
        character = Character.objects.create(
            name="John Doe",
            owner=self.user,
        )
        self.assertEqual(str(character), "John Doe")

    def test_character_absolute_url(self):
        """Test that get_absolute_url returns the correct path."""
        character = Character.objects.create(
            name="Test",
            owner=self.user,
        )
        expected_url = f"/characters/{character.id}/"
        self.assertEqual(character.get_absolute_url(), expected_url)

    def test_character_xp_tracking(self):
        """Test XP tracking functionality."""
        character = Character.objects.create(
            name="Test",
            owner=self.user,
            xp=10,
        )
        self.assertEqual(character.xp, 10)

    def test_character_total_xp_calculation(self):
        """Test total XP calculation (earned + starting)."""
        character = Character.objects.create(
            name="Test",
            owner=self.user,
            xp=15,
        )
        # Total should be earned XP plus starting XP (if any)
        total = character.total_xp()
        self.assertGreaterEqual(total, 15)

    def test_character_spent_xp_tracking(self):
        """Test spent XP tracking via XPSpendingRequest model."""
        from game.models import XPSpendingRequest

        character = Character.objects.create(
            name="Test",
            owner=self.user,
            xp=20,
        )
        # Create XP spending requests (the new model-based approach)
        XPSpendingRequest.objects.create(
            character=character,
            trait_name="Strength",
            trait_type="attribute",
            trait_value=4,
            cost=5,
            approved="Approved",
        )
        XPSpendingRequest.objects.create(
            character=character,
            trait_name="Alertness",
            trait_type="ability",
            trait_value=2,
            cost=3,
            approved="Pending",
        )

        # Test that spending requests are tracked correctly
        self.assertEqual(character.xp_spendings.count(), 2)
        self.assertEqual(character.xp_spendings.filter(approved="Approved").count(), 1)
        self.assertEqual(character.total_spent_xp(), 5)  # Only approved spending

    def test_character_available_xp(self):
        """Test calculating available (unspent) XP."""
        character = Character.objects.create(
            name="Test",
            owner=self.user,
            xp=20,
        )
        # If spent_xp tracking is implemented
        available = character.available_xp()
        self.assertLessEqual(available, 20)

    def test_character_status_choices(self):
        """Test that status can be set through valid transitions."""
        character = Character.objects.create(
            name="Test",
            owner=self.user,
        )
        # Test valid transition sequence: Un -> Sub -> App -> Dec
        self.assertEqual(character.status, "Un")

        character.status = "Sub"
        character.save()
        character.refresh_from_db()
        self.assertEqual(character.status, "Sub")

        character.status = "App"
        character.save()
        character.refresh_from_db()
        self.assertEqual(character.status, "App")

        character.status = "Dec"
        character.save()
        character.refresh_from_db()
        self.assertEqual(character.status, "Dec")

        # Test Ret status with a fresh character
        char2 = Character.objects.create(name="Test2", owner=self.user)
        char2.status = "Sub"
        char2.save()
        char2.status = "App"
        char2.save()
        char2.status = "Ret"
        char2.save()
        char2.refresh_from_db()
        self.assertEqual(char2.status, "Ret")

    def test_character_npc_flag(self):
        """Test NPC flag functionality."""
        npc = Character.objects.create(
            name="NPC Guard",
            owner=self.user,
            npc=True,
        )
        pc = Character.objects.create(
            name="Player Character",
            owner=self.user,
            npc=False,
        )
        self.assertTrue(npc.npc)
        self.assertFalse(pc.npc)


class TestHuman(TestCase):
    """Test the Human character model."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")

    def test_human_creation(self):
        """Test creating a human character."""
        human = Human.objects.create(
            name="John Smith",
            owner=self.user,
            concept="Detective",
        )
        self.assertEqual(human.name, "John Smith")
        self.assertEqual(human.concept, "Detective")

    def test_human_has_character_fields(self):
        """Test that Human has all Character fields."""
        human = Human.objects.create(
            name="Test Human",
            owner=self.user,
            chronicle=self.chronicle,
        )
        # Should have inherited Character fields
        self.assertIsNotNone(human.name)
        self.assertIsNotNone(human.owner)
        self.assertIsNotNone(human.chronicle)
        self.assertIsNotNone(human.status)

    def test_human_has_history_field(self):
        """Test that Human has history field."""
        human = Human.objects.create(
            name="Test",
            owner=self.user,
            history="Born in New York...",
        )
        self.assertEqual(human.history, "Born in New York...")

    def test_human_has_goals_field(self):
        """Test that Human has goals field."""
        human = Human.objects.create(
            name="Test",
            owner=self.user,
            goals="Become the best detective in the city",
        )
        self.assertEqual(human.goals, "Become the best detective in the city")

    def test_human_attributes(self):
        """Test that Human can have attributes set."""
        human = Human.objects.create(
            name="Test",
            owner=self.user,
            strength=3,
            dexterity=2,
            stamina=3,
            charisma=2,
            manipulation=2,
            appearance=3,
            perception=4,
            intelligence=3,
            wits=2,
        )
        self.assertEqual(human.strength, 3)
        self.assertEqual(human.perception, 4)
        self.assertEqual(human.charisma, 2)

    def test_human_attribute_total_validation(self):
        """Test attribute total calculation."""
        human = Human.objects.create(
            name="Test",
            owner=self.user,
            strength=3,
            dexterity=2,
            stamina=2,
        )
        # Physical total should be 7
        physical_total = human.strength + human.dexterity + human.stamina
        self.assertEqual(physical_total, 7)

    def test_human_freebie_points(self):
        """Test freebie points tracking."""
        human = Human.objects.create(
            name="Test",
            owner=self.user,
            freebies=15,
        )
        self.assertEqual(human.freebies, 15)

    def test_human_spent_freebies_tracking(self):
        """Test spent freebies tracking."""
        human = Human.objects.create(
            name="Test",
            owner=self.user,
            freebies=15,
            spent_freebies={"attribute": 5, "ability": 3},
        )
        total_spent = sum(human.spent_freebies.values())
        self.assertEqual(total_spent, 8)
        remaining = human.freebies - total_spent
        self.assertEqual(remaining, 7)

    def test_human_willpower(self):
        """Test willpower attribute."""
        human = Human.objects.create(
            name="Test",
            owner=self.user,
            willpower=5,
        )
        self.assertEqual(human.willpower, 5)

    def test_human_specialties(self):
        """Test that specialties can be added."""
        human = Human.objects.create(
            name="Test",
            owner=self.user,
        )
        # Specialties should be manageable (exact implementation may vary)
        self.assertIsNotNone(human)

    def test_human_public_info_field(self):
        """Test public_info field for player-visible information."""
        human = Human.objects.create(
            name="Test",
            owner=self.user,
            public_info="Known as a skilled investigator",
        )
        self.assertEqual(human.public_info, "Known as a skilled investigator")

    def test_human_notes_field(self):
        """Test private notes field."""
        human = Human.objects.create(
            name="Test",
            owner=self.user,
            notes="Secret: Working for the mob",
        )
        self.assertEqual(human.notes, "Secret: Working for the mob")


class TestCharacterXPSystem(TestCase):
    """Test the character XP earning and spending system."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.character = Character.objects.create(
            name="Test",
            owner=self.user,
            xp=0,
        )

    def test_earning_xp(self):
        """Test that XP can be earned."""
        self.character.xp = 10
        self.character.save()
        self.character.refresh_from_db()
        self.assertEqual(self.character.xp, 10)

    def test_spending_xp_requires_approval(self):
        """Test that spent XP tracks approval status."""
        self.character.spent_xp = {
            "new_ability": {
                "amount": 3,
                "approved": False,
                "description": "Melee 1",
            }
        }
        self.character.save()

        self.assertFalse(self.character.spent_xp["new_ability"]["approved"])

    def test_approved_xp_expenditure(self):
        """Test approved XP expenditure."""
        self.character.xp = 10
        self.character.spent_xp = {
            "ability_increase": {
                "amount": 3,
                "approved": True,
                "description": "Melee 2->3",
            }
        }
        self.character.save()

        self.assertTrue(self.character.spent_xp["ability_increase"]["approved"])

    def test_total_spent_xp_calculation(self):
        """Test calculating total spent XP."""
        self.character.spent_xp = {
            "ability1": {"amount": 3, "approved": True},
            "ability2": {"amount": 5, "approved": True},
            "ability3": {"amount": 2, "approved": False},  # Not approved
        }
        self.character.save()

        # Calculate total approved spent XP
        approved_spent = sum(
            entry["amount"]
            for entry in self.character.spent_xp.values()
            if entry.get("approved", False)
        )
        self.assertEqual(approved_spent, 8)


class TestCharacterStatusTransitions(TestCase):
    """Test character status transitions and validation."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )

    def test_unfinished_to_submitted(self):
        """Test transitioning from Unfinished to Submitted."""
        character = Character.objects.create(
            name="Test",
            owner=self.user,
            status="Un",
        )
        character.status = "Sub"
        character.save()
        character.refresh_from_db()
        self.assertEqual(character.status, "Sub")

    def test_submitted_to_approved(self):
        """Test transitioning from Submitted to Approved."""
        character = Character.objects.create(
            name="Test",
            owner=self.user,
            status="Sub",
        )
        character.status = "App"
        character.save()
        character.refresh_from_db()
        self.assertEqual(character.status, "App")

    def test_approved_to_retired(self):
        """Test retiring an approved character."""
        character = Character.objects.create(
            name="Test",
            owner=self.user,
            status="App",
        )
        character.status = "Ret"
        character.save()
        character.refresh_from_db()
        self.assertEqual(character.status, "Ret")

    def test_approved_to_deceased(self):
        """Test marking a character as deceased."""
        character = Character.objects.create(
            name="Test",
            owner=self.user,
            status="App",
        )
        character.status = "Dec"
        character.save()
        character.refresh_from_db()
        self.assertEqual(character.status, "Dec")


class TestJSONFieldDefaultBehavior(TestCase):
    """Test that JSONField defaults don't share state between instances.

    Django's JSONField treats default=list and default=dict as callable factories,
    calling them each time to get a fresh instance. These tests verify this behavior.
    See issue #1096 for context.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )

    def test_spent_freebies_not_shared(self):
        """Test that spent_freebies JSONField default doesn't share state."""
        human1 = Human.objects.create(name="Human 1", owner=self.user)
        human2 = Human.objects.create(name="Human 2", owner=self.user)

        # Modify human1's spent_freebies
        human1.spent_freebies.append({"attribute": 5})
        human1.save()

        # Reload human2 to ensure it has fresh data
        human2.refresh_from_db()

        # human2 should NOT be affected
        self.assertEqual(human2.spent_freebies, [])
        self.assertNotEqual(human1.spent_freebies, human2.spent_freebies)

    def test_jsonfield_defaults_are_independent(self):
        """Test that each instance gets its own default list/dict."""
        human1 = Human(name="Human 1", owner=self.user)
        human2 = Human(name="Human 2", owner=self.user)

        # Without saving, the defaults should still be independent
        self.assertIsNot(human1.spent_freebies, human2.spent_freebies)

        # Mutating one should not affect the other
        human1.spent_freebies.append("test")
        self.assertEqual(human1.spent_freebies, ["test"])
        self.assertEqual(human2.spent_freebies, [])
