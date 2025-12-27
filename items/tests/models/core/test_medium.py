from django.test import TestCase
from items.models.core import Medium


class TestMediumDetailView(TestCase):
    def setUp(self) -> None:
        self.medium = Medium.objects.create(
            name="Test Medium", length_modifier_type="/", length_modifier=4
        )
        self.url = self.medium.get_absolute_url()

    def test_medium_detail_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_medium_detail_view_templates(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "items/core/medium/detail.html")


class TestMediumCreateView(TestCase):
    def setUp(self):
        self.valid_data = {
            "name": "Test Medium",
            "length_modifier_type": "/",
            "length_modifier": 4,
        }
        self.url = Medium.get_creation_url()

    def test_create_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "items/core/medium/form.html")

    def test_create_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Medium.objects.count(), 1)
        self.assertEqual(Medium.objects.first().name, "Test Medium")


class TestMediumUpdateView(TestCase):
    def setUp(self):
        self.medium = Medium.objects.create(
            name="Test Medium", length_modifier_type="/", length_modifier=4
        )
        self.valid_data = {
            "name": "Test Medium 2",
            "length_modifier_type": "/",
            "length_modifier": 4,
        }
        self.url = self.medium.get_update_url()

    def test_update_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "items/core/medium/form.html")

    def test_update_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.medium.refresh_from_db()
        self.assertEqual(self.medium.name, "Test Medium 2")
