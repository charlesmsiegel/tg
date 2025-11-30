from characters.models.wraith.wtohuman import WtOHuman
from characters.tests.utils import wraith_setup
from django.contrib.auth.models import User
from django.test import TestCase


class TestWtOHuman(TestCase):
    def setUp(self):
        self.player = User.objects.create_user(username="Player")
        self.character = WtOHuman.objects.create(
            name="Test WtOHuman", owner=self.player
        )
        wraith_setup()

    def set_abilities(self):
        self.character.alertness = 3
        self.character.awareness = 2
        self.character.persuasion = 1

        self.character.crafts = 1
        self.character.larceny = 2
        self.character.stealth = 3

        self.character.academics = 1
        self.character.bureaucracy = 2
        self.character.technology = 3

    def set_backgrounds(self):
        self.character.contacts = 1
        self.character.mentor = 2
        self.character.allies = 3
        self.character.artifact = 4
        self.character.eidolon = 5
        self.character.haunt = 4
        self.character.legacy = 3
        self.character.memoriam = 2
        self.character.notoriety = 1
        self.character.relic = 2
        self.character.status_background = 3

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
                "awareness": 0,
                "persuasion": 0,
            },
        )
        self.set_abilities()
        self.assertEqual(
            self.character.get_talents(),
            {
                "alertness": 3,
                "athletics": 0,
                "brawl": 0,
                "empathy": 0,
                "expression": 0,
                "intimidation": 0,
                "streetwise": 0,
                "subterfuge": 0,
                "awareness": 2,
                "persuasion": 1,
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
                "larceny": 0,
                "meditation": 0,
                "performance": 0,
            },
        )
        self.set_abilities()
        self.assertEqual(
            self.character.get_skills(),
            {
                "crafts": 1,
                "drive": 0,
                "etiquette": 0,
                "firearms": 0,
                "melee": 0,
                "stealth": 3,
                "larceny": 2,
                "meditation": 0,
                "performance": 0,
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
                "bureaucracy": 0,
                "enigmas": 0,
                "occult": 0,
                "politics": 0,
                "technology": 0,
            },
        )
        self.set_abilities()
        self.assertEqual(
            self.character.get_knowledges(),
            {
                "academics": 1,
                "computer": 0,
                "investigation": 0,
                "medicine": 0,
                "science": 0,
                "bureaucracy": 2,
                "enigmas": 0,
                "occult": 0,
                "politics": 0,
                "technology": 3,
            },
        )

    def test_get_backgrounds(self):
        self.assertEqual(
            self.character.get_backgrounds(),
            {
                "contacts": 0,
                "mentor": 0,
                "allies": 0,
                "artifact": 0,
                "eidolon": 0,
                "haunt": 0,
                "legacy": 0,
                "memoriam": 0,
                "notoriety": 0,
                "relic": 0,
                "status_background": 0,
            },
        )
        self.set_backgrounds()
        self.assertEqual(
            self.character.get_backgrounds(),
            {
                "contacts": 1,
                "mentor": 2,
                "allies": 3,
                "artifact": 4,
                "eidolon": 5,
                "haunt": 4,
                "legacy": 3,
                "memoriam": 2,
                "notoriety": 1,
                "relic": 2,
                "status_background": 3,
            },
        )


class TestWtOHumanDetailView(TestCase):
    def setUp(self) -> None:
        self.wtohuman = WtOHuman.objects.create(name="Test WtOHuman")
        self.url = self.wtohuman.get_absolute_url()

    def test_effect_detail_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_effect_detail_view_templates(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/wraith/wtohuman/detail.html")


class TestWtOHumanCreateView(TestCase):
    def setUp(self):
        self.valid_data = {
            "name": "Test WtOHuman",
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
            "history": "aasf",
            "goals": "aasf",
            "notes": "aasf",
            "awareness": 0,
            "persuasion": 0,
            "larceny": 0,
            "meditation": 0,
            "performance": 0,
            "bureaucracy": 0,
            "enigmas": 0,
            "occult": 0,
            "politics": 0,
            "technology": 0,
        }
        self.url = WtOHuman.get_creation_url()

    def test_create_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/wraith/wtohuman/form.html")

    def test_create_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(WtOHuman.objects.count(), 1)
        self.assertEqual(WtOHuman.objects.first().name, "Test WtOHuman")


class TestWtOHumanUpdateView(TestCase):
    def setUp(self):
        self.wtohuman = WtOHuman.objects.create(
            name="Test WtOHuman", description="Test"
        )
        self.valid_data = {
            "name": "Test WtOHuman 2",
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
            "willpower": 0,
            "age": 0,
            "apparent_age": 0,
            "childhood": "aasf",
            "history": "aasf",
            "goals": "aasf",
            "notes": "aasf",
            "awareness": 0,
            "persuasion": 0,
            "larceny": 0,
            "meditation": 0,
            "performance": 0,
            "bureaucracy": 0,
            "enigmas": 0,
            "occult": 0,
            "politics": 0,
            "technology": 0,
        }
        self.url = self.wtohuman.get_update_url()

    def test_update_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/wraith/wtohuman/form.html")

    def test_update_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.wtohuman.refresh_from_db()
        self.assertEqual(self.wtohuman.name, "Test WtOHuman 2")
