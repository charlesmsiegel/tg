from django.test import TestCase
from locations.models.mage.sanctum import Sanctum


class TestSanctumDetailView(TestCase):
    def setUp(self) -> None:
        self.sanctum = Sanctum.objects.create(name="Test Sanctum")
        self.url = self.sanctum.get_absolute_url()

    def test_sanctum_detail_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_sanctum_detail_view_templates(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "locations/mage/sanctum/detail.html")


class TestSanctumCreateView(TestCase):
    def setUp(self):
        self.valid_data = {
            "name": "Sanctum",
            "description": "Test",
        }
        self.url = Sanctum.get_creation_url()

    def test_create_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "locations/mage/sanctum/form.html")

    def test_create_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Sanctum.objects.count(), 1)
        self.assertEqual(Sanctum.objects.first().name, "Sanctum")


class TestSanctumUpdateView(TestCase):
    def setUp(self):
        self.sanctum = Sanctum.objects.create(
            name="Test Sanctum",
            description="Test description",
        )
        self.valid_data = {
            "name": "Sanctum Updated",
            "description": "Test",
        }
        self.url = self.sanctum.get_update_url()

    def test_update_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "locations/mage/sanctum/form.html")

    def test_update_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.sanctum.refresh_from_db()
        self.assertEqual(self.sanctum.name, "Sanctum Updated")
        self.assertEqual(self.sanctum.description, "Test")
