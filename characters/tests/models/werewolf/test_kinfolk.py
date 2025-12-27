from unittest.mock import patch

from characters.models.core.derangement import Derangement
from characters.models.core.merit_flaw_block import MeritFlaw
from characters.models.werewolf.gift import Gift, GiftPermission
from characters.models.werewolf.kinfolk import Kinfolk
from characters.models.werewolf.tribe import Tribe
from characters.tests.utils import werewolf_setup
from django.contrib.auth.models import User
from django.test import TestCase
from game.models import Chronicle
from items.models.werewolf.fetish import Fetish


class TestKinfolk(TestCase):
    def setUp(self):
        self.tribe = Tribe.objects.create(name="Test Tribe")
        self.gift = Gift.objects.create(name="Test Gift", rank=1)
        self.fetish = Fetish.objects.create(name="Test Fetish", rank=1)
        self.kinfolk = Kinfolk.objects.create(name="Test Kinfolk")
        werewolf_setup()

    def test_has_breed(self):
        self.assertFalse(self.kinfolk.has_breed())
        self.kinfolk.set_breed("homid")
        self.assertTrue(self.kinfolk.has_breed())

    def test_set_breed(self):
        self.assertEqual(self.kinfolk.breed, "")
        self.assertTrue(self.kinfolk.set_breed("lupus"))
        self.assertEqual(self.kinfolk.breed, "lupus")

    def test_set_tribe(self):
        self.assertIsNone(self.kinfolk.tribe)
        self.assertTrue(self.kinfolk.set_tribe(self.tribe))
        self.assertEqual(self.kinfolk.tribe, self.tribe)
        self.kinfolk.set_breed("homid")
        rt = Tribe.objects.create(name="Red Talons")
        sf = Tribe.objects.create(name="Silver Fangs")
        bsd = Tribe.objects.create(name="Black Spiral Dancers")
        self.assertFalse(self.kinfolk.set_tribe(rt))
        self.kinfolk.set_breed("lupus")
        self.assertTrue(self.kinfolk.set_tribe(rt))
        self.assertTrue(self.kinfolk.set_tribe(sf))
        self.assertGreater(self.kinfolk.pure_breed, 0)
        Derangement.objects.create(name="Test Derangement")
        self.assertTrue(self.kinfolk.set_tribe(bsd))
        self.assertGreater(self.kinfolk.derangements.count(), 0)

    def test_has_tribe(self):
        self.assertFalse(self.kinfolk.has_tribe())
        self.kinfolk.set_tribe(self.tribe)
        self.assertTrue(self.kinfolk.has_tribe())

    def test_get_backgrounds(self):
        backgrounds = self.kinfolk.get_backgrounds()
        self.assertEqual(backgrounds["allies"], 0)
        self.assertEqual(backgrounds["contacts"], 0)
        self.assertEqual(backgrounds["mentor"], 0)
        self.assertEqual(backgrounds["pure_breed"], 0)
        self.assertEqual(backgrounds["resources"], 0)

    def test_add_background(self):
        bg = Tribe.objects.create(name="Bone Gnawers")
        self.kinfolk.set_tribe(bg)
        self.assertFalse(self.kinfolk.add_background("pure_breed"))
        self.assertTrue(self.kinfolk.add_background("resources"))
        self.assertTrue(self.kinfolk.add_background("resources"))
        self.assertTrue(self.kinfolk.add_background("resources"))
        self.assertFalse(self.kinfolk.add_background("resources"))
        gw = Tribe.objects.create(name="Glass Walkers")
        self.kinfolk.set_tribe(gw)
        self.kinfolk.resources = 0
        self.assertFalse(self.kinfolk.add_background("pure_breed"))
        self.assertFalse(self.kinfolk.add_background("mentor"))
        rt = Tribe.objects.create(name="Red Talons")
        self.kinfolk.set_tribe(rt)
        self.assertFalse(self.kinfolk.add_background("resources"))
        self.assertFalse(self.kinfolk.add_background("allies"))
        self.assertFalse(self.kinfolk.add_background("contacts"))
        sl = Tribe.objects.create(name="Shadow Lords")
        self.kinfolk.set_tribe(sl)
        self.assertFalse(self.kinfolk.add_background("mentor"))
        self.kinfolk.resources = 3
        ss = Tribe.objects.create(name="Silent Striders")
        self.kinfolk.set_tribe(ss)
        self.assertFalse(self.kinfolk.add_background("resources"))
        sg = Tribe.objects.create(name="Stargazers")
        self.kinfolk.set_tribe(sg)
        self.assertFalse(self.kinfolk.add_background("resources"))
        w = Tribe.objects.create(name="Wendigo")
        self.kinfolk.set_tribe(w)
        self.assertFalse(self.kinfolk.add_background("resources"))

    def test_add_gift(self):
        self.assertTrue(self.kinfolk.add_gift(self.gift))
        self.assertFalse(self.kinfolk.add_gift(self.gift))

    def test_set_relation(self):
        self.assertTrue(self.kinfolk.set_relation("Test Relation"))

    def test_has_relation(self):
        self.assertFalse(self.kinfolk.has_relation())
        self.kinfolk.relation = "Test Relation"
        self.assertTrue(self.kinfolk.has_relation())

    def test_mf_based_corrections(self):
        gnosis = MeritFlaw.objects.create(name="Gnosis")
        gnosis.add_ratings([5, 6, 7])
        fetish = MeritFlaw.objects.create(name="Fetish")
        fetish.add_ratings([5, 6, 7])
        Fetish.objects.create(name="Test Fetish", rank=1)
        self.kinfolk.add_mf(gnosis, 5)
        self.kinfolk.add_mf(fetish, 5)
        self.kinfolk.mf_based_corrections()
        self.assertNotEqual(self.kinfolk.gnosis, 0)
        self.assertTrue(self.kinfolk.fetishes_owned.exists())

    def test_add_fetish(self):
        # Test that a Kinfolk can add a fetish successfully
        self.assertTrue(self.kinfolk.add_fetish(self.fetish))

        # Test that a Kinfolk cannot add a fetish they already own
        self.assertFalse(self.kinfolk.add_fetish(self.fetish))

    def test_filter_fetishes(self):
        # Test that the method returns the correct set of fetishes
        filtered_fetishes = self.kinfolk.filter_fetishes(min_rating=3, max_rating=5)
        self.assertNotIn(self.fetish, filtered_fetishes)


class TestKinfolkDetailView(TestCase):
    def setUp(self) -> None:
        self.player = User.objects.create_user(username="User1", password="12345")
        self.kinfolk = Kinfolk.objects.create(
            name="Test Kinfolk",
            owner=self.player,
            status="App",
        )
        self.url = self.kinfolk.get_absolute_url()

    def test_kinfolk_detail_view_status_code(self):
        self.client.login(username="User1", password="12345")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_kinfolk_detail_view_templates(self):
        self.client.login(username="User1", password="12345")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/werewolf/kinfolk/detail.html")


class TestKinfolkCreateView(TestCase):
    def setUp(self):
        self.st = User.objects.create_user(username="ST", password="password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.chronicle.storytellers.add(self.st)
        self.valid_data = {
            "name": "Kinfolk",
            "description": "Test",
            "concept": 0,
            "strength": 0,
            "dexterity": 0,
            "stamina": 0,
            "perception": 0,
            "intelligence": 0,
            "wits": 0,
            "charisma": 0,
            "manipulation": 0,
            "appearance": 0,
            "alertness": 0,
            "athletics": 0,
            "brawl": 0,
            "empathy": 0,
            "expression": 0,
            "intimidation": 0,
            "streetwise": 0,
            "subterfuge": 0,
            "crafts": 0,
            "drive": 0,
            "etiquette": 0,
            "firearms": 0,
            "melee": 0,
            "stealth": 0,
            "academics": 0,
            "computer": 0,
            "investigation": 0,
            "medicine": 0,
            "science": 0,
            "willpower": 0,
            "age": 0,
            "apparent_age": 0,
            "childhood": "aasf",
            "history": "aasf",
            "goals": "aasf",
            "notes": "aasf",
            "leadership": 0,
            "primal_urge": 0,
            "animal_ken": 0,
            "larceny": 0,
            "performance": 0,
            "survival": 0,
            "enigmas": 0,
            "law": 0,
            "occult": 0,
            "rituals": 0,
            "technology": 0,
            "breed": "homid",
            "relation": "cousin",
            "gnosis": 0,
            "glory": 0,
            "temporary_glory": 0,
            "wisdom": 0,
            "temporary_wisdom": 0,
            "honor": 0,
            "temporary_honor": 0,
        }
        self.url = Kinfolk.get_creation_url()

    def test_create_view_status_code(self):
        self.client.login(username="ST", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        self.client.login(username="ST", password="password")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/werewolf/kinfolk/basics.html")

    def test_create_view_successful_post(self):
        self.client.login(username="ST", password="password")
        response = self.client.post(self.url, data={"name": "Kinfolk"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Kinfolk.objects.count(), 1)
        self.assertEqual(Kinfolk.objects.first().name, "Kinfolk")


class TestKinfolkUpdateView(TestCase):
    def setUp(self):
        self.st = User.objects.create_user(username="ST", password="password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.chronicle.storytellers.add(self.st)
        self.kinfolk = Kinfolk.objects.create(
            name="Test Kinfolk",
            owner=self.st,
            chronicle=self.chronicle,
            description="Test description",
        )
        self.valid_data = {
            "name": "Kinfolk Updated",
            "owner": self.st.id,
            "description": "Test",
            "concept": 0,
            "strength": 0,
            "dexterity": 0,
            "stamina": 0,
            "perception": 0,
            "intelligence": 0,
            "wits": 0,
            "charisma": 0,
            "manipulation": 0,
            "appearance": 0,
            "alertness": 0,
            "athletics": 0,
            "brawl": 0,
            "empathy": 0,
            "expression": 0,
            "intimidation": 0,
            "streetwise": 0,
            "subterfuge": 0,
            "crafts": 0,
            "drive": 0,
            "etiquette": 0,
            "firearms": 0,
            "melee": 0,
            "stealth": 0,
            "academics": 0,
            "computer": 0,
            "investigation": 0,
            "medicine": 0,
            "science": 0,
            "willpower": 3,
            "temporary_willpower": 3,
            "age": 0,
            "apparent_age": 0,
            "history": "aasf",
            "goals": "aasf",
            "notes": "aasf",
            "leadership": 0,
            "primal_urge": 0,
            "animal_ken": 0,
            "larceny": 0,
            "performance": 0,
            "survival": 0,
            "enigmas": 0,
            "law": 0,
            "occult": 0,
            "rituals": 0,
            "technology": 0,
            "breed": "homid",
            "relation": "cousin",
            "gnosis": 0,
            "glory": 0,
            "temporary_glory": 0,
            "wisdom": 0,
            "temporary_wisdom": 0,
            "honor": 0,
            "temporary_honor": 0,
        }
        self.url = self.kinfolk.get_update_url()

    def test_update_view_status_code(self):
        self.client.login(username="ST", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        self.client.login(username="ST", password="password")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/werewolf/kinfolk/form.html")

    def test_update_view_successful_post(self):
        self.client.login(username="ST", password="password")
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.kinfolk.refresh_from_db()
        self.assertEqual(self.kinfolk.name, "Kinfolk Updated")
        self.assertEqual(self.kinfolk.description, "Test")
