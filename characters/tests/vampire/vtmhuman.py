from characters.models.vampire.vtmhuman import VtMHuman
from django.contrib.auth.models import User
from django.test import TestCase


class TestVtMHuman(TestCase):
    def setUp(self):
        self.player = User.objects.create_user(username="Player")
        self.character = VtMHuman.objects.create(
            name="Test VtMHuman", owner=self.player
        )

    def set_abilities(self):
        self.character.alertness = 1
        self.character.brawl = 2
        self.character.expression = 3
        self.character.subterfuge = 4
        self.character.leadership = 5

        self.character.crafts = 5
        self.character.etiquette = 4
        self.character.melee = 3
        self.character.animal_ken = 2
        self.character.performance = 1

        self.character.academics = 2
        self.character.investigation = 5
        self.character.science = 3
        self.character.occult = 1
        self.character.technology = 4

    def set_backgrounds(self):
        self.character.contacts = 1
        self.character.mentor = 2
        self.character.allies = 3
        self.character.alternate_identity = 4
        self.character.black_hand_membership = 5
        self.character.domain = 4
        self.character.fame = 3
        self.character.generation = 2
        self.character.herd = 1
        self.character.influence = 2
        self.character.resources = 3
        self.character.retainers = 4
        self.character.rituals = 5
        self.character.status_background = 5

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
                "leadership": 0,
            },
        )
        self.set_abilities()
        self.assertEqual(
            self.character.get_talents(),
            {
                "alertness": 1,
                "athletics": 0,
                "brawl": 2,
                "empathy": 0,
                "expression": 3,
                "intimidation": 0,
                "streetwise": 0,
                "subterfuge": 4,
                "awareness": 0,
                "leadership": 5,
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
                "crafts": 5,
                "drive": 0,
                "etiquette": 4,
                "firearms": 0,
                "melee": 3,
                "stealth": 0,
                "animal_ken": 2,
                "larceny": 0,
                "performance": 1,
                "survival": 0,
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
                "finance": 0,
                "law": 0,
                "occult": 0,
                "politics": 0,
                "technology": 0,
            },
        )
        self.set_abilities()
        self.assertEqual(
            self.character.get_knowledges(),
            {
                "academics": 2,
                "computer": 0,
                "investigation": 5,
                "medicine": 0,
                "science": 3,
                "finance": 0,
                "law": 0,
                "occult": 1,
                "politics": 0,
                "technology": 4,
            },
        )

    def test_get_backgrounds(self):
        self.assertEqual(
            self.character.get_backgrounds(),
            {
                "contacts": 0,
                "mentor": 0,
                "allies": 0,
                "alternate_identity": 0,
                "black_hand_membership": 0,
                "domain": 0,
                "fame": 0,
                "generation": 0,
                "herd": 0,
                "influence": 0,
                "resources": 0,
                "retainers": 0,
                "rituals": 0,
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
                "alternate_identity": 4,
                "black_hand_membership": 5,
                "domain": 4,
                "fame": 3,
                "generation": 2,
                "herd": 1,
                "influence": 2,
                "resources": 3,
                "retainers": 4,
                "rituals": 5,
                "status_background": 5,
            },
        )


class TestVtMHumanDetailView(TestCase):
    def setUp(self) -> None:
        self.vtmhuman = VtMHuman.objects.create(name="Test VtMHuman")
        self.url = self.vtmhuman.get_absolute_url()

    def test_effect_detail_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_effect_detail_view_templates(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/vampire/vtmhuman/detail.html")


class TestVtMHumanCreateView(TestCase):
    def setUp(self):
        self.valid_data = {
            "name": "Test VtMHuman",
            "description": "Test",
            "willpower": 3,
            "age": 200,
            "apparent_age": 18,
            "hair": "Asfa",
            "eyes": "asf",
            "ethnicity": "asfa",
            "nationality": "asfasf",
            "height": "afasf",
            "weight": "Asfas",
            "sex": "asfasf",
            "childhood": "asfasf",
            "history": "afasf",
            "goals": "asfasf",
            "notes": "asfasf",
            "strength": 1,
            "dexterity": 1,
            "stamina": 1,
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
            "contacts": 0,
            "mentor": 0,
            "xp": 0,
            "awareness": 0,
            "leadership": 0,
            "animal_ken": 0,
            "larceny": 0,
            "performance": 0,
            "survival": 0,
            "finance": 0,
            "law": 0,
            "occult": 0,
            "politics": 0,
            "technology": 0,
            "allies": 0,
            "alternate_identity": 0,
            "black_hand_membership": 0,
            "domain": 0,
            "fame": 0,
            "generation": 0,
            "herd": 0,
            "influence": 0,
            "resources": 0,
            "retainers": 0,
            "rituals": 0,
            "status_background": 0,
        }
        self.url = VtMHuman.get_creation_url()

    def test_create_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/vampire/vtmhuman/form.html")

    def test_create_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(VtMHuman.objects.count(), 1)
        self.assertEqual(VtMHuman.objects.first().name, "Test VtMHuman")


class TestVtMHumanUpdateView(TestCase):
    def setUp(self):
        self.vtmhuman = VtMHuman.objects.create(
            name="Test VtMHuman", description="Test"
        )
        self.valid_data = {
            "name": "Test VtMHuman 2",
            "description": "Tst",
            "willpower": 3,
            "age": 200,
            "apparent_age": 18,
            "hair": "Asfa",
            "eyes": "asf",
            "ethnicity": "asfa",
            "nationality": "asfasf",
            "height": "afasf",
            "weight": "Asfas",
            "sex": "asfasf",
            "childhood": "asfasf",
            "history": "afasf",
            "goals": "asfasf",
            "notes": "asfasf",
            "strength": 1,
            "dexterity": 1,
            "stamina": 1,
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
            "contacts": 0,
            "mentor": 0,
            "xp": 0,
            "awareness": 0,
            "leadership": 0,
            "animal_ken": 0,
            "larceny": 0,
            "performance": 0,
            "survival": 0,
            "finance": 0,
            "law": 0,
            "occult": 0,
            "politics": 0,
            "technology": 0,
            "allies": 0,
            "alternate_identity": 0,
            "black_hand_membership": 0,
            "domain": 0,
            "fame": 0,
            "generation": 0,
            "herd": 0,
            "influence": 0,
            "resources": 0,
            "retainers": 0,
            "rituals": 0,
            "status_background": 0,
        }
        self.url = self.vtmhuman.get_update_url()

    def test_update_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/vampire/vtmhuman/form.html")

    def test_update_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.vtmhuman.refresh_from_db()
        self.assertEqual(self.vtmhuman.name, "Test VtMHuman 2")
