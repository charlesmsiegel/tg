from characters.models.core import Archetype
from django.test import TestCase


class TestArchetypeDetailView(TestCase):
    def setUp(self) -> None:
        self.archetype = Archetype.objects.create(name="Test Archetype")
        self.url = self.archetype.get_absolute_url()

    def test_archetype_detail_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_archetype_detail_view_templates(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/core/archetype/detail.html")


class TestArchetypeCreateView(TestCase):
    def setUp(self):
        self.valid_data = {
            "name": "Test Archetype",
            "description": "A test description for the Archetype.",
        }
        self.url = Archetype.get_creation_url()

    def test_create_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/core/archetype/form.html")

    def test_create_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Archetype.objects.count(), 1)
        self.assertEqual(Archetype.objects.first().name, "Test Archetype")


class TestArchetypeUpdateView(TestCase):
    def setUp(self):
        self.archetype = Archetype.objects.create(name="Test Archetype")
        self.valid_data = {
            "name": "Test Archetype Updated",
            "description": "A test description for the Archetype.",
        }
        self.url = self.archetype.get_update_url()

    def test_update_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/core/archetype/form.html")

    def test_update_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.archetype.refresh_from_db()
        self.assertEqual(self.archetype.name, "Test Archetype Updated")
        self.assertEqual(self.archetype.description, "A test description for the Archetype.")
