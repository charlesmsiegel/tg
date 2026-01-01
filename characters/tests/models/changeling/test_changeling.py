from characters.models.changeling.changeling import Changeling
from characters.models.changeling.house import House
from characters.models.changeling.kith import Kith
from characters.models.changeling.legacy import Legacy
from characters.tests.utils import changeling_setup
from django.contrib.auth.models import User
from django.test import TestCase
from game.models import Chronicle


class TestChangeling(TestCase):
    def setUp(self) -> None:
        self.player = User.objects.create_user(username="User1", password="12345")
        self.character = Changeling.objects.create(
            owner=self.player,
            name="Test Changeling",
        )
        changeling_setup()

    def test_set_seeming(self):
        self.assertFalse(self.character.has_seeming())
        c = Changeling.objects.create(owner=self.player, name="Childling")
        self.assertFalse(c.has_seeming())
        glamour = 4
        willpower = 4
        self.assertTrue(c.set_seeming("childling"))
        self.assertEqual(c.glamour, glamour + 1)
        self.assertTrue(c.has_seeming())
        c = Changeling.objects.create(owner=self.player, name="Wilder")
        self.assertFalse(c.has_seeming())
        glamour = 4
        willpower = 4
        self.assertTrue(c.set_seeming("wilder"))
        self.assertEqual(c.glamour + c.willpower, glamour + willpower + 1)
        c = Changeling.objects.create(owner=self.player, name="Grump")
        self.assertFalse(c.has_seeming())
        glamour = 4
        willpower = 4
        self.assertTrue(c.set_seeming("grump"))
        self.assertEqual(c.willpower, willpower + 1)

    def test_has_seeming(self):
        self.assertFalse(self.character.has_seeming())
        self.character.set_seeming("childling")
        self.assertTrue(self.character.has_seeming())

    def test_set_court(self):
        self.assertFalse(self.character.has_court())
        self.assertTrue(self.character.set_court("seelie"))
        self.assertTrue(self.character.has_court())

    def test_eligible_for_house(self):
        self.character.kith = Kith.objects.get(name="Kith 0")
        self.assertFalse(self.character.eligible_for_house())
        self.character.title = 1
        self.assertTrue(self.character.eligible_for_house())
        self.character.backgrounds.filter(bg__property_name="title").delete()
        self.assertFalse(self.character.eligible_for_house())
        self.character.kith = Kith.objects.create(name="Arcadian Sidhe")
        self.assertTrue(self.character.eligible_for_house())

    def test_eligible_for_house_no_kith(self):
        """Test eligible_for_house when character has no kith (uses title only)."""
        self.character.kith = None
        self.assertFalse(self.character.eligible_for_house())
        self.character.title = 1
        self.assertTrue(self.character.eligible_for_house())

    def test_has_house(self):
        self.character.title = 1
        self.character.court = "seelie"
        self.assertFalse(self.character.has_house())
        self.assertTrue(self.character.set_house(House.objects.get(name="House 0")))
        self.assertTrue(self.character.has_house())
        self.character.backgrounds.filter(bg__property_name="title").delete()
        self.assertFalse(self.character.has_house())
        self.character.house = None
        self.assertTrue(self.character.has_house())

    def test_set_house(self):
        self.assertTrue(self.character.has_house())
        self.assertFalse(self.character.set_house(House.objects.get(name="House 0")))
        self.character.title = 1
        self.character.court = "seelie"
        self.assertTrue(self.character.set_house(House.objects.get(name="House 0")))
        self.assertTrue(self.character.has_house())
        self.character.backgrounds.filter(bg__property_name="title").delete()
        self.assertFalse(self.character.has_house())
        self.character.kith = Kith.objects.create(name="Arcadian Sidhe")
        self.assertTrue(self.character.set_house(House.objects.get(name="House 0")))
        self.assertTrue(self.character.has_house())
        self.character.court = "unseelie"
        self.assertFalse(self.character.set_house(House.objects.get(name="House 0")))

    def test_has_court(self):
        self.assertFalse(self.character.has_court())
        self.character.set_court("seelie")
        self.assertTrue(self.character.has_court())

    def test_has_kith(self):
        self.assertFalse(self.character.has_kith())
        self.character.set_kith(Kith.objects.get(name="Kith 0"))
        self.assertTrue(self.character.has_kith())

    def test_set_kith(self):
        self.assertFalse(self.character.has_kith())
        self.assertTrue(self.character.set_kith(Kith.objects.get(name="Kith 0")))
        self.assertTrue(self.character.has_kith())

    def test_set_seelie_legacy(self):
        seelie = Legacy.objects.get(name="Legacy 0")
        unseelie = Legacy.objects.get(name="Legacy 1")
        self.assertFalse(self.character.has_seelie_legacy())
        self.assertFalse(self.character.set_seelie_legacy(unseelie))
        self.assertFalse(self.character.has_seelie_legacy())
        self.assertTrue(self.character.set_seelie_legacy(seelie))
        self.assertTrue(self.character.has_seelie_legacy())

    def test_has_seelie_legacy(self):
        legacy = Legacy.objects.get(name="Legacy 0")
        self.assertFalse(self.character.has_seelie_legacy())
        self.assertTrue(self.character.set_seelie_legacy(legacy))
        self.assertTrue(self.character.has_seelie_legacy())

    def test_set_unseelie_legacy(self):
        seelie = Legacy.objects.get(name="Legacy 0")
        unseelie = Legacy.objects.get(name="Legacy 1")
        self.assertFalse(self.character.has_unseelie_legacy())
        self.assertFalse(self.character.set_unseelie_legacy(seelie))
        self.assertFalse(self.character.has_unseelie_legacy())
        self.assertTrue(self.character.set_unseelie_legacy(unseelie))
        self.assertTrue(self.character.has_unseelie_legacy())

    def test_has_unseelie_legacy(self):
        legacy = Legacy.objects.get(name="Legacy 1")
        self.assertFalse(self.character.has_unseelie_legacy())
        self.assertTrue(self.character.set_unseelie_legacy(legacy))
        self.assertTrue(self.character.has_unseelie_legacy())

    def test_add_art(self):
        self.character.wayfare = 0
        self.assertTrue(self.character.add_art("wayfare"))
        self.assertEqual(self.character.wayfare, 1)

    def test_add_art_at_max(self):
        """Test that add_art fails when art is already at maximum (5)."""
        self.character.wayfare = 5
        self.assertFalse(self.character.add_art("wayfare"))
        self.assertEqual(self.character.wayfare, 5)

    def test_get_arts(self):
        self.assertEqual(
            self.character.get_arts(),
            {
                "autumn": 0,
                "chicanery": 0,
                "chronos": 0,
                "contract": 0,
                "dragons_ire": 0,
                "legerdemain": 0,
                "metamorphosis": 0,
                "naming": 0,
                "oneiromancy": 0,
                "primal": 0,
                "pyretics": 0,
                "skycraft": 0,
                "soothsay": 0,
                "sovereign": 0,
                "spring": 0,
                "summer": 0,
                "wayfare": 0,
                "winter": 0,
            },
        )
        self.character.add_art("naming")
        self.character.add_art("naming")
        self.character.add_art("naming")
        self.character.add_art("wayfare")
        self.character.add_art("wayfare")
        self.character.add_art("pyretics")
        self.character.add_art("legerdemain")
        self.assertEqual(
            self.character.get_arts(),
            {
                "autumn": 0,
                "chicanery": 0,
                "chronos": 0,
                "contract": 0,
                "dragons_ire": 0,
                "legerdemain": 1,
                "metamorphosis": 0,
                "naming": 3,
                "oneiromancy": 0,
                "primal": 0,
                "pyretics": 1,
                "skycraft": 0,
                "soothsay": 0,
                "sovereign": 0,
                "spring": 0,
                "summer": 0,
                "wayfare": 2,
                "winter": 0,
            },
        )

    def test_has_arts(self):
        self.assertFalse(self.character.has_arts())
        self.character.add_art("naming")
        self.assertFalse(self.character.has_arts())
        self.character.add_art("naming")
        self.assertFalse(self.character.has_arts())
        self.character.add_art("naming")
        self.assertTrue(self.character.has_arts())

    def test_total_arts(self):
        self.assertEqual(self.character.total_arts(), 0)
        self.character.add_art("naming")
        self.assertEqual(self.character.total_arts(), 1)
        self.character.add_art("soothsay")
        self.assertEqual(self.character.total_arts(), 2)
        self.character.add_art("chronos")
        self.assertEqual(self.character.total_arts(), 3)

    def test_filter_arts(self):
        self.character.autumn = 0
        self.character.pyretics = 0
        self.character.chicanery = 1
        self.character.primal = 1
        self.character.skycraft = 1
        self.character.chronos = 2
        self.character.oneiromancy = 2
        self.character.soothsay = 2
        self.character.contract = 3
        self.character.naming = 3
        self.character.winter = 3
        self.character.sovereign = 3
        self.character.dragons_ire = 4
        self.character.spring = 4
        self.character.wayfare = 4
        self.character.metamorphosis = 4
        self.character.legerdemain = 5
        self.character.summer = 5
        self.assertEqual(len(self.character.filter_arts(minimum=0, maximum=5)), 18)
        self.assertEqual(len(self.character.filter_arts(minimum=1, maximum=5)), 16)
        self.assertEqual(len(self.character.filter_arts(minimum=2, maximum=5)), 13)
        self.assertEqual(len(self.character.filter_arts(minimum=3, maximum=5)), 10)
        self.assertEqual(len(self.character.filter_arts(minimum=4, maximum=5)), 6)
        self.assertEqual(len(self.character.filter_arts(minimum=5, maximum=5)), 2)
        self.assertEqual(len(self.character.filter_arts(minimum=0, maximum=4)), 16)
        self.assertEqual(len(self.character.filter_arts(minimum=0, maximum=3)), 12)
        self.assertEqual(len(self.character.filter_arts(minimum=0, maximum=2)), 8)
        self.assertEqual(len(self.character.filter_arts(minimum=0, maximum=1)), 5)
        self.assertEqual(len(self.character.filter_arts(minimum=0, maximum=0)), 2)

    def test_add_realm(self):
        self.character.actor = 0
        self.assertTrue(self.character.add_realm("actor"))
        self.assertEqual(self.character.actor, 1)

    def test_add_realm_at_max(self):
        """Test that add_realm fails when realm is already at maximum (5)."""
        self.character.actor = 5
        self.assertFalse(self.character.add_realm("actor"))
        self.assertEqual(self.character.actor, 5)

    def test_get_realms(self):
        self.assertEqual(
            self.character.get_realms(),
            {
                "actor": 0,
                "fae": 0,
                "nature_realm": 0,
                "prop": 0,
                "scene": 0,
                "time": 0,
            },
        )
        self.character.add_realm("actor")
        self.character.add_realm("actor")
        self.character.add_realm("actor")
        self.character.add_realm("nature_realm")
        self.character.add_realm("nature_realm")
        self.character.add_realm("scene")
        self.character.add_realm("time")
        self.assertEqual(
            self.character.get_realms(),
            {
                "actor": 3,
                "fae": 0,
                "nature_realm": 2,
                "prop": 0,
                "scene": 1,
                "time": 1,
            },
        )

    def test_has_realms(self):
        self.assertFalse(self.character.has_realms())
        self.character.add_realm("actor")
        self.assertFalse(self.character.has_realms())
        self.character.add_realm("actor")
        self.assertFalse(self.character.has_realms())
        self.character.add_realm("actor")
        self.assertFalse(self.character.has_realms())
        self.character.add_realm("fae")
        self.assertFalse(self.character.has_realms())
        self.character.add_realm("fae")
        self.assertTrue(self.character.has_realms())

    def test_total_realms(self):
        self.assertEqual(self.character.total_realms(), 0)
        self.character.add_realm("actor")
        self.assertEqual(self.character.total_realms(), 1)
        self.character.add_realm("time")
        self.assertEqual(self.character.total_realms(), 2)
        self.character.add_realm("fae")
        self.assertEqual(self.character.total_realms(), 3)

    def test_filter_realms(self):
        self.character.actor = 0
        self.character.fae = 1
        self.character.nature_realm = 2
        self.character.prop = 3
        self.character.scene = 4
        self.character.time = 5
        self.assertEqual(len(self.character.filter_realms(minimum=0, maximum=5)), 6)
        self.assertEqual(len(self.character.filter_realms(minimum=1, maximum=5)), 5)
        self.assertEqual(len(self.character.filter_realms(minimum=2, maximum=5)), 4)
        self.assertEqual(len(self.character.filter_realms(minimum=3, maximum=5)), 3)
        self.assertEqual(len(self.character.filter_realms(minimum=4, maximum=5)), 2)
        self.assertEqual(len(self.character.filter_realms(minimum=5, maximum=5)), 1)
        self.assertEqual(len(self.character.filter_realms(minimum=0, maximum=4)), 5)
        self.assertEqual(len(self.character.filter_realms(minimum=0, maximum=3)), 4)
        self.assertEqual(len(self.character.filter_realms(minimum=0, maximum=2)), 3)
        self.assertEqual(len(self.character.filter_realms(minimum=0, maximum=1)), 2)
        self.assertEqual(len(self.character.filter_realms(minimum=0, maximum=0)), 1)

    def test_set_musing_threshold(self):
        self.assertFalse(self.character.has_musing_threshold())
        self.assertTrue(self.character.set_musing_threshold("Inspire Creativity"))
        self.assertTrue(self.character.has_musing_threshold())

    def test_has_musing_threshold(self):
        self.assertFalse(self.character.has_musing_threshold())
        self.character.set_musing_threshold("Inspire Creativity")
        self.assertTrue(self.character.has_musing_threshold())

    def test_set_ravaging_threshold(self):
        self.assertFalse(self.character.has_ravaging_threshold())
        self.assertTrue(self.character.set_ravaging_threshold("Exhaust Creativity"))
        self.assertTrue(self.character.has_ravaging_threshold())

    def test_has_ravaging_threshold(self):
        self.assertFalse(self.character.has_ravaging_threshold())
        self.character.set_ravaging_threshold("Exhaust Creativity")
        self.assertTrue(self.character.has_ravaging_threshold())

    def test_set_antithesis(self):
        self.assertFalse(self.character.has_antithesis())
        self.assertTrue(self.character.set_antithesis("Antithesis"))
        self.assertTrue(self.character.has_antithesis())

    def test_has_antithesis(self):
        self.assertFalse(self.character.has_antithesis())
        self.character.set_antithesis("Antithesis")
        self.assertTrue(self.character.has_antithesis())

    def test_add_glamour(self):
        g = self.character.glamour
        self.assertTrue(self.character.add_glamour())
        self.assertEqual(self.character.glamour, g + 1)

    def test_add_glamour_at_max(self):
        """Test that add_glamour fails when glamour is at maximum (10)."""
        self.character.glamour = 10
        self.assertFalse(self.character.add_glamour())
        self.assertEqual(self.character.glamour, 10)

    def test_add_banality(self):
        b = self.character.banality
        self.assertTrue(self.character.add_banality())
        self.assertEqual(self.character.banality, b + 1)

    def test_add_banality_at_max(self):
        """Test that add_banality fails when banality is at maximum (10)."""
        self.character.banality = 10
        self.assertFalse(self.character.add_banality())
        self.assertEqual(self.character.banality, 10)

    def test_birthright_corrections(self):
        piskey = Kith.objects.create(name="Piskey")
        satyr = Kith.objects.create(name="Satyr")
        troll = Kith.objects.create(name="Troll")
        autumn_sidhe = Kith.objects.create(name="Autumn Sidhe")
        arcadian_sidhe = Kith.objects.create(name="Arcadian Sidhe")
        char1 = Changeling.objects.create(owner=self.player, name="Char 1", kith=piskey)
        char2 = Changeling.objects.create(owner=self.player, name="Char 2", kith=satyr)
        char3 = Changeling.objects.create(owner=self.player, name="Char 3", kith=troll)
        char4 = Changeling.objects.create(owner=self.player, name="Char 4", kith=autumn_sidhe)
        char5 = Changeling.objects.create(owner=self.player, name="Char 5", kith=arcadian_sidhe)
        char1.birthright_correction()
        char2.birthright_correction()
        char3.birthright_correction()
        char4.birthright_correction()
        char5.birthright_correction()
        self.assertEqual(char1.dexterity, 2)
        self.assertEqual(char2.stamina, 2)
        self.assertEqual(char3.strength, 2)
        self.assertEqual(char3.max_health_levels, 8)
        self.assertEqual(char4.appearance, 3)
        self.assertEqual(char5.appearance, 3)

    def test_has_changeling_history(self):
        self.assertFalse(self.character.has_changeling_history())
        self.character.true_name = "Faerie Name"
        self.assertFalse(self.character.has_changeling_history())
        self.character.crysalis = "It Happened"
        self.assertTrue(self.character.has_changeling_history())

    def test_has_changeling_appearance(self):
        self.assertFalse(self.character.has_changeling_appearance())
        self.character.fae_mien = "Magical"
        self.assertTrue(self.character.has_changeling_appearance())

    def test_set_changeling_appearance(self):
        fae_mien = "Beautiful butterfly wings"
        self.character.set_changeling_appearance(fae_mien)
        self.assertEqual(self.character.fae_mien, fae_mien)
        self.assertTrue(self.character.has_changeling_appearance())

    def test_set_changeling_history(self):
        true_name = "John Doe"
        date_ennobled = "01/01/2000"
        crysalis = "A cocoon"
        date_of_crysalis = "01/02/2000"
        self.character.set_changeling_history(true_name, date_ennobled, crysalis, date_of_crysalis)
        self.assertEqual(self.character.true_name, true_name)
        self.assertEqual(self.character.date_ennobled, date_ennobled)
        self.assertEqual(self.character.crysalis, crysalis)
        self.assertEqual(self.character.date_of_crysalis, date_of_crysalis)
        self.assertTrue(self.character.has_changeling_history())


class TestChangelingXPMethods(TestCase):
    """Tests for XP spending methods on Changeling model."""

    def setUp(self):
        self.player = User.objects.create_user(username="User1", password="12345")
        self.character = Changeling.objects.create(
            owner=self.player,
            name="Test Changeling",
            xp=100,  # Give enough XP to test spending
        )
        changeling_setup()

    def test_xp_frequencies(self):
        """Test that xp_frequencies returns correct distribution."""
        frequencies = self.character.xp_frequencies()
        self.assertIn("art", frequencies)
        self.assertIn("realm", frequencies)
        self.assertIn("glamour", frequencies)
        self.assertIn("banality", frequencies)
        self.assertEqual(frequencies["art"], 30)
        self.assertEqual(frequencies["realm"], 15)
        self.assertEqual(frequencies["glamour"], 3)
        self.assertEqual(frequencies["banality"], 1)

    def test_xp_cost_art(self):
        """Test XP cost calculation for arts."""
        self.assertEqual(self.character.xp_cost("art", 1), 8)
        self.assertEqual(self.character.xp_cost("art", 2), 16)
        self.assertEqual(self.character.xp_cost("art", 3), 24)
        # Test without value
        self.assertEqual(self.character.xp_cost("art"), 8)

    def test_xp_cost_realm(self):
        """Test XP cost calculation for realms."""
        self.assertEqual(self.character.xp_cost("realm", 1), 5)
        self.assertEqual(self.character.xp_cost("realm", 2), 10)
        self.assertEqual(self.character.xp_cost("realm", 3), 15)
        # Test without value
        self.assertEqual(self.character.xp_cost("realm"), 5)

    def test_xp_cost_glamour(self):
        """Test XP cost calculation for glamour."""
        self.assertEqual(self.character.xp_cost("glamour", 5), 15)
        self.assertEqual(self.character.xp_cost("glamour", 6), 18)
        # Test without value
        self.assertEqual(self.character.xp_cost("glamour"), 3)

    def test_xp_cost_banality(self):
        """Test XP cost calculation for banality."""
        self.assertEqual(self.character.xp_cost("banality", 4), 8)
        self.assertEqual(self.character.xp_cost("banality", 5), 10)
        # Test without value
        self.assertEqual(self.character.xp_cost("banality"), 2)

    def test_spend_xp_unknown_trait(self):
        """Test spending XP on unknown trait returns trait name."""
        result = self.character.spend_xp("unknown_trait")
        self.assertEqual(result, "unknown_trait")


class TestChangelingFreebieMethods(TestCase):
    """Tests for freebie spending methods on Changeling model."""

    def setUp(self):
        self.player = User.objects.create_user(username="User1", password="12345")
        self.character = Changeling.objects.create(
            owner=self.player,
            name="Test Changeling",
            freebies=50,  # Give enough freebies to test spending
        )
        changeling_setup()

    def test_freebie_frequencies(self):
        """Test that freebie_frequencies returns correct distribution."""
        frequencies = self.character.freebie_frequencies()
        self.assertIn("art", frequencies)
        self.assertIn("realm", frequencies)
        self.assertIn("glamour", frequencies)
        self.assertIn("banality", frequencies)
        self.assertEqual(frequencies["art"], 25)
        self.assertEqual(frequencies["realm"], 15)
        self.assertEqual(frequencies["glamour"], 5)
        self.assertEqual(frequencies["banality"], 1)

    def test_freebie_costs(self):
        """Test that freebie_costs returns correct costs."""
        costs = self.character.freebie_costs()
        self.assertIn("art", costs)
        self.assertIn("realm", costs)
        self.assertIn("glamour", costs)
        self.assertIn("banality", costs)
        self.assertEqual(costs["art"], 5)
        self.assertEqual(costs["realm"], 3)
        self.assertEqual(costs["glamour"], 3)
        self.assertEqual(costs["banality"], 2)

    def test_freebie_cost_art(self):
        """Test freebie cost for arts."""
        self.assertEqual(self.character.freebie_cost("art"), 5)

    def test_freebie_cost_realm(self):
        """Test freebie cost for realms."""
        self.assertEqual(self.character.freebie_cost("realm"), 3)

    def test_freebie_cost_glamour(self):
        """Test freebie cost for glamour."""
        self.assertEqual(self.character.freebie_cost("glamour"), 3)

    def test_freebie_cost_banality(self):
        """Test freebie cost for banality."""
        self.assertEqual(self.character.freebie_cost("banality"), 2)

    def test_spend_freebies_unknown_trait(self):
        """Test spending freebies on unknown trait returns trait name."""
        result = self.character.spend_freebies("unknown_trait")
        self.assertEqual(result, "unknown_trait")


class TestChangelingDetailView(TestCase):
    def setUp(self) -> None:
        self.player = User.objects.create_user(username="User1", password="12345")
        self.changeling = Changeling.objects.create(
            name="Test Changeling",
            owner=self.player,
            status="App",
        )
        self.url = self.changeling.get_absolute_url()

    def test_changeling_detail_view_status_code(self):
        self.client.login(username="User1", password="12345")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_changeling_detail_view_templates(self):
        self.client.login(username="User1", password="12345")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/changeling/changeling/detail.html")


class TestChangelingCreateView(TestCase):
    def setUp(self):
        self.st = User.objects.create_user(username="ST", password="password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.chronicle.storytellers.add(self.st)
        self.valid_data = {
            "name": "Changeling",
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
            "treasure": 1,
            "court": "seelie",
            "seeming": "grump",
            "autumn": 0,
            "chicanery": 0,
            "chronos": 1,
            "contract": 1,
            "dragons_ire": 1,
            "legerdemain": 1,
            "metamorphosis": 1,
            "naming": 1,
            "oneiromancy": 1,
            "primal": 1,
            "pyretics": 1,
            "skycraft": 1,
            "soothsay": 1,
            "sovereign": 1,
            "spring": 1,
            "summer": 1,
            "wayfare": 1,
            "winter": 1,
            "actor": 1,
            "fae": 1,
            "nature_realm": 1,
            "prop": 1,
            "scene": 1,
            "time": 1,
            "banality": 1,
            "glamour": 1,
            "musing_threshold": "create_love",
            "ravaging_threshold": "create_anger",
            "antithesis": "anti-this",
            "true_name": "Bob",
            "date_ennobled": "2024-08-01",
            "crysalis": "Ya",
            "date_of_crysalis": "2024-07-30",
            "fae_mien": "Blue",
        }
        self.url = Changeling.get_creation_url()

    def test_create_view_status_code(self):
        self.client.login(username="ST", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        self.client.login(username="ST", password="password")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/changeling/changeling/basics.html")

    def test_create_view_successful_post(self):
        # Test basic creation with name only - the basics form
        self.client.login(username="ST", password="password")
        response = self.client.post(self.url, data={"name": "Test Changeling"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Changeling.objects.count(), 1)
        self.assertEqual(Changeling.objects.first().name, "Test Changeling")


class TestChangelingUpdateView(TestCase):
    def setUp(self):
        self.st = User.objects.create_user(username="ST", password="password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.chronicle.storytellers.add(self.st)
        self.changeling = Changeling.objects.create(
            name="Test Changeling",
            owner=self.st,
            chronicle=self.chronicle,
            description="Test description",
        )
        self.valid_data = {
            "name": "Changeling Updated",
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
            "court": "seelie",
            "seeming": "grump",
            "autumn": 0,
            "chicanery": 0,
            "chronos": 1,
            "contract": 1,
            "dragons_ire": 1,
            "legerdemain": 1,
            "metamorphosis": 1,
            "naming": 1,
            "oneiromancy": 1,
            "primal": 1,
            "pyretics": 1,
            "skycraft": 1,
            "soothsay": 1,
            "sovereign": 1,
            "spring": 1,
            "summer": 1,
            "wayfare": 1,
            "winter": 1,
            "actor": 1,
            "fae": 1,
            "nature_realm": 1,
            "prop": 1,
            "scene": 1,
            "time": 1,
            "banality": 1,
            "glamour": 1,
            "musing_threshold": "create_love",
            "ravaging_threshold": "create_anger",
            "antithesis": "anti-this",
            "true_name": "Bob",
            "date_ennobled": "2024-08-01",
            "crysalis": "Ya",
            "date_of_crysalis": "2024-07-30",
            "fae_mien": "Blue",
        }
        self.url = self.changeling.get_update_url()

    def test_update_view_status_code(self):
        self.client.login(username="ST", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        self.client.login(username="ST", password="password")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/changeling/changeling/form.html")

    def test_update_view_successful_post(self):
        self.client.login(username="ST", password="password")
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.changeling.refresh_from_db()
        self.assertEqual(self.changeling.name, "Changeling Updated")
        self.assertEqual(self.changeling.description, "Test")


class TestChangelingSpendXP(TestCase):
    """Comprehensive tests for XP spending on Changeling-specific traits."""

    def setUp(self):
        self.player = User.objects.create_user(username="User1", password="12345")
        self.character = Changeling.objects.create(
            owner=self.player,
            name="Test Changeling",
            xp=200,  # Enough XP for all tests
        )
        changeling_setup()

    def test_spend_xp_on_art_success(self):
        """Test spending XP to increase an art."""
        self.character.wayfare = 1
        initial_xp = self.character.xp
        result = self.character.spend_xp("wayfare")
        self.assertTrue(result)
        self.assertEqual(self.character.wayfare, 2)
        # Cost should be 8 * new_value (2) = 16
        self.assertEqual(self.character.xp, initial_xp - 16)

    def test_spend_xp_on_art_at_max(self):
        """Test spending XP on art that is at maximum fails."""
        self.character.wayfare = 5
        result = self.character.spend_xp("wayfare")
        self.assertFalse(result)
        self.assertEqual(self.character.wayfare, 5)

    def test_spend_xp_on_art_insufficient_xp(self):
        """Test spending XP on art when insufficient XP fails."""
        self.character.xp = 1  # Not enough
        self.character.wayfare = 2
        result = self.character.spend_xp("wayfare")
        self.assertFalse(result)
        self.assertEqual(self.character.wayfare, 2)

    def test_spend_xp_on_realm_success(self):
        """Test spending XP to increase a realm."""
        self.character.actor = 1
        initial_xp = self.character.xp
        result = self.character.spend_xp("actor")
        self.assertTrue(result)
        self.assertEqual(self.character.actor, 2)
        # Cost should be 5 * new_value (2) = 10
        self.assertEqual(self.character.xp, initial_xp - 10)

    def test_spend_xp_on_realm_at_max(self):
        """Test spending XP on realm that is at maximum fails."""
        self.character.actor = 5
        result = self.character.spend_xp("actor")
        self.assertFalse(result)
        self.assertEqual(self.character.actor, 5)

    def test_spend_xp_on_realm_insufficient_xp(self):
        """Test spending XP on realm when insufficient XP fails."""
        self.character.xp = 1  # Not enough
        self.character.actor = 2
        result = self.character.spend_xp("actor")
        self.assertFalse(result)
        self.assertEqual(self.character.actor, 2)

    def test_spend_xp_on_glamour_success(self):
        """Test spending XP to increase glamour."""
        self.character.glamour = 5
        initial_xp = self.character.xp
        result = self.character.spend_xp("glamour")
        self.assertTrue(result)
        self.assertEqual(self.character.glamour, 6)
        # Cost should be 3 * new_value (6) = 18
        self.assertEqual(self.character.xp, initial_xp - 18)

    def test_spend_xp_on_glamour_at_max(self):
        """Test spending XP on glamour at maximum fails."""
        self.character.glamour = 10
        result = self.character.spend_xp("glamour")
        self.assertFalse(result)
        self.assertEqual(self.character.glamour, 10)

    def test_spend_xp_on_glamour_insufficient_xp(self):
        """Test spending XP on glamour when insufficient XP fails."""
        self.character.xp = 1  # Not enough
        self.character.glamour = 5
        result = self.character.spend_xp("glamour")
        self.assertFalse(result)
        self.assertEqual(self.character.glamour, 5)

    def test_spend_xp_on_banality_success(self):
        """Test spending XP to increase banality."""
        self.character.banality = 4
        initial_xp = self.character.xp
        result = self.character.spend_xp("banality")
        self.assertTrue(result)
        self.assertEqual(self.character.banality, 5)
        # Cost should be 2 * new_value (5) = 10
        self.assertEqual(self.character.xp, initial_xp - 10)

    def test_spend_xp_on_banality_at_max(self):
        """Test spending XP on banality at maximum fails."""
        self.character.banality = 10
        result = self.character.spend_xp("banality")
        self.assertFalse(result)
        self.assertEqual(self.character.banality, 10)

    def test_spend_xp_on_banality_insufficient_xp(self):
        """Test spending XP on banality when insufficient XP fails."""
        self.character.xp = 1  # Not enough
        self.character.banality = 5
        result = self.character.spend_xp("banality")
        self.assertFalse(result)
        self.assertEqual(self.character.banality, 5)

    def test_spend_xp_on_different_arts(self):
        """Test spending XP on multiple different arts."""
        self.character.chicanery = 0
        self.character.primal = 0
        self.character.soothsay = 0

        result1 = self.character.spend_xp("chicanery")
        result2 = self.character.spend_xp("primal")
        result3 = self.character.spend_xp("soothsay")

        self.assertTrue(result1)
        self.assertTrue(result2)
        self.assertTrue(result3)
        self.assertEqual(self.character.chicanery, 1)
        self.assertEqual(self.character.primal, 1)
        self.assertEqual(self.character.soothsay, 1)

    def test_spend_xp_on_different_realms(self):
        """Test spending XP on multiple different realms."""
        self.character.fae = 0
        self.character.prop = 0
        self.character.scene = 0

        result1 = self.character.spend_xp("fae")
        result2 = self.character.spend_xp("prop")
        result3 = self.character.spend_xp("scene")

        self.assertTrue(result1)
        self.assertTrue(result2)
        self.assertTrue(result3)
        self.assertEqual(self.character.fae, 1)
        self.assertEqual(self.character.prop, 1)
        self.assertEqual(self.character.scene, 1)


class TestChangelingSpendFreebies(TestCase):
    """Comprehensive tests for freebie spending on Changeling-specific traits."""

    def setUp(self):
        self.player = User.objects.create_user(username="User1", password="12345")
        self.character = Changeling.objects.create(
            owner=self.player,
            name="Test Changeling",
            freebies=100,  # Enough freebies for all tests
        )
        changeling_setup()

    def test_spend_freebies_on_art_success(self):
        """Test spending freebies to increase an art."""
        self.character.wayfare = 1
        initial_freebies = self.character.freebies
        result = self.character.spend_freebies("wayfare")
        self.assertTrue(result)
        self.assertEqual(self.character.wayfare, 2)
        # Art cost is 5 freebies
        self.assertEqual(self.character.freebies, initial_freebies - 5)

    def test_spend_freebies_on_art_at_max(self):
        """Test spending freebies on art at maximum fails."""
        self.character.wayfare = 5
        result = self.character.spend_freebies("wayfare")
        self.assertFalse(result)
        self.assertEqual(self.character.wayfare, 5)

    def test_spend_freebies_on_art_insufficient_freebies(self):
        """Test spending freebies on art when insufficient freebies fails."""
        self.character.freebies = 1  # Not enough
        self.character.wayfare = 2
        result = self.character.spend_freebies("wayfare")
        self.assertFalse(result)
        self.assertEqual(self.character.wayfare, 2)

    def test_spend_freebies_on_realm_success(self):
        """Test spending freebies to increase a realm."""
        self.character.actor = 1
        initial_freebies = self.character.freebies
        result = self.character.spend_freebies("actor")
        self.assertTrue(result)
        self.assertEqual(self.character.actor, 2)
        # Realm cost is 3 freebies
        self.assertEqual(self.character.freebies, initial_freebies - 3)

    def test_spend_freebies_on_realm_at_max(self):
        """Test spending freebies on realm at maximum fails."""
        self.character.actor = 5
        result = self.character.spend_freebies("actor")
        self.assertFalse(result)
        self.assertEqual(self.character.actor, 5)

    def test_spend_freebies_on_realm_insufficient_freebies(self):
        """Test spending freebies on realm when insufficient freebies fails."""
        self.character.freebies = 1  # Not enough
        self.character.actor = 2
        result = self.character.spend_freebies("actor")
        self.assertFalse(result)
        self.assertEqual(self.character.actor, 2)

    def test_spend_freebies_on_glamour_success(self):
        """Test spending freebies to increase glamour."""
        self.character.glamour = 5
        initial_freebies = self.character.freebies
        result = self.character.spend_freebies("glamour")
        self.assertTrue(result)
        self.assertEqual(self.character.glamour, 6)
        # Glamour cost is 3 freebies
        self.assertEqual(self.character.freebies, initial_freebies - 3)

    def test_spend_freebies_on_glamour_at_max(self):
        """Test spending freebies on glamour at maximum fails."""
        self.character.glamour = 10
        result = self.character.spend_freebies("glamour")
        self.assertFalse(result)
        self.assertEqual(self.character.glamour, 10)

    def test_spend_freebies_on_glamour_insufficient_freebies(self):
        """Test spending freebies on glamour when insufficient freebies fails."""
        self.character.freebies = 1  # Not enough
        self.character.glamour = 5
        result = self.character.spend_freebies("glamour")
        self.assertFalse(result)
        self.assertEqual(self.character.glamour, 5)

    def test_spend_freebies_on_banality_success(self):
        """Test spending freebies to decrease banality."""
        self.character.banality = 4
        initial_freebies = self.character.freebies
        result = self.character.spend_freebies("banality")
        self.assertTrue(result)
        self.assertEqual(self.character.banality, 5)
        # Banality cost is 2 freebies
        self.assertEqual(self.character.freebies, initial_freebies - 2)

    def test_spend_freebies_on_banality_at_max(self):
        """Test spending freebies on banality at maximum fails."""
        self.character.banality = 10
        result = self.character.spend_freebies("banality")
        self.assertFalse(result)
        self.assertEqual(self.character.banality, 10)

    def test_spend_freebies_on_banality_insufficient_freebies(self):
        """Test spending freebies on banality when insufficient freebies fails."""
        self.character.freebies = 1  # Not enough
        self.character.banality = 5
        result = self.character.spend_freebies("banality")
        self.assertFalse(result)
        self.assertEqual(self.character.banality, 5)

    def test_spend_freebies_on_different_arts(self):
        """Test spending freebies on multiple different arts."""
        self.character.chicanery = 0
        self.character.primal = 0
        self.character.soothsay = 0

        result1 = self.character.spend_freebies("chicanery")
        result2 = self.character.spend_freebies("primal")
        result3 = self.character.spend_freebies("soothsay")

        self.assertTrue(result1)
        self.assertTrue(result2)
        self.assertTrue(result3)
        self.assertEqual(self.character.chicanery, 1)
        self.assertEqual(self.character.primal, 1)
        self.assertEqual(self.character.soothsay, 1)

    def test_spend_freebies_on_different_realms(self):
        """Test spending freebies on multiple different realms."""
        self.character.fae = 0
        self.character.prop = 0
        self.character.scene = 0

        result1 = self.character.spend_freebies("fae")
        result2 = self.character.spend_freebies("prop")
        result3 = self.character.spend_freebies("scene")

        self.assertTrue(result1)
        self.assertTrue(result2)
        self.assertTrue(result3)
        self.assertEqual(self.character.fae, 1)
        self.assertEqual(self.character.prop, 1)
        self.assertEqual(self.character.scene, 1)


class TestChangelingDetailViewContext(TestCase):
    """Test the context data passed to the Changeling detail view."""

    def setUp(self):
        self.player = User.objects.create_user(username="User1", password="12345")
        changeling_setup()
        self.kith = Kith.objects.first()
        self.house = House.objects.filter(court="seelie").first()
        self.seelie_legacy = Legacy.objects.filter(court="seelie").first()
        self.unseelie_legacy = Legacy.objects.filter(court="unseelie").first()
        self.changeling = Changeling.objects.create(
            name="Test Changeling",
            owner=self.player,
            status="App",
            kith=self.kith,
            house=self.house,
            seelie_legacy=self.seelie_legacy,
            unseelie_legacy=self.unseelie_legacy,
            court="seelie",
            seeming="wilder",
            wayfare=3,
            actor=2,
            glamour=6,
            banality=4,
        )
        self.url = self.changeling.get_absolute_url()

    def test_detail_view_context_has_specialties(self):
        """Test that the detail view context includes specialty data."""
        self.client.login(username="User1", password="12345")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        # Check that specialty context keys exist
        self.assertIn("strength_spec", response.context)

    def test_detail_view_context_has_merits_and_flaws(self):
        """Test that the detail view context includes merits and flaws."""
        self.client.login(username="User1", password="12345")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("merits_and_flaws", response.context)


class TestChangelingBasicsView(TestCase):
    """Tests for the ChangelingBasicsView."""

    def setUp(self):
        self.player = User.objects.create_user(username="User1", password="12345")
        self.st = User.objects.create_user(username="ST", password="12345")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.chronicle.storytellers.add(self.st)

    def test_basics_view_requires_login(self):
        """Test that the basics view requires login."""
        response = self.client.get(Changeling.get_creation_url())
        # App returns 401 for unauthenticated users instead of redirect
        self.assertEqual(response.status_code, 401)

    def test_basics_view_logged_in(self):
        """Test that logged in users can access the basics view."""
        self.client.login(username="User1", password="12345")
        response = self.client.get(Changeling.get_creation_url())
        self.assertEqual(response.status_code, 200)

    def test_basics_view_shows_storyteller_context_for_st(self):
        """Test that storyteller context is True for storytellers."""
        self.client.login(username="ST", password="12345")
        response = self.client.get(Changeling.get_creation_url())
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["storyteller"])

    def test_basics_view_shows_storyteller_context_for_player(self):
        """Test that storyteller context is False for regular players."""
        self.client.login(username="User1", password="12345")
        response = self.client.get(Changeling.get_creation_url())
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["storyteller"])

    def test_basics_view_form_invalid(self):
        """Test that form invalid returns proper error message."""
        self.client.login(username="User1", password="12345")
        # Post with empty name (invalid)
        response = self.client.post(Changeling.get_creation_url(), data={"name": ""})
        self.assertEqual(response.status_code, 200)  # Form error, stay on page


class TestChangelingArtsRealmsValidation(TestCase):
    """Tests for arts and realms validation during character creation."""

    def setUp(self):
        self.st = User.objects.create_user(username="ST", password="password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.chronicle.storytellers.add(self.st)
        changeling_setup()
        self.changeling = Changeling.objects.create(
            name="Test Changeling",
            owner=self.st,
            chronicle=self.chronicle,
            creation_status=4,  # At arts/realms step
        )

    def test_arts_must_total_three(self):
        """Test that arts must total exactly 3 dots."""
        self.client.login(username="ST", password="password")
        # Post with arts totaling 5, not 3
        data = {
            "autumn": 2,
            "chicanery": 2,
            "chronos": 1,
            "contract": 0,
            "dragons_ire": 0,
            "legerdemain": 0,
            "metamorphosis": 0,
            "naming": 0,
            "oneiromancy": 0,
            "primal": 0,
            "pyretics": 0,
            "skycraft": 0,
            "soothsay": 0,
            "sovereign": 0,
            "spring": 0,
            "summer": 0,
            "wayfare": 0,
            "winter": 0,
            "actor": 2,
            "fae": 2,
            "nature_realm": 1,
            "prop": 0,
            "scene": 0,
            "time": 0,
        }
        from django.urls import reverse

        url = reverse(
            "characters:changeling:changeling_arts_realms", kwargs={"pk": self.changeling.pk}
        )
        response = self.client.post(url, data=data)
        # Should return form with errors (stay on page)
        self.assertEqual(response.status_code, 200)

    def test_realms_must_total_five(self):
        """Test that realms must total exactly 5 dots."""
        self.client.login(username="ST", password="password")
        # Post with realms totaling 3, not 5
        data = {
            "autumn": 1,
            "chicanery": 1,
            "chronos": 1,
            "contract": 0,
            "dragons_ire": 0,
            "legerdemain": 0,
            "metamorphosis": 0,
            "naming": 0,
            "oneiromancy": 0,
            "primal": 0,
            "pyretics": 0,
            "skycraft": 0,
            "soothsay": 0,
            "sovereign": 0,
            "spring": 0,
            "summer": 0,
            "wayfare": 0,
            "winter": 0,
            "actor": 1,
            "fae": 1,
            "nature_realm": 1,
            "prop": 0,
            "scene": 0,
            "time": 0,
        }
        from django.urls import reverse

        url = reverse(
            "characters:changeling:changeling_arts_realms", kwargs={"pk": self.changeling.pk}
        )
        response = self.client.post(url, data=data)
        # Should return form with errors (stay on page)
        self.assertEqual(response.status_code, 200)

    def test_valid_arts_realms_submission(self):
        """Test that valid arts and realms submission succeeds."""
        self.client.login(username="ST", password="password")
        # Post with valid totals: arts = 3, realms = 5
        data = {
            "autumn": 1,
            "chicanery": 1,
            "chronos": 1,
            "contract": 0,
            "dragons_ire": 0,
            "legerdemain": 0,
            "metamorphosis": 0,
            "naming": 0,
            "oneiromancy": 0,
            "primal": 0,
            "pyretics": 0,
            "skycraft": 0,
            "soothsay": 0,
            "sovereign": 0,
            "spring": 0,
            "summer": 0,
            "wayfare": 0,
            "winter": 0,
            "actor": 2,
            "fae": 2,
            "nature_realm": 1,
            "prop": 0,
            "scene": 0,
            "time": 0,
        }
        from django.urls import reverse

        url = reverse(
            "characters:changeling:changeling_arts_realms", kwargs={"pk": self.changeling.pk}
        )
        response = self.client.post(url, data=data)
        # Should redirect on success
        self.assertEqual(response.status_code, 302)
        self.changeling.refresh_from_db()
        self.assertEqual(self.changeling.creation_status, 5)


class TestChangelingSeemingAndCourt(TestCase):
    """Tests for seeming and court mechanics."""

    def setUp(self):
        self.player = User.objects.create_user(username="User1", password="12345")
        changeling_setup()

    def test_wilder_seeming_bonus(self):
        """Test that wilder seeming adds to glamour or willpower."""
        char = Changeling.objects.create(owner=self.player, name="Wilder Test")
        initial_glamour = char.glamour
        char.set_seeming("wilder")
        # Wilder adds 1 to either glamour or willpower (implementation adds to glamour)
        self.assertEqual(char.glamour, initial_glamour + 1)

    def test_childling_seeming_bonus(self):
        """Test that childling seeming adds to glamour."""
        char = Changeling.objects.create(owner=self.player, name="Childling Test")
        initial_glamour = char.glamour
        char.set_seeming("childling")
        self.assertEqual(char.glamour, initial_glamour + 1)

    def test_grump_seeming_bonus(self):
        """Test that grump seeming adds to willpower."""
        char = Changeling.objects.create(owner=self.player, name="Grump Test")
        char.set_seeming("grump")
        # Willpower is set to 4 then adds 1
        self.assertEqual(char.willpower, 5)

    def test_court_seelie(self):
        """Test setting seelie court."""
        char = Changeling.objects.create(owner=self.player, name="Seelie Test")
        self.assertFalse(char.has_court())
        char.set_court("seelie")
        self.assertTrue(char.has_court())
        self.assertEqual(char.court, "seelie")

    def test_court_unseelie(self):
        """Test setting unseelie court."""
        char = Changeling.objects.create(owner=self.player, name="Unseelie Test")
        self.assertFalse(char.has_court())
        char.set_court("unseelie")
        self.assertTrue(char.has_court())
        self.assertEqual(char.court, "unseelie")


class TestChangelingHouseMechanics(TestCase):
    """Tests for house mechanics including court matching."""

    def setUp(self):
        self.player = User.objects.create_user(username="User1", password="12345")
        changeling_setup()

    def test_house_requires_matching_court(self):
        """Test that house must match character's court."""
        char = Changeling.objects.create(owner=self.player, name="House Test")
        char.title = 1
        char.court = "seelie"
        seelie_house = House.objects.filter(court="seelie").first()
        unseelie_house = House.objects.filter(court="unseelie").first()

        # Should succeed with matching court
        result = char.set_house(seelie_house)
        self.assertTrue(result)
        self.assertEqual(char.house, seelie_house)

        # Should fail with mismatched court
        char.house = None
        result = char.set_house(unseelie_house)
        self.assertFalse(result)
        self.assertIsNone(char.house)

    def test_sidhe_automatic_house_eligibility(self):
        """Test that Sidhe kiths are automatically eligible for houses."""
        arcadian_sidhe = Kith.objects.create(name="Arcadian Sidhe")
        char = Changeling.objects.create(owner=self.player, name="Sidhe Test", kith=arcadian_sidhe)
        # Sidhe should be eligible even without title
        self.assertTrue(char.eligible_for_house())

    def test_non_sidhe_needs_title_for_house(self):
        """Test that non-Sidhe kiths need title for house eligibility."""
        regular_kith = Kith.objects.get(name="Kith 0")
        char = Changeling.objects.create(owner=self.player, name="Regular Test", kith=regular_kith)
        # Should not be eligible without title
        self.assertFalse(char.eligible_for_house())
        # Should be eligible with title
        char.title = 1
        self.assertTrue(char.eligible_for_house())
