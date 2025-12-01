from characters.models.mage import Resonance
from django.test import TestCase


class TestResonanceDetailView(TestCase):
    def setUp(self) -> None:
        self.resonance = Resonance.objects.create(name="Test Resonance")
        self.url = self.resonance.get_absolute_url()

    def test_effect_detail_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_effect_detail_view_templates(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/mage/resonance/detail.html")


class TestResonanceCreateView(TestCase):
    def setUp(self):
        self.valid_data = {
            "name": "Test Resonance",
            "correspondence": False,
            "time": False,
            "spirit": False,
            "matter": False,
            "life": False,
            "forces": True,
            "entropy": False,
            "mind": False,
            "prime": True,
        }
        self.url = Resonance.get_creation_url()

    def test_create_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/mage/resonance/form.html")

    def test_create_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Resonance.objects.count(), 1)
        self.assertEqual(Resonance.objects.first().name, "Test Resonance")


class TestResonanceUpdateView(TestCase):
    def setUp(self):
        self.resonance = Resonance.objects.create(name="Test Resonance", description="Test")
        self.valid_data = {
            "name": "Test Resonance 2",
            "correspondence": False,
            "time": False,
            "spirit": False,
            "matter": False,
            "life": False,
            "forces": True,
            "entropy": False,
            "mind": False,
            "prime": True,
        }
        self.url = self.resonance.get_update_url()

    def test_update_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/mage/resonance/form.html")

    def test_update_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.resonance.refresh_from_db()
        self.assertEqual(self.resonance.name, "Test Resonance 2")
        self.assertTrue(self.resonance.prime)
