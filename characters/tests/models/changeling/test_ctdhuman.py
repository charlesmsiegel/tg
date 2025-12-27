from characters.models.changeling.changeling import Changeling
from characters.models.changeling.ctdhuman import CtDHuman
from characters.tests.utils import changeling_setup
from django.contrib.auth.models import User
from django.test import TestCase


class TestCtDHuman(TestCase):
    def setUp(self) -> None:
        self.player = User.objects.create_user(username="User1", password="12345")
        self.character = Changeling.objects.create(owner=self.player, name="Test Changeling")
        changeling_setup()

    def set_abilities(self):
        self.character.kenning = 3
        self.character.leadership = 2
        self.character.crafts = 3
        self.character.animal_ken = 2
        self.character.larceny = 2
        self.character.enigmas = 2
        self.character.gremayre = 3

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
                "kenning": 0,
                "leadership": 0,
                "streetwise": 0,
                "subterfuge": 0,
            },
        )
        self.set_abilities()
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
                "kenning": 3,
                "leadership": 2,
            },
        )

    def test_get_skills(self):
        self.assertEqual(
            self.character.get_skills(),
            {
                "animal_ken": 0,
                "crafts": 0,
                "drive": 0,
                "etiquette": 0,
                "firearms": 0,
                "larceny": 0,
                "melee": 0,
                "performance": 0,
                "stealth": 0,
                "survival": 0,
            },
        )
        self.set_abilities()
        self.assertEqual(
            self.character.get_skills(),
            {
                "crafts": 3,
                "drive": 0,
                "etiquette": 0,
                "firearms": 0,
                "melee": 0,
                "stealth": 0,
                "animal_ken": 2,
                "larceny": 2,
                "performance": 0,
                "survival": 0,
            },
        )

    def test_get_knowledges(self):
        self.assertEqual(
            self.character.get_knowledges(),
            {
                "academics": 0,
                "computer": 0,
                "enigmas": 0,
                "gremayre": 0,
                "investigation": 0,
                "law": 0,
                "medicine": 0,
                "politics": 0,
                "science": 0,
                "technology": 0,
            },
        )
        self.set_abilities()
        self.assertEqual(
            self.character.get_knowledges(),
            {
                "academics": 0,
                "computer": 0,
                "investigation": 0,
                "medicine": 0,
                "science": 0,
                "enigmas": 2,
                "gremayre": 3,
                "law": 0,
                "politics": 0,
                "technology": 0,
            },
        )

    def test_get_backgrounds(self):
        self.assertEqual(
            self.character.get_backgrounds(),
            {
                "chimera": 0,
                "contacts": 0,
                "dreamers": 0,
                "holdings": 0,
                "mentor": 0,
                "remembrance": 0,
                "resources": 0,
                "retinue": 0,
                "title": 0,
                "treasure": 0,
            },
        )
        self.character.contacts = 2
        self.character.title = 3
        self.character.dreamers = 4
        self.character.resources = 5
        self.assertEqual(
            self.character.get_backgrounds(),
            {
                "contacts": 2,
                "mentor": 0,
                "chimera": 0,
                "dreamers": 4,
                "holdings": 0,
                "remembrance": 0,
                "resources": 5,
                "retinue": 0,
                "title": 3,
                "treasure": 0,
            },
        )


class TestCtDHumanDetailView(TestCase):
    def setUp(self) -> None:
        self.ctdhuman = CtDHuman.objects.create(name="Test CtDHuman")
        self.url = self.ctdhuman.get_absolute_url()

    def test_ctdhuman_detail_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_ctdhuman_detail_view_templates(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/changeling/ctdhuman/detail.html")


class TestCtDHumanCreateView(TestCase):
    def setUp(self):
        self.valid_data = {
            "name": "CtDHuman",
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
            "chimera": 1,
            "dreamers": 1,
            "holdings": 1,
            "remembrance": 1,
            "resources": 1,
            "retinue": 1,
            "title": 1,
            "treasure": 1,
        }
        self.url = CtDHuman.get_creation_url()

    def test_create_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/changeling/ctdhuman/form.html")

    def test_create_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(CtDHuman.objects.count(), 1)
        self.assertEqual(CtDHuman.objects.first().name, "CtDHuman")


class TestCtDHumanUpdateView(TestCase):
    def setUp(self):
        self.ctdhuman = CtDHuman.objects.create(
            name="Test CtDHuman",
            description="Test description",
        )
        self.valid_data = {
            "name": "CtDHuman Updated",
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
            "chimera": 1,
            "dreamers": 1,
            "holdings": 1,
            "remembrance": 1,
            "resources": 1,
            "retinue": 1,
            "title": 1,
            "treasure": 1,
        }
        self.url = self.ctdhuman.get_update_url()

    def test_update_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/changeling/ctdhuman/form.html")

    def test_update_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.ctdhuman.refresh_from_db()
        self.assertEqual(self.ctdhuman.name, "CtDHuman Updated")
        self.assertEqual(self.ctdhuman.description, "Test")
