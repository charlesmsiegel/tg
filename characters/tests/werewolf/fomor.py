from characters.models.core.archetype import Archetype
from characters.models.core.specialty import Specialty
from characters.models.werewolf.fomor import Fomor
from characters.models.werewolf.fomoripower import FomoriPower
from characters.tests.utils import werewolf_setup
from django.test import TestCase


class TestFomor(TestCase):
    def setUp(self):
        werewolf_setup()
        self.power1 = FomoriPower.objects.create(name="Power 1")
        self.power2 = FomoriPower.objects.create(name="Power 2")
        self.power3 = FomoriPower.objects.create(name="Power 3")
        self.fomor = Fomor.objects.create(name="Test Fomor")
        self.fomor.allies = 2
        self.fomor.contacts = 1

    def test_get_backgrounds(self):
        expected = {
            "allies": 2,
            "contacts": 1,
            "resources": 0,
        }
        self.assertEqual(self.fomor.get_backgrounds(), expected)

    def test_add_power(self):
        self.fomor.add_power(self.power1)
        self.assertEqual(self.fomor.powers.count(), 1)
        self.assertEqual(list(self.fomor.powers.all()), [self.power1])

    def test_filter_powers(self):
        self.fomor.add_power(self.power1)
        self.fomor.add_power(self.power2)
        self.fomor.add_power(self.power3)
        filtered_powers = self.fomor.filter_powers()
        self.assertEqual(filtered_powers.count(), 0)
        self.fomor.powers.remove(self.power3)
        filtered_powers = self.fomor.filter_powers()
        self.assertEqual(filtered_powers.count(), 1)
        self.assertEqual(list(filtered_powers.all()), [self.power3])


class TestFomorDetailView(TestCase):
    def setUp(self) -> None:
        self.fomor = Fomor.objects.create(name="Test Fomor")
        self.url = self.fomor.get_absolute_url()

    def test_fomor_detail_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_fomor_detail_view_templates(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/werewolf/fomor/detail.html")


class TestFomorCreateView(TestCase):
    def setUp(self):
        self.valid_data = {
            "name": "Fomor",
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
            "rage": 1,
            "gnosis": 1,
        }
        self.url = Fomor.get_creation_url()

    def test_create_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/werewolf/fomor/form.html")

    def test_create_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Fomor.objects.count(), 1)
        self.assertEqual(Fomor.objects.first().name, "Fomor")


class TestFomorUpdateView(TestCase):
    def setUp(self):
        self.fomor = Fomor.objects.create(
            name="Test Fomor",
            description="Test description",
        )
        self.valid_data = {
            "name": "Fomor Updated",
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
            "rage": 1,
            "gnosis": 1,
        }
        self.url = self.fomor.get_update_url()

    def test_update_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/werewolf/fomor/form.html")

    def test_update_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.fomor.refresh_from_db()
        self.assertEqual(self.fomor.name, "Fomor Updated")
        self.assertEqual(self.fomor.description, "Test")
