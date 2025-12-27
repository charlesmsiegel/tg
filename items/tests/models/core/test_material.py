from django.test import TestCase
from items.models.core import Material


class TestMaterialDetailView(TestCase):
    def setUp(self) -> None:
        self.material = Material.objects.create(name="Test Material")
        self.url = self.material.get_absolute_url()

    def test_material_detail_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_material_detail_view_templates(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "items/core/material/detail.html")


class TestMaterialCreateView(TestCase):
    def setUp(self):
        self.valid_data = {"name": "Test Material", "is_hard": True}
        self.url = Material.get_creation_url()

    def test_create_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "items/core/material/form.html")

    def test_create_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Material.objects.count(), 1)
        self.assertEqual(Material.objects.first().name, "Test Material")


class TestMaterialUpdateView(TestCase):
    def setUp(self):
        self.material = Material.objects.create(name="Test Material")
        self.valid_data = {"name": "Test Material Update", "is_hard": False}
        self.url = self.material.get_update_url()

    def test_update_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "items/core/material/form.html")

    def test_update_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.material.refresh_from_db()
        self.assertEqual(self.material.name, "Test Material Update")
        self.assertFalse(self.material.is_hard)
