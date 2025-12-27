from characters.models.werewolf.spirit_character import SpiritCharacter
from django.test import TestCase


class TestSpiritDetailView(TestCase):
    def setUp(self) -> None:
        self.spirit = SpiritCharacter.objects.create(name="Test Spirit")
        self.url = self.spirit.get_absolute_url()

    def test_spirit_detail_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_spirit_detail_view_templates(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/werewolf/spirit/detail.html")


class TestSpiritCreateView(TestCase):
    def setUp(self):
        self.valid_data = {
            "name": "Spirit",
            "description": "Test",
            "willpower": 2,
            "rage": 4,
            "gnosis": 1,
            "essence": 20,
        }
        self.url = SpiritCharacter.get_creation_url()

    def test_create_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/werewolf/spirit/form.html")

    def test_create_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(SpiritCharacter.objects.count(), 1)
        self.assertEqual(SpiritCharacter.objects.first().name, "Spirit")


class TestSpiritUpdateView(TestCase):
    def setUp(self):
        self.spirit = SpiritCharacter.objects.create(
            name="Test Spirit",
            description="Test description",
        )
        self.valid_data = {
            "name": "Spirit Updated",
            "description": "Test",
            "willpower": 2,
            "rage": 4,
            "gnosis": 1,
            "essence": 20,
        }
        self.url = self.spirit.get_update_url()

    def test_update_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/werewolf/spirit/form.html")

    def test_update_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.spirit.refresh_from_db()
        self.assertEqual(self.spirit.name, "Spirit Updated")
        self.assertEqual(self.spirit.description, "Test")
