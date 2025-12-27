from characters.models.changeling.changeling import Changeling
from characters.models.changeling.house import House
from characters.models.changeling.kith import Kith
from characters.models.changeling.legacy import Legacy
from characters.tests.utils import changeling_setup
from django.contrib.auth.models import User
from django.test import TestCase


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

    def test_add_banality(self):
        b = self.character.banality
        self.assertTrue(self.character.add_banality())
        self.assertEqual(self.character.banality, b + 1)

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


class TestChangelingDetailView(TestCase):
    def setUp(self) -> None:
        self.player = User.objects.create_user(username="User1", password="12345")
        self.changeling = Changeling.objects.create(
            name="Test Changeling",
            owner=self.player,
        )
        self.url = self.changeling.get_absolute_url()

    def test_changeling_detail_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_changeling_detail_view_templates(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/changeling/changeling/detail.html")


class TestChangelingCreateView(TestCase):
    def setUp(self):
        self.valid_data = {
            "name": "Changeling",
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
            "willpower": 1,
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
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/changeling/changeling/form.html")

    def test_create_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Changeling.objects.count(), 1)
        self.assertEqual(Changeling.objects.first().name, "Changeling")


class TestChangelingUpdateView(TestCase):
    def setUp(self):
        self.player = User.objects.create_user(username="User1", password="12345")
        self.changeling = Changeling.objects.create(
            name="Test Changeling",
            owner=self.player,
            description="Test description",
        )
        self.valid_data = {
            "name": "Changeling Updated",
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
            "willpower": 1,
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
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/changeling/changeling/form.html")

    def test_update_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.changeling.refresh_from_db()
        self.assertEqual(self.changeling.name, "Changeling Updated")
        self.assertEqual(self.changeling.description, "Test")
