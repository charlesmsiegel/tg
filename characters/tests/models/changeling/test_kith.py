from django.test import TestCase

from characters.models.changeling.kith import Kith


class TestKithDetailView(TestCase):
    def setUp(self) -> None:
        self.kith = Kith.objects.create(name="Test Kith")
        self.url = self.kith.get_absolute_url()

    def test_kith_detail_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_kith_detail_view_templates(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/changeling/kith/detail.html")


class TestKithCreateView(TestCase):
    def setUp(self):
        self.valid_data = {
            "name": "Kith",
            "description": "Test",
            "affinity": "time",
            "frailty": "sucks",
        }
        self.url = Kith.get_creation_url()

    def test_create_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/changeling/kith/form.html")

    def test_create_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Kith.objects.count(), 1)
        self.assertEqual(Kith.objects.first().name, "Kith")


class TestKithUpdateView(TestCase):
    def setUp(self):
        self.kith = Kith.objects.create(
            name="Test Kith",
            description="Test description",
        )
        self.valid_data = {
            "name": "Kith Updated",
            "description": "Test",
            "affinity": "time",
            "frailty": "sucks",
        }
        self.url = self.kith.get_update_url()

    def test_update_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/changeling/kith/form.html")

    def test_update_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.kith.refresh_from_db()
        self.assertEqual(self.kith.name, "Kith Updated")
        self.assertEqual(self.kith.description, "Test")
