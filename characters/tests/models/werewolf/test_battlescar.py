from django.test import TestCase

from characters.models.werewolf.battlescar import BattleScar


class TestBattleScarDetailView(TestCase):
    def setUp(self) -> None:
        self.battlescar = BattleScar.objects.create(name="Test BattleScar")
        self.url = self.battlescar.get_absolute_url()

    def test_battlescar_detail_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_battlescar_detail_view_templates(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/werewolf/battlescar/detail.html")


class TestBattleScarCreateView(TestCase):
    def setUp(self):
        self.valid_data = {
            "name": "BattleScar",
            "description": "Test",
            "glory": 2,
        }
        self.url = BattleScar.get_creation_url()

    def test_create_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/werewolf/battlescar/form.html")

    def test_create_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(BattleScar.objects.count(), 1)
        self.assertEqual(BattleScar.objects.first().name, "BattleScar")


class TestBattleScarUpdateView(TestCase):
    def setUp(self):
        self.battlescar = BattleScar.objects.create(
            name="Test BattleScar",
            description="Test description",
        )
        self.valid_data = {
            "name": "BattleScar Updated",
            "description": "Test",
            "glory": 2,
        }
        self.url = self.battlescar.get_update_url()

    def test_update_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/werewolf/battlescar/form.html")

    def test_update_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.battlescar.refresh_from_db()
        self.assertEqual(self.battlescar.name, "BattleScar Updated")
        self.assertEqual(self.battlescar.description, "Test")
