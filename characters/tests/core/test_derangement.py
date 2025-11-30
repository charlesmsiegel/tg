from characters.models.core import Derangement
from django.test import TestCase


class TestDerangementDetailView(TestCase):
    def setUp(self) -> None:
        self.derangement = Derangement.objects.create(name="Test Derangement")
        self.url = self.derangement.get_absolute_url()

    def test_derangement_detail_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_derangement_detail_view_templates(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/core/derangement/detail.html")


class TestDerangementCreateView(TestCase):
    def setUp(self):
        self.valid_data = {"name": "Test Derangement", "description": "Test"}
        self.url = Derangement.get_creation_url()

    def test_create_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/core/derangement/form.html")

    def test_create_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Derangement.objects.count(), 1)
        self.assertEqual(Derangement.objects.first().name, "Test Derangement")


class TestDerangementUpdateView(TestCase):
    def setUp(self):
        self.derangement = Derangement.objects.create(
            name="Test Derangement",
        )
        self.valid_data = {"name": "Test Derangement Updated", "description": "Test"}
        self.url = self.derangement.get_update_url()

    def test_update_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/core/derangement/form.html")

    def test_update_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.derangement.refresh_from_db()
        self.assertEqual(self.derangement.name, "Test Derangement Updated")
