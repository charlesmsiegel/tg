from characters.models.mage.effect import Effect
from characters.models.mage.rote import Rote
from django.test import TestCase
from django.urls import reverse


class TestRoteDetailView(TestCase):
    def setUp(self) -> None:
        self.rote = Rote.objects.create(name="Test Rote")
        self.url = self.rote.get_absolute_url()

    def test_effect_detail_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_effect_detail_view_templates(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/mage/rote/detail.html")


class TestRoteCreateView(TestCase):
    def setUp(self):
        e = Effect.objects.create(name="Test Effect")
        self.valid_data = {
            "name": "Test Rote",
            "effect": e.id,
            "description": "Test",
            "attribute": "tmp",
            "ability": "tmp",
        }
        self.url = reverse("characters:mage:create:rote")

    def test_create_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/mage/rote/form.html")

    def test_create_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Rote.objects.count(), 1)
        self.assertEqual(Rote.objects.first().name, "Test Rote")


class TestRoteUpdateView(TestCase):
    def setUp(self):
        e = Effect.objects.create(name="Test Effect")
        self.rote = Rote.objects.create(name="Test Rote", description="Test")
        self.valid_data = {
            "name": "Test Rote 2",
            "effect": e.id,
            "description": "Test",
            "attribute": "tmp",
            "ability": "tmp",
        }
        self.url = self.rote.get_update_url()

    def test_update_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/mage/rote/form.html")

    def test_update_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)

        self.assertEqual(response.status_code, 302)
        self.rote.refresh_from_db()
        self.assertEqual(self.rote.name, "Test Rote 2")