from characters.models.werewolf.fomoripower import FomoriPower
from django.test import TestCase


class TestFomoriPowerDetailView(TestCase):
    def setUp(self) -> None:
        self.fomoripower = FomoriPower.objects.create(name="Test FomoriPower")
        self.url = self.fomoripower.get_absolute_url()

    def test_fomoripower_detail_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_fomoripower_detail_view_templates(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/werewolf/fomoripower/detail.html")


class TestFomoriPowerCreateView(TestCase):
    def setUp(self):
        self.valid_data = {
            "name": "FomoriPower",
            "description": "Test",
        }
        self.url = FomoriPower.get_creation_url()

    def test_create_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/werewolf/fomoripower/form.html")

    def test_create_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(FomoriPower.objects.count(), 1)
        self.assertEqual(FomoriPower.objects.first().name, "FomoriPower")


class TestFomoriPowerUpdateView(TestCase):
    def setUp(self):
        self.fomoripower = FomoriPower.objects.create(
            name="Test FomoriPower",
            description="Test description",
        )
        self.valid_data = {
            "name": "FomoriPower Updated",
            "description": "Test",
        }
        self.url = self.fomoripower.get_update_url()

    def test_update_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/werewolf/fomoripower/form.html")

    def test_update_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.fomoripower.refresh_from_db()
        self.assertEqual(self.fomoripower.name, "FomoriPower Updated")
        self.assertEqual(self.fomoripower.description, "Test")
