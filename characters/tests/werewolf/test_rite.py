from characters.models.werewolf.rite import Rite
from django.test import TestCase


class TestRiteDetailView(TestCase):
    def setUp(self) -> None:
        self.rite = Rite.objects.create(name="Test Rite")
        self.url = self.rite.get_absolute_url()

    def test_rite_detail_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_rite_detail_view_templates(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/werewolf/rite/detail.html")


class TestRiteCreateView(TestCase):
    def setUp(self):
        self.valid_data = {
            "name": "Rite",
            "description": "Test",
            "level": 2,
            "rite_type": "Test",
        }
        self.url = Rite.get_creation_url()

    def test_create_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/werewolf/rite/form.html")

    def test_create_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Rite.objects.count(), 1)
        self.assertEqual(Rite.objects.first().name, "Rite")


class TestRiteUpdateView(TestCase):
    def setUp(self):
        self.rite = Rite.objects.create(
            name="Test Rite",
            description="Test description",
        )
        self.valid_data = {
            "name": "Rite Updated",
            "description": "Test",
            "level": 2,
            "rite_type": "Test",
        }
        self.url = self.rite.get_update_url()

    def test_update_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/werewolf/rite/form.html")

    def test_update_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.rite.refresh_from_db()
        self.assertEqual(self.rite.name, "Rite Updated")
        self.assertEqual(self.rite.description, "Test")
