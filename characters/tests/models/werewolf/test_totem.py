from django.test import TestCase

from characters.models.werewolf.totem import Totem


class TestTotemDetailView(TestCase):
    def setUp(self) -> None:
        self.totem = Totem.objects.create(name="Test Totem")
        self.url = self.totem.get_absolute_url()

    def test_totem_detail_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_totem_detail_view_templates(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/werewolf/totem/detail.html")


class TestTotemCreateView(TestCase):
    def setUp(self):
        self.valid_data = {
            "name": "Totem",
            "description": "Test",
            "cost": 3,
            "totem_type": "respect",
            "individual_traits": "Test",
            "pack_traits": "Test",
            "ban": "Test",
        }
        self.url = Totem.get_creation_url()

    def test_create_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/werewolf/totem/form.html")

    def test_create_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Totem.objects.count(), 1)
        self.assertEqual(Totem.objects.first().name, "Totem")


class TestTotemUpdateView(TestCase):
    def setUp(self):
        self.totem = Totem.objects.create(
            name="Test Totem",
            description="Test description",
        )
        self.valid_data = {
            "name": "Totem Updated",
            "description": "Test",
            "cost": 3,
            "totem_type": "respect",
            "individual_traits": "Test",
            "pack_traits": "Test",
            "ban": "Test",
        }
        self.url = self.totem.get_update_url()

    def test_update_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/werewolf/totem/form.html")

    def test_update_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.totem.refresh_from_db()
        self.assertEqual(self.totem.name, "Totem Updated")
        self.assertEqual(self.totem.description, "Test")
