from characters.models.werewolf.wtahuman import WtAHuman
from characters.tests.utils import werewolf_setup
from django.contrib.auth.models import User
from django.test import TestCase
from game.models import Chronicle


class TestWtAHuman(TestCase):
    def setUp(self):
        self.player = User.objects.create_user(username="Player")
        self.character = WtAHuman.objects.create(name="Test WtAHuman", owner=self.player)
        werewolf_setup()

    def set_abilities(self):
        self.character.brawl = 1
        self.character.expression = 3
        self.character.intimidation = 2
        self.character.subterfuge = 1
        self.character.leadership = 4
        self.character.crafts = 2
        self.character.etiquette = 1
        self.character.animal_ken = 5
        self.character.larceny = 2
        self.character.survival = 1
        self.character.computer = 4
        self.character.science = 5
        self.character.law = 3
        self.character.rituals = 2
        self.character.technology = 1
        self.character.save()

    def test_get_abilities(self):
        self.assertEqual(
            self.character.get_abilities(),
            {
                "alertness": 0,
                "athletics": 0,
                "brawl": 0,
                "empathy": 0,
                "expression": 0,
                "intimidation": 0,
                "streetwise": 0,
                "subterfuge": 0,
                "leadership": 0,
                "primal_urge": 0,
                "crafts": 0,
                "drive": 0,
                "etiquette": 0,
                "firearms": 0,
                "melee": 0,
                "stealth": 0,
                "animal_ken": 0,
                "larceny": 0,
                "performance": 0,
                "survival": 0,
                "academics": 0,
                "computer": 0,
                "investigation": 0,
                "medicine": 0,
                "science": 0,
                "enigmas": 0,
                "law": 0,
                "occult": 0,
                "rituals": 0,
                "technology": 0,
            },
        )
        self.set_abilities()
        self.assertEqual(
            self.character.get_abilities(),
            {
                "alertness": 0,
                "athletics": 0,
                "brawl": 1,
                "empathy": 0,
                "expression": 3,
                "intimidation": 2,
                "streetwise": 0,
                "subterfuge": 1,
                "leadership": 4,
                "primal_urge": 0,
                "crafts": 2,
                "drive": 0,
                "etiquette": 1,
                "firearms": 0,
                "melee": 0,
                "stealth": 0,
                "animal_ken": 5,
                "larceny": 2,
                "performance": 0,
                "survival": 1,
                "academics": 0,
                "computer": 4,
                "investigation": 0,
                "medicine": 0,
                "science": 5,
                "enigmas": 0,
                "law": 3,
                "occult": 0,
                "rituals": 2,
                "technology": 1,
            },
        )

    def test_get_talents(self):
        self.assertEqual(
            self.character.get_talents(),
            {
                "alertness": 0,
                "athletics": 0,
                "brawl": 0,
                "empathy": 0,
                "expression": 0,
                "intimidation": 0,
                "streetwise": 0,
                "subterfuge": 0,
                "leadership": 0,
                "primal_urge": 0,
            },
        )
        self.set_abilities()
        self.assertEqual(
            self.character.get_talents(),
            {
                "alertness": 0,
                "athletics": 0,
                "brawl": 1,
                "empathy": 0,
                "expression": 3,
                "intimidation": 2,
                "streetwise": 0,
                "subterfuge": 1,
                "leadership": 4,
                "primal_urge": 0,
            },
        )

    def test_get_skills(self):
        self.assertEqual(
            self.character.get_skills(),
            {
                "crafts": 0,
                "drive": 0,
                "etiquette": 0,
                "firearms": 0,
                "melee": 0,
                "stealth": 0,
                "animal_ken": 0,
                "larceny": 0,
                "performance": 0,
                "survival": 0,
            },
        )
        self.set_abilities()
        self.assertEqual(
            self.character.get_skills(),
            {
                "crafts": 2,
                "drive": 0,
                "etiquette": 1,
                "firearms": 0,
                "melee": 0,
                "stealth": 0,
                "animal_ken": 5,
                "larceny": 2,
                "performance": 0,
                "survival": 1,
            },
        )

    def test_get_knowledges(self):
        self.assertEqual(
            self.character.get_knowledges(),
            {
                "academics": 0,
                "computer": 0,
                "investigation": 0,
                "medicine": 0,
                "science": 0,
                "enigmas": 0,
                "law": 0,
                "occult": 0,
                "rituals": 0,
                "technology": 0,
            },
        )
        self.set_abilities()
        self.assertEqual(
            self.character.get_knowledges(),
            {
                "academics": 0,
                "computer": 4,
                "investigation": 0,
                "medicine": 0,
                "science": 5,
                "enigmas": 0,
                "law": 3,
                "occult": 0,
                "rituals": 2,
                "technology": 1,
            },
        )

    def test_get_backgrounds(self):
        self.assertEqual(
            self.character.get_backgrounds(),
            {
                "allies": 0,
                "ancestors": 0,
                "fate": 0,
                "fetish": 0,
                "kinfolk_rating": 0,
                "pure_breed": 0,
                "contacts": 0,
                "rites": 0,
                "spirit_heritage": 0,
                "mentor": 0,
                "resources": 0,
                "totem": 0,
            },
        )
        self.character.allies = 1
        self.character.ancestors = 3
        self.character.kinfolk_rating = 3
        self.character.pure_breed = 2
        self.character.mentor = 2
        self.assertEqual(
            self.character.get_backgrounds(),
            {
                "allies": 1,
                "ancestors": 3,
                "fate": 0,
                "fetish": 0,
                "kinfolk_rating": 3,
                "pure_breed": 2,
                "contacts": 0,
                "rites": 0,
                "spirit_heritage": 0,
                "mentor": 2,
                "resources": 0,
                "totem": 0,
            },
        )

    def test_total_backgrounds(self):
        self.character.allies = 3
        self.character.ancestors = 4
        self.character.resources = 1
        self.character.fetish = 2
        self.assertEqual(self.character.total_backgrounds(), 10)
        self.character.spirit_heritage = 2
        self.assertEqual(self.character.total_backgrounds(), 12)


class TestWtAHumanDetailView(TestCase):
    def setUp(self) -> None:
        self.player = User.objects.create_user(username="User1", password="12345")
        self.wtahuman = WtAHuman.objects.create(
            name="Test WtAHuman",
            owner=self.player,
            status="App",
        )
        self.url = self.wtahuman.get_absolute_url()

    def test_effect_detail_view_status_code(self):
        self.client.login(username="User1", password="12345")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_effect_detail_view_templates(self):
        self.client.login(username="User1", password="12345")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/werewolf/wtahuman/detail.html")


class TestWtAHumanCreateView(TestCase):
    def setUp(self):
        self.st = User.objects.create_user(username="ST", password="password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.chronicle.storytellers.add(self.st)
        self.valid_data = {
            "name": "Test WtAHuman",
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
        }
        self.url = WtAHuman.get_creation_url()

    def test_create_view_status_code(self):
        self.client.login(username="ST", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        self.client.login(username="ST", password="password")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/werewolf/wtahuman/basics.html")

    def test_create_view_successful_post(self):
        self.client.login(username="ST", password="password")
        response = self.client.post(self.url, data={"name": "Test WtAHuman"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(WtAHuman.objects.count(), 1)
        self.assertEqual(WtAHuman.objects.first().name, "Test WtAHuman")


class TestWtAHumanUpdateView(TestCase):
    def setUp(self):
        self.st = User.objects.create_user(username="ST", password="password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.chronicle.storytellers.add(self.st)
        self.wtahuman = WtAHuman.objects.create(
            name="Test WtAHuman",
            owner=self.st,
            chronicle=self.chronicle,
            description="Test",
        )
        self.valid_data = {
            "name": "Test WtAHuman 2",
            "owner": self.st.id,
            "description": "Tst",
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
        }
        self.url = self.wtahuman.get_update_url()

    def test_update_view_status_code(self):
        self.client.login(username="ST", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        self.client.login(username="ST", password="password")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/werewolf/wtahuman/form.html")

    def test_update_view_successful_post(self):
        self.client.login(username="ST", password="password")
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.wtahuman.refresh_from_db()
        self.assertEqual(self.wtahuman.name, "Test WtAHuman 2")
