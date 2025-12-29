"""
Tests for Vampire model.

Tests cover:
- Vampire creation and basic attributes
- Generation effects (blood pool, blood per turn)
- Discipline tracking and costs
- Virtue system (active virtues, setting virtues)
- Freebie costs and spending
- XP costs and spending
"""

from characters.models.vampire.clan import VampireClan
from characters.models.vampire.discipline import Discipline
from characters.models.vampire.path import Path
from characters.models.vampire.sect import VampireSect
from characters.models.vampire.vampire import Vampire
from django.contrib.auth.models import User
from django.test import TestCase
from game.models import Chronicle


class VampireModelTestCase(TestCase):
    """Base test case with common setup for Vampire model tests."""

    @classmethod
    def setUpTestData(cls):
        """Set up test data for all test methods."""
        # Create disciplines
        cls.potence = Discipline.objects.create(name="Potence", property_name="potence")
        cls.celerity = Discipline.objects.create(name="Celerity", property_name="celerity")
        cls.fortitude = Discipline.objects.create(name="Fortitude", property_name="fortitude")
        cls.dominate = Discipline.objects.create(name="Dominate", property_name="dominate")
        cls.presence = Discipline.objects.create(name="Presence", property_name="presence")
        cls.auspex = Discipline.objects.create(name="Auspex", property_name="auspex")

        # Create a clan with disciplines
        cls.brujah = VampireClan.objects.create(
            name="Brujah",
            nickname="Rabble",
            weakness="Prone to frenzy",
        )
        cls.brujah.disciplines.add(cls.potence, cls.celerity, cls.presence)

        cls.ventrue = VampireClan.objects.create(
            name="Ventrue",
            nickname="Blue Bloods",
            weakness="Refined palate",
        )
        cls.ventrue.disciplines.add(cls.dominate, cls.fortitude, cls.presence)

        # Create a sect
        cls.camarilla = VampireSect.objects.create(name="Camarilla")

        # Create a path of enlightenment
        cls.path_of_caine = Path.objects.create(
            name="Path of Caine",
            requires_conviction=True,
            requires_instinct=True,
            ethics="Follow the ways of the First Vampire",
        )

    def setUp(self):
        """Set up test user and character."""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@test.com",
            password="testpassword",
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")


class TestVampireCreation(VampireModelTestCase):
    """Test Vampire model creation and basic attributes."""

    def test_vampire_creation_basic(self):
        """Test basic vampire creation."""
        vampire = Vampire.objects.create(
            name="Test Vampire",
            owner=self.user,
            chronicle=self.chronicle,
            concept="Warrior",
        )
        self.assertEqual(vampire.name, "Test Vampire")
        self.assertEqual(vampire.owner, self.user)
        self.assertEqual(vampire.concept, "Warrior")
        self.assertEqual(vampire.type, "vampire")

    def test_vampire_default_generation(self):
        """Test that new vampires default to 13th generation."""
        vampire = Vampire.objects.create(name="Test", owner=self.user)
        self.assertEqual(vampire.generation_rating, 13)

    def test_vampire_default_blood_pool(self):
        """Test that default blood pool matches 13th generation."""
        vampire = Vampire.objects.create(name="Test", owner=self.user)
        self.assertEqual(vampire.max_blood_pool, 10)
        self.assertEqual(vampire.blood_per_turn, 1)

    def test_vampire_default_virtues(self):
        """Test default virtue configuration (Humanity with Conscience/Self-Control)."""
        vampire = Vampire.objects.create(name="Test", owner=self.user)
        self.assertFalse(vampire.has_conviction)
        self.assertFalse(vampire.has_instinct)
        self.assertEqual(vampire.conscience, 1)
        self.assertEqual(vampire.self_control, 1)
        self.assertEqual(vampire.courage, 1)
        self.assertEqual(vampire.humanity, 7)

    def test_vampire_can_have_clan(self):
        """Test assigning a clan to a vampire."""
        vampire = Vampire.objects.create(
            name="Test",
            owner=self.user,
            clan=self.brujah,
        )
        self.assertEqual(vampire.clan, self.brujah)

    def test_vampire_can_have_sect(self):
        """Test assigning a sect to a vampire."""
        vampire = Vampire.objects.create(
            name="Test",
            owner=self.user,
            sect=self.camarilla,
        )
        self.assertEqual(vampire.sect, self.camarilla)

    def test_vampire_get_absolute_url(self):
        """Test that get_absolute_url returns correct path."""
        vampire = Vampire.objects.create(name="Test", owner=self.user)
        expected_url = f"/characters/vampire/vampire/{vampire.id}/"
        self.assertEqual(vampire.get_absolute_url(), expected_url)

    def test_vampire_get_update_url(self):
        """Test that get_update_url returns correct path."""
        vampire = Vampire.objects.create(name="Test", owner=self.user)
        expected_url = f"/characters/vampire/update/vampire/{vampire.pk}/"
        self.assertEqual(vampire.get_update_url(), expected_url)

    def test_vampire_get_creation_url(self):
        """Test that get_creation_url returns correct path."""
        expected_url = "/characters/vampire/create/vampire/"
        self.assertEqual(Vampire.get_creation_url(), expected_url)

    def test_vampire_get_heading(self):
        """Test that get_heading returns vtm_heading."""
        vampire = Vampire.objects.create(name="Test", owner=self.user)
        self.assertEqual(vampire.get_heading(), "vtm_heading")


class TestVampireGenerationEffects(VampireModelTestCase):
    """Test generation-dependent values (blood pool, blood per turn)."""

    def test_generation_3_blood_pool(self):
        """Test 3rd generation blood pool values."""
        vampire = Vampire.objects.create(
            name="Antediluvian",
            owner=self.user,
            generation_rating=3,
        )
        self.assertEqual(vampire.max_blood_pool, 50)
        self.assertEqual(vampire.blood_per_turn, 10)

    def test_generation_4_blood_pool(self):
        """Test 4th generation blood pool values."""
        vampire = Vampire.objects.create(
            name="Methuselah",
            owner=self.user,
            generation_rating=4,
        )
        self.assertEqual(vampire.max_blood_pool, 50)
        self.assertEqual(vampire.blood_per_turn, 10)

    def test_generation_5_blood_pool(self):
        """Test 5th generation blood pool values."""
        vampire = Vampire.objects.create(
            name="Elder",
            owner=self.user,
            generation_rating=5,
        )
        self.assertEqual(vampire.max_blood_pool, 40)
        self.assertEqual(vampire.blood_per_turn, 8)

    def test_generation_6_blood_pool(self):
        """Test 6th generation blood pool values."""
        vampire = Vampire.objects.create(
            name="Elder",
            owner=self.user,
            generation_rating=6,
        )
        self.assertEqual(vampire.max_blood_pool, 30)
        self.assertEqual(vampire.blood_per_turn, 6)

    def test_generation_7_blood_pool(self):
        """Test 7th generation blood pool values."""
        vampire = Vampire.objects.create(
            name="Elder",
            owner=self.user,
            generation_rating=7,
        )
        self.assertEqual(vampire.max_blood_pool, 20)
        self.assertEqual(vampire.blood_per_turn, 4)

    def test_generation_8_blood_pool(self):
        """Test 8th generation blood pool values."""
        vampire = Vampire.objects.create(
            name="Ancilla",
            owner=self.user,
            generation_rating=8,
        )
        self.assertEqual(vampire.max_blood_pool, 15)
        self.assertEqual(vampire.blood_per_turn, 3)

    def test_generation_9_blood_pool(self):
        """Test 9th generation blood pool values."""
        vampire = Vampire.objects.create(
            name="Ancilla",
            owner=self.user,
            generation_rating=9,
        )
        self.assertEqual(vampire.max_blood_pool, 14)
        self.assertEqual(vampire.blood_per_turn, 2)

    def test_generation_10_blood_pool(self):
        """Test 10th generation blood pool values."""
        vampire = Vampire.objects.create(
            name="Neonate",
            owner=self.user,
            generation_rating=10,
        )
        self.assertEqual(vampire.max_blood_pool, 13)
        self.assertEqual(vampire.blood_per_turn, 1)

    def test_generation_11_blood_pool(self):
        """Test 11th generation blood pool values."""
        vampire = Vampire.objects.create(
            name="Neonate",
            owner=self.user,
            generation_rating=11,
        )
        self.assertEqual(vampire.max_blood_pool, 12)
        self.assertEqual(vampire.blood_per_turn, 1)

    def test_generation_12_blood_pool(self):
        """Test 12th generation blood pool values."""
        vampire = Vampire.objects.create(
            name="Neonate",
            owner=self.user,
            generation_rating=12,
        )
        self.assertEqual(vampire.max_blood_pool, 11)
        self.assertEqual(vampire.blood_per_turn, 1)

    def test_generation_13_blood_pool(self):
        """Test 13th generation blood pool values."""
        vampire = Vampire.objects.create(
            name="Fledgling",
            owner=self.user,
            generation_rating=13,
        )
        self.assertEqual(vampire.max_blood_pool, 10)
        self.assertEqual(vampire.blood_per_turn, 1)

    def test_generation_14_blood_pool(self):
        """Test 14th generation (thin-blood) blood pool values."""
        vampire = Vampire.objects.create(
            name="Thin-Blood",
            owner=self.user,
            generation_rating=14,
        )
        self.assertEqual(vampire.max_blood_pool, 10)
        self.assertEqual(vampire.blood_per_turn, 1)

    def test_generation_15_blood_pool(self):
        """Test 15th generation (thin-blood) blood pool values."""
        vampire = Vampire.objects.create(
            name="Thin-Blood",
            owner=self.user,
            generation_rating=15,
        )
        self.assertEqual(vampire.max_blood_pool, 10)
        self.assertEqual(vampire.blood_per_turn, 1)

    def test_generation_change_updates_blood_pool(self):
        """Test that changing generation updates blood pool on save."""
        vampire = Vampire.objects.create(
            name="Test",
            owner=self.user,
            generation_rating=13,
        )
        self.assertEqual(vampire.max_blood_pool, 10)

        vampire.generation_rating = 8
        vampire.save()
        vampire.refresh_from_db()

        self.assertEqual(vampire.max_blood_pool, 15)
        self.assertEqual(vampire.blood_per_turn, 3)


class TestVampireDisciplines(VampireModelTestCase):
    """Test discipline tracking and methods."""

    def test_get_disciplines_empty(self):
        """Test get_disciplines with no disciplines."""
        vampire = Vampire.objects.create(name="Test", owner=self.user)
        disciplines = vampire.get_disciplines()
        self.assertEqual(disciplines, {})

    def test_get_disciplines_with_ratings(self):
        """Test get_disciplines returns only disciplines with ratings > 0."""
        vampire = Vampire.objects.create(
            name="Test",
            owner=self.user,
            potence=3,
            celerity=2,
            fortitude=0,  # Should not appear
        )
        disciplines = vampire.get_disciplines()
        self.assertEqual(disciplines, {"Potence": 3, "Celerity": 2})
        self.assertNotIn("Fortitude", disciplines)

    def test_get_clan_disciplines_with_clan(self):
        """Test get_clan_disciplines returns clan disciplines."""
        vampire = Vampire.objects.create(
            name="Test",
            owner=self.user,
            clan=self.brujah,
        )
        clan_disciplines = vampire.get_clan_disciplines()
        discipline_names = [d.name for d in clan_disciplines]
        self.assertIn("Potence", discipline_names)
        self.assertIn("Celerity", discipline_names)
        self.assertIn("Presence", discipline_names)

    def test_get_clan_disciplines_without_clan(self):
        """Test get_clan_disciplines returns empty list without clan."""
        vampire = Vampire.objects.create(name="Test", owner=self.user)
        clan_disciplines = vampire.get_clan_disciplines()
        self.assertEqual(clan_disciplines, [])

    def test_is_clan_discipline_true(self):
        """Test is_clan_discipline returns True for in-clan discipline."""
        vampire = Vampire.objects.create(
            name="Test",
            owner=self.user,
            clan=self.brujah,
        )
        self.assertTrue(vampire.is_clan_discipline(self.potence))
        self.assertTrue(vampire.is_clan_discipline("potence"))

    def test_is_clan_discipline_false(self):
        """Test is_clan_discipline returns False for out-of-clan discipline."""
        vampire = Vampire.objects.create(
            name="Test",
            owner=self.user,
            clan=self.brujah,
        )
        self.assertFalse(vampire.is_clan_discipline(self.dominate))
        self.assertFalse(vampire.is_clan_discipline("dominate"))

    def test_is_clan_discipline_no_clan(self):
        """Test is_clan_discipline returns False without clan."""
        vampire = Vampire.objects.create(name="Test", owner=self.user)
        self.assertFalse(vampire.is_clan_discipline(self.potence))


class TestVampireVirtues(VampireModelTestCase):
    """Test virtue system and properties."""

    def test_active_virtue_1_conscience(self):
        """Test active_virtue_1 returns Conscience when has_conviction is False."""
        vampire = Vampire.objects.create(
            name="Test",
            owner=self.user,
            has_conviction=False,
            conscience=3,
            conviction=2,
        )
        self.assertEqual(vampire.active_virtue_1, 3)
        self.assertEqual(vampire.active_virtue_1_name, "Conscience")

    def test_active_virtue_1_conviction(self):
        """Test active_virtue_1 returns Conviction when has_conviction is True."""
        vampire = Vampire.objects.create(
            name="Test",
            owner=self.user,
            has_conviction=True,
            conscience=3,
            conviction=4,
        )
        self.assertEqual(vampire.active_virtue_1, 4)
        self.assertEqual(vampire.active_virtue_1_name, "Conviction")

    def test_active_virtue_2_self_control(self):
        """Test active_virtue_2 returns Self-Control when has_instinct is False."""
        vampire = Vampire.objects.create(
            name="Test",
            owner=self.user,
            has_instinct=False,
            self_control=3,
            instinct=2,
        )
        self.assertEqual(vampire.active_virtue_2, 3)
        self.assertEqual(vampire.active_virtue_2_name, "Self-Control")

    def test_active_virtue_2_instinct(self):
        """Test active_virtue_2 returns Instinct when has_instinct is True."""
        vampire = Vampire.objects.create(
            name="Test",
            owner=self.user,
            has_instinct=True,
            self_control=3,
            instinct=4,
        )
        self.assertEqual(vampire.active_virtue_2, 4)
        self.assertEqual(vampire.active_virtue_2_name, "Instinct")

    def test_get_active_virtues_humanity(self):
        """Test get_active_virtues for Humanity character."""
        vampire = Vampire.objects.create(
            name="Test",
            owner=self.user,
            has_conviction=False,
            has_instinct=False,
            conscience=3,
            self_control=2,
            courage=4,
        )
        virtues = vampire.get_active_virtues()
        self.assertEqual(virtues, {
            "Conscience": 3,
            "Self-Control": 2,
            "Courage": 4,
        })

    def test_get_active_virtues_path(self):
        """Test get_active_virtues for Path follower."""
        vampire = Vampire.objects.create(
            name="Test",
            owner=self.user,
            has_conviction=True,
            has_instinct=True,
            conviction=4,
            instinct=3,
            courage=2,
        )
        virtues = vampire.get_active_virtues()
        self.assertEqual(virtues, {
            "Conviction": 4,
            "Instinct": 3,
            "Courage": 2,
        })

    def test_set_virtue_by_name_valid(self):
        """Test set_virtue_by_name with valid virtue names."""
        vampire = Vampire.objects.create(name="Test", owner=self.user)

        vampire.set_virtue_by_name("conscience", 4)
        self.assertEqual(vampire.conscience, 4)

        vampire.set_virtue_by_name("Conviction", 3)
        self.assertEqual(vampire.conviction, 3)

        vampire.set_virtue_by_name("SELF_CONTROL", 5)
        self.assertEqual(vampire.self_control, 5)

        vampire.set_virtue_by_name("instinct", 2)
        self.assertEqual(vampire.instinct, 2)

        vampire.set_virtue_by_name("Courage", 4)
        self.assertEqual(vampire.courage, 4)

    def test_set_virtue_by_name_invalid(self):
        """Test set_virtue_by_name raises error for invalid virtue."""
        vampire = Vampire.objects.create(name="Test", owner=self.user)

        with self.assertRaises(ValueError) as context:
            vampire.set_virtue_by_name("invalid_virtue", 3)
        self.assertIn("Unknown virtue", str(context.exception))


class TestVampirePathIntegration(VampireModelTestCase):
    """Test Path of Enlightenment integration."""

    def test_path_updates_virtues_on_save(self):
        """Test that setting a path updates virtue booleans on save."""
        vampire = Vampire.objects.create(
            name="Test",
            owner=self.user,
            has_conviction=False,
            has_instinct=False,
            conscience=3,
            self_control=3,
        )
        self.assertFalse(vampire.has_conviction)
        self.assertFalse(vampire.has_instinct)

        vampire.path = self.path_of_caine
        vampire.save()
        vampire.refresh_from_db()

        self.assertTrue(vampire.has_conviction)
        self.assertTrue(vampire.has_instinct)
        # Original virtues should be reset
        self.assertEqual(vampire.conscience, 0)
        self.assertEqual(vampire.self_control, 0)


class TestVampireFreebies(VampireModelTestCase):
    """Test freebie point costs and methods."""

    def test_freebie_cost_discipline(self):
        """Test freebie cost for in-clan disciplines."""
        vampire = Vampire.objects.create(name="Test", owner=self.user)
        self.assertEqual(vampire.freebie_cost("discipline"), 7)

    def test_freebie_cost_out_of_clan_discipline(self):
        """Test freebie cost for out-of-clan disciplines."""
        vampire = Vampire.objects.create(name="Test", owner=self.user)
        self.assertEqual(vampire.freebie_cost("out_of_clan_discipline"), 10)

    def test_freebie_cost_virtue(self):
        """Test freebie cost for virtues."""
        vampire = Vampire.objects.create(name="Test", owner=self.user)
        self.assertEqual(vampire.freebie_cost("virtue"), 2)

    def test_freebie_cost_humanity(self):
        """Test freebie cost for humanity."""
        vampire = Vampire.objects.create(name="Test", owner=self.user)
        self.assertEqual(vampire.freebie_cost("humanity"), 1)

    def test_freebie_cost_path_rating(self):
        """Test freebie cost for path rating."""
        vampire = Vampire.objects.create(name="Test", owner=self.user)
        self.assertEqual(vampire.freebie_cost("path_rating"), 1)

    def test_freebie_costs_dict(self):
        """Test freebie_costs returns complete cost dictionary."""
        vampire = Vampire.objects.create(name="Test", owner=self.user)
        costs = vampire.freebie_costs()
        self.assertEqual(costs["discipline"], 7)
        self.assertEqual(costs["out_of_clan_discipline"], 10)
        self.assertEqual(costs["virtue"], 2)
        self.assertEqual(costs["humanity"], 1)
        self.assertEqual(costs["path_rating"], 1)

    def test_freebie_frequencies(self):
        """Test freebie_frequencies returns expected distribution."""
        vampire = Vampire.objects.create(name="Test", owner=self.user)
        freqs = vampire.freebie_frequencies()
        self.assertIn("discipline", freqs)
        self.assertIn("virtue", freqs)
        self.assertIn("humanity", freqs)
        self.assertIn("path_rating", freqs)


class TestVampireXPCosts(VampireModelTestCase):
    """Test XP costs for vampire traits."""

    def test_xp_cost_new_discipline(self):
        """Test XP cost for new discipline."""
        vampire = Vampire.objects.create(name="Test", owner=self.user)
        self.assertEqual(vampire.xp_cost("new_discipline"), 10)

    def test_xp_cost_clan_discipline(self):
        """Test XP cost for raising clan discipline."""
        vampire = Vampire.objects.create(name="Test", owner=self.user)
        # Cost is 5 * new rating
        self.assertEqual(vampire.xp_cost("clan_discipline", 3), 15)

    def test_xp_cost_out_of_clan_discipline(self):
        """Test XP cost for raising out-of-clan discipline."""
        vampire = Vampire.objects.create(name="Test", owner=self.user)
        # Cost is 7 * new rating
        self.assertEqual(vampire.xp_cost("out_of_clan_discipline", 3), 21)

    def test_xp_cost_virtue(self):
        """Test XP cost for virtue."""
        vampire = Vampire.objects.create(name="Test", owner=self.user)
        # Cost is 2 * new rating
        self.assertEqual(vampire.xp_cost("virtue", 4), 8)

    def test_xp_cost_humanity(self):
        """Test XP cost for humanity."""
        vampire = Vampire.objects.create(name="Test", owner=self.user)
        # Cost is 1 * new rating
        self.assertEqual(vampire.xp_cost("humanity", 8), 8)

    def test_xp_cost_path_rating(self):
        """Test XP cost for path rating."""
        vampire = Vampire.objects.create(name="Test", owner=self.user)
        # Cost is 1 * new rating
        self.assertEqual(vampire.xp_cost("path_rating", 5), 5)

    def test_xp_frequencies(self):
        """Test xp_frequencies returns expected distribution."""
        vampire = Vampire.objects.create(name="Test", owner=self.user)
        freqs = vampire.xp_frequencies()
        self.assertIn("discipline", freqs)
        self.assertIn("virtue", freqs)
        self.assertIn("humanity", freqs)
        self.assertIn("path_rating", freqs)


class TestVampireSireRelationship(VampireModelTestCase):
    """Test sire/childe relationship."""

    def test_vampire_can_have_sire(self):
        """Test that a vampire can have a sire."""
        sire = Vampire.objects.create(
            name="Elder Ventrue",
            owner=self.user,
            generation_rating=8,
        )
        childe = Vampire.objects.create(
            name="Neonate",
            owner=self.user,
            sire=sire,
            generation_rating=9,
        )
        self.assertEqual(childe.sire, sire)

    def test_sire_can_have_childer(self):
        """Test that childer relationship is accessible from sire."""
        sire = Vampire.objects.create(
            name="Elder",
            owner=self.user,
            generation_rating=8,
        )
        childe1 = Vampire.objects.create(
            name="Childe 1",
            owner=self.user,
            sire=sire,
        )
        childe2 = Vampire.objects.create(
            name="Childe 2",
            owner=self.user,
            sire=sire,
        )
        childer = list(sire.childer.all())
        self.assertEqual(len(childer), 2)
        self.assertIn(childe1, childer)
        self.assertIn(childe2, childer)


class TestVampireAllowedBackgrounds(VampireModelTestCase):
    """Test allowed backgrounds for vampires."""

    def test_allowed_backgrounds_includes_generation(self):
        """Test that allowed_backgrounds includes generation."""
        vampire = Vampire.objects.create(name="Test", owner=self.user)
        self.assertIn("generation", vampire.allowed_backgrounds)

    def test_allowed_backgrounds_includes_domain(self):
        """Test that allowed_backgrounds includes domain."""
        vampire = Vampire.objects.create(name="Test", owner=self.user)
        self.assertIn("domain", vampire.allowed_backgrounds)

    def test_allowed_backgrounds_includes_herd(self):
        """Test that allowed_backgrounds includes herd."""
        vampire = Vampire.objects.create(name="Test", owner=self.user)
        self.assertIn("herd", vampire.allowed_backgrounds)

    def test_allowed_backgrounds_includes_status(self):
        """Test that allowed_backgrounds includes status_background."""
        vampire = Vampire.objects.create(name="Test", owner=self.user)
        self.assertIn("status_background", vampire.allowed_backgrounds)


class TestVampireFreebieStep(VampireModelTestCase):
    """Test freebie_step configuration."""

    def test_vampire_freebie_step(self):
        """Test that vampires have freebie_step of 7."""
        vampire = Vampire.objects.create(name="Test", owner=self.user)
        self.assertEqual(vampire.freebie_step, 7)
