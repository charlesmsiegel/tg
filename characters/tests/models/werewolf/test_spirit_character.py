from characters.models.werewolf.spirit_character import SpiritCharacter
from django.contrib.auth.models import User
from django.test import TestCase
from game.models import Chronicle


class TestSpiritDetailView(TestCase):
    def setUp(self) -> None:
        self.player = User.objects.create_user(username="User1", password="12345")
        self.spirit = SpiritCharacter.objects.create(
            name="Test Spirit",
            owner=self.player,
            status="App",
        )
        self.url = self.spirit.get_absolute_url()

    def test_spirit_detail_view_status_code(self):
        self.client.login(username="User1", password="12345")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_spirit_detail_view_templates(self):
        self.client.login(username="User1", password="12345")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/werewolf/spirit/detail.html")


class TestSpiritCreateView(TestCase):
    def setUp(self):
        self.st = User.objects.create_user(username="ST", password="password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.chronicle.storytellers.add(self.st)
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
        self.client.login(username="ST", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        self.client.login(username="ST", password="password")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/werewolf/spirit/form.html")

    def test_create_view_successful_post(self):
        self.client.login(username="ST", password="password")
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(SpiritCharacter.objects.count(), 1)
        self.assertEqual(SpiritCharacter.objects.first().name, "Spirit")


class TestSpiritUpdateView(TestCase):
    def setUp(self):
        self.st = User.objects.create_user(username="ST", password="password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.chronicle.storytellers.add(self.st)
        self.spirit = SpiritCharacter.objects.create(
            name="Test Spirit",
            owner=self.st,
            chronicle=self.chronicle,
            description="Test description",
        )
        self.valid_data = {
            "name": "Spirit Updated",
            "owner": self.st.id,
            "description": "Test",
            "willpower": 2,
            "rage": 4,
            "gnosis": 1,
            "essence": 20,
        }
        self.url = self.spirit.get_update_url()

    def test_update_view_status_code(self):
        self.client.login(username="ST", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        self.client.login(username="ST", password="password")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/werewolf/spirit/form.html")

    def test_update_view_successful_post(self):
        self.client.login(username="ST", password="password")
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.spirit.refresh_from_db()
        self.assertEqual(self.spirit.name, "Spirit Updated")
        self.assertEqual(self.spirit.description, "Test")
