from django.contrib.auth.models import User
from django.test import TestCase

from characters.models.core import Specialty


class TestSpecialtyDetailView(TestCase):
    def setUp(self) -> None:
        self.player = User.objects.create_user(username="User1", password="12345")
        self.specialty = Specialty.objects.create(name="Test Specialty", stat="Test")
        self.url = self.specialty.get_absolute_url()

    def test_specialty_detail_view_status_code(self):
        self.client.login(username="User1", password="12345")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_specialty_detail_view_templates(self):
        self.client.login(username="User1", password="12345")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/core/specialty/detail.html")


class TestSpecialtyCreateView(TestCase):
    def setUp(self):
        self.player = User.objects.create_user(username="User1", password="12345")
        self.valid_data = {
            "name": "Test Specialty",
            "stat": "Test",
        }
        self.url = Specialty.get_creation_url()

    def test_create_view_status_code(self):
        self.client.login(username="User1", password="12345")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        self.client.login(username="User1", password="12345")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/core/specialty/form.html")

    def test_create_view_successful_post(self):
        self.client.login(username="User1", password="12345")
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Specialty.objects.count(), 1)
        self.assertEqual(Specialty.objects.first().name, "Test Specialty")


class TestSpecialtyUpdateView(TestCase):
    def setUp(self):
        self.specialty = Specialty.objects.create(name="Test Specialty", stat="Test")
        self.valid_data = {
            "name": "Test Specialty Updated",
            "stat": "Test",
        }
        self.url = self.specialty.get_update_url()

    def test_update_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/core/specialty/form.html")

    def test_update_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.specialty.refresh_from_db()
        self.assertEqual(self.specialty.name, "Test Specialty Updated")
        self.assertEqual(self.specialty.stat, "Test")
